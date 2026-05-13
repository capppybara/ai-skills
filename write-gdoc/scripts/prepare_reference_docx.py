#!/usr/bin/env python3
"""
prepare_reference_docx.py

Inject missing pandoc-referenced styles into a docx that will be used as
pandoc's `--reference-doc`. Especially useful for docx files exported from
Google Docs, which routinely omit style definitions that pandoc emits
references to (e.g., "Table", "Compact", "VerbatimChar").

The script is deliberately conservative: it only injects styles that are
missing. It does NOT modify pre-existing style definitions. Opinionated
formatting (bold headings, specific code fonts, etc.) should be baked into
a specific reference docx once, not forced on every docx that passes
through this checklist.

All fixes are idempotent: safe to run repeatedly.

USAGE:
    python3 prepare_reference_docx.py <input.docx> [-o <output.docx>]

    # In-place (default)
    python3 prepare_reference_docx.py /path/to/exported.docx

    # Out-of-place
    python3 prepare_reference_docx.py /path/to/exported.docx -o /path/to/patched.docx
"""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


# --- Phase 1: INJECT-IF-MISSING fixes -------------------------------------
#
# Each entry is (name, detection_marker, injection_xml).
# - name: human-readable fix name, for logging
# - detection_marker: if this substring already appears in styles.xml, the
#   fix is treated as applied and skipped. Keep the marker unique to that
#   style definition (e.g., include the styleId attribute).
# - injection_xml: the XML snippet to insert immediately before `</w:styles>`
#   when the marker is missing.

FIXES: list[tuple[str, str, str]] = [
    (
        "Table style (markdown tables, bordered)",
        'w:styleId="Table"',
        (
            '<w:style w:type="table" w:styleId="Table">'
            '<w:name w:val="Table"/>'
            '<w:basedOn w:val="TableNormal"/>'
            '<w:tblPr>'
            '<w:tblBorders>'
            '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
            '</w:tblBorders>'
            '<w:tblCellMar>'
            '<w:top w:w="80" w:type="dxa"/>'
            '<w:left w:w="108" w:type="dxa"/>'
            '<w:bottom w:w="80" w:type="dxa"/>'
            '<w:right w:w="108" w:type="dxa"/>'
            '</w:tblCellMar>'
            '</w:tblPr>'
            '</w:style>'
        ),
    ),
    (
        "Compact paragraph style (tight list items, table cells)",
        'w:styleId="Compact"',
        (
            '<w:style w:type="paragraph" w:styleId="Compact" w:customStyle="1">'
            '<w:name w:val="Compact"/>'
            '<w:basedOn w:val="Normal"/>'
            '<w:pPr>'
            '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
            '</w:pPr>'
            '</w:style>'
        ),
    ),
    (
        "FirstParagraph style (para after heading, no extra top space)",
        'w:styleId="FirstParagraph"',
        (
            '<w:style w:type="paragraph" w:styleId="FirstParagraph" w:customStyle="1">'
            '<w:name w:val="First Paragraph"/>'
            '<w:basedOn w:val="Normal"/>'
            '<w:pPr>'
            '<w:ind w:firstLine="0"/>'
            '</w:pPr>'
            '</w:style>'
        ),
    ),
    (
        "VerbatimChar (inline `code` spans, Consolas)",
        'w:styleId="VerbatimChar"',
        (
            '<w:style w:type="character" w:styleId="VerbatimChar" w:customStyle="1">'
            '<w:name w:val="Verbatim Char"/>'
            '<w:rPr>'
            '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
            '</w:rPr>'
            '</w:style>'
        ),
    ),
    (
        "SourceCode (fenced code blocks, Consolas)",
        'w:styleId="SourceCode"',
        (
            '<w:style w:type="paragraph" w:styleId="SourceCode" w:customStyle="1">'
            '<w:name w:val="Source Code"/>'
            '<w:basedOn w:val="Normal"/>'
            '<w:pPr>'
            '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
            '</w:pPr>'
            '<w:rPr>'
            '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>'
            '</w:rPr>'
            '</w:style>'
        ),
    ),
    (
        "BlockText (block quotes, italic)",
        'w:styleId="BlockText"',
        (
            '<w:style w:type="paragraph" w:styleId="BlockText">'
            '<w:name w:val="Block Text"/>'
            '<w:basedOn w:val="Normal"/>'
            '<w:pPr>'
            '<w:ind w:left="720" w:right="720"/>'
            '</w:pPr>'
            '<w:rPr>'
            '<w:i/>'
            '</w:rPr>'
            '</w:style>'
        ),
    ),
    (
        "FootnoteText (footnote body, smaller font)",
        'w:styleId="FootnoteText"',
        (
            '<w:style w:type="paragraph" w:styleId="FootnoteText">'
            '<w:name w:val="footnote text"/>'
            '<w:basedOn w:val="Normal"/>'
            '<w:rPr>'
            '<w:sz w:val="20"/>'
            '<w:szCs w:val="20"/>'
            '</w:rPr>'
            '</w:style>'
        ),
    ),
    (
        "FootnoteReference (footnote markers, superscript)",
        'w:styleId="FootnoteReference"',
        (
            '<w:style w:type="character" w:styleId="FootnoteReference">'
            '<w:name w:val="footnote reference"/>'
            '<w:rPr>'
            '<w:vertAlign w:val="superscript"/>'
            '</w:rPr>'
            '</w:style>'
        ),
    ),
    (
        "Hyperlink (links, blue underline)",
        'w:styleId="Hyperlink"',
        (
            '<w:style w:type="character" w:styleId="Hyperlink">'
            '<w:name w:val="Hyperlink"/>'
            '<w:rPr>'
            '<w:color w:val="1155CC"/>'
            '<w:u w:val="single"/>'
            '</w:rPr>'
            '</w:style>'
        ),
    ),
]


# --- Core logic -----------------------------------------------------------

def apply_fixes(styles_xml: str) -> tuple[str, list[str], list[str]]:
    """
    Inject every FIXES entry whose marker is missing. Returns
    (patched_xml, injected, skipped).
    """
    injected: list[str] = []
    skipped: list[str] = []
    out = styles_xml
    for name, marker, xml in FIXES:
        if marker in out:
            skipped.append(name)
            continue
        if "</w:styles>" not in out:
            raise RuntimeError("styles.xml is malformed: missing </w:styles>")
        out = out.replace("</w:styles>", xml + "</w:styles>", 1)
        injected.append(name)
    return out, injected, skipped


def patch_docx(src: Path, dst: Path) -> tuple[list[str], list[str]]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(src, "r") as zf:
            zf.extractall(tmp_path)
        styles = tmp_path / "word" / "styles.xml"
        if not styles.exists():
            raise RuntimeError(f"Not a docx (no word/styles.xml inside): {src}")
        original = styles.read_text(encoding="utf-8")
        patched, injected, skipped = apply_fixes(original)
        if patched != original:
            styles.write_text(patched, encoding="utf-8")
        if dst.exists():
            dst.unlink()
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in tmp_path.rglob("*"):
                if path.is_file():
                    zf.write(path, path.relative_to(tmp_path))
    return injected, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_docx", help="Input docx to patch")
    ap.add_argument("-o", "--output", help="Output path (defaults to in-place)")
    args = ap.parse_args()

    src = Path(args.input_docx).expanduser().resolve()
    if not src.exists():
        print(f"ERROR: not found: {src}", file=sys.stderr)
        return 2
    if src.suffix.lower() != ".docx":
        print(f"ERROR: expected .docx, got {src.suffix}", file=sys.stderr)
        return 2

    dst = Path(args.output).expanduser().resolve() if args.output else src
    inplace = dst == src

    if inplace:
        tmp_dst = src.with_suffix(".docx.tmp")
        injected, skipped = patch_docx(src, tmp_dst)
        shutil.move(str(tmp_dst), str(src))
    else:
        injected, skipped = patch_docx(src, dst)

    print(f"Reference docx prepared: {dst}")
    if injected:
        print(f"  Injected {len(injected)} missing style(s):")
        for name in injected:
            print(f"    + {name}")
    if skipped:
        print(f"  Skipped {len(skipped)} (already present):")
        for name in skipped:
            print(f"    = {name}")
    if not (injected or skipped):
        print("  No fixes defined (empty checklist?)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
