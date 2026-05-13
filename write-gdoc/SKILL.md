---
name: write-gdoc
description: |-
  Convert a local markdown file to a formatted Google Doc by generating a
  pandoc .docx and uploading it to Google Drive with MIME conversion enabled
  so Drive renders it as a native Google Doc. Optionally uses a template
  Google Doc as a formatting reference.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
---

# write-gdoc: Markdown → docx → Google Doc (upload + convert)

End-to-end workflow: take a local `.md` file, generate a pandoc `.docx`
alongside it, then upload that `.docx` to a Google Drive folder with MIME
conversion so the final artifact is a native Google Doc (with Title style,
real tables, bullet lists, etc. preserved from pandoc).

The docx is the source of truth for formatting. The markdown is only the
author surface.

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Source markdown path | Yes | Local absolute path |
| Target Drive folder ID | Yes | Segment after `/folders/` in the folder URL |
| Doc title | Yes | Becomes Drive filename and docx Title |
| Template Google Doc ID | Optional | Only needed to override the bundled default reference. See Step 3. |
| Output docx path | Optional | Defaults to same directory as source with `.docx` extension |

---

## Workflow

### Step 0 — Preflight

```bash
pandoc --version 2>/dev/null | head -1 || /opt/homebrew/bin/brew install pandoc
```

On macOS Apple Silicon the binary lands at `/opt/homebrew/bin/pandoc`. On
Linux, install via the system package manager (`apt install pandoc`,
`dnf install pandoc`, etc.).

Also install the Google API client libraries used by the upload helper:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 1 — Inspect the template (optional)

If the user provided a template Google Doc ID, fetch it once using the
Google Docs API (or open it manually in a browser) and note paragraph
styles (TITLE, HEADING_1 / 2 / 3), metadata lines (e.g., bold `Author:`,
`Last Updated:`), and any table or list conventions to mirror. Do not copy
content; the template is only a formatting spec.

### Step 2 — Write source markdown with YAML title

For pandoc to apply the Title style in the docx output, the source markdown
must have a YAML frontmatter `title:` field. Everything else is regular
markdown:

```markdown
---
title: "Doc Title Here"
---

**Author:** Name
**Last Updated:** <created date>

# Section 1

Body text.

## Subsection 1.1

- Bullet one
- Bullet two

| Col A | Col B |
|-------|-------|
| x     | y     |
```

### Step 3 — Pick the reference docx

The reference docx controls Title / heading / body fonts, Table borders,
Normal spacing, etc.

**The default is installed globally as pandoc's system default**, so
Step 4's pandoc command does NOT need `--reference-doc`. Pandoc
auto-loads `~/.local/share/pandoc/reference.docx` when no explicit flag
is passed.

| File | Role |
|------|------|
| `~/.local/share/pandoc/reference.docx` | **Active default.** Pandoc auto-loads this for any `.docx` output with no flag required. Installed by copying from the skill-owned source below. |
| `<skill-dir>/reference/template-reference.docx` | **Source-of-truth.** Pre-built from a "Document Template" Google Doc, checklist-patched, with these baked-in customizations: **Heading 1-6 are bold** and **VerbatimChar / SourceCode use Courier New**. When you edit this file, copy it to `~/.local/share/pandoc/reference.docx` to make the change active. |
| `<skill-dir>/reference/pandoc-reference.docx` | Fallback. Pandoc's bundled reference, patched so the Table style has borders. Use via `--reference-doc=...` only when the template style would be inappropriate (e.g., external audience, non-work-format). |

To re-install the default after editing the source:

```bash
cp <skill-dir>/reference/template-reference.docx \
   ~/.local/share/pandoc/reference.docx
```

**Caveat:** Installing the reference globally means *any* pandoc docx
output on this machine picks it up, not just skill invocations. If that's
a problem, skip the install step and pass `--reference-doc=$HOME/...`
explicitly per invocation instead.

#### Overriding the default with a different Google Doc template

If the user provides a different template Google Doc ID, re-export it as
docx and re-run the checklist patcher. This overwrites the bundled
`template-reference.docx`.

```bash
# 1. Export the template Google Doc as docx using Drive's export API:
#    drive.files().export_media(fileId=<TEMPLATE_DOC_ID>,
#                               mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
#    Save the bytes to <skill-dir>/reference/template-reference.docx.
#
#    Alternatively, open the doc in a browser and File → Download → .docx,
#    then move the downloaded file into place.

# 2. Apply the standard checklist (table borders + missing pandoc styles)
python3 <skill-dir>/scripts/prepare_reference_docx.py \
    <skill-dir>/reference/template-reference.docx
```

#### Why the checklist patcher is required for any Google-Docs-exported docx

Drive's export omits several styles pandoc references (`Table`, `Compact`,
`VerbatimChar`, `SourceCode`, `BlockText`, `FootnoteText`,
`FootnoteReference`, `Hyperlink`, `FirstParagraph`), which causes broken
tables and missing code / link formatting. `prepare_reference_docx.py`
checks each style and injects a sensible default if missing. Idempotent.
Run it after every fresh export.

### Step 4 — Generate the docx with pandoc

Run from any directory (paths are absolute):

```bash
/opt/homebrew/bin/pandoc /path/to/input.md -o /path/to/input.docx \
    --from=markdown+pipe_tables-auto_identifiers --standalone
```

No `--reference-doc` needed: pandoc auto-loads
`~/.local/share/pandoc/reference.docx` as the default (Step 3). To force
the vanilla fallback instead, add:

```bash
--reference-doc=$HOME/<skill-dir>/reference/pandoc-reference.docx
```

Flags:
- `pipe_tables` preserves markdown tables as real docx tables.
- `-auto_identifiers` suppresses heading bookmark generation. Pandoc
  otherwise emits a Word bookmark at each heading (anchor IDs from
  slugified heading text) so intra-doc links work. Google Docs preserves
  those bookmarks on import, which clutters the doc. Drop the flag if you
  actually use `[text](#anchor)` intra-doc links.
- `--standalone` writes a full docx (Title style, heading outline, etc.).

**Path gotcha (only relevant when overriding):** If you pass
`--reference-doc=...`, use `$HOME/...`, not `~/...`. The shell does not
expand `~` inside an `--option=value` token in some contexts, and pandoc
will silently fall back to its auto-loaded default without an error.

Verify: `ls -la input.docx`.

If you need to tweak the reference manually (fonts, spacing, margins,
colors):

```bash
# Regenerate the bundled pandoc-reference.docx from scratch, then patch:
/opt/homebrew/bin/pandoc -o <skill-dir>/reference/pandoc-reference.docx \
    --print-default-data-file reference.docx
# Unpack, edit word/styles.xml, repack:
unzip -o <skill-dir>/reference/pandoc-reference.docx -d /tmp/ref_docx
# ... edit ...
(cd /tmp/ref_docx && zip -r -q <skill-dir>/reference/pandoc-reference.docx .)
```

### Step 5 — Upload the docx to Drive with MIME conversion

Goal: upload `input.docx` to the target folder, specifying
`mimeType = application/vnd.google-apps.document` so Drive converts it to a
Google Doc during upload. Title style, headings, tables, and lists carry
over from pandoc's output.

Pick one of the following:

#### Path A — Manual (simplest, no setup)

1. Open Google Drive in a browser and navigate to the target folder.
2. Drive → Settings → General → **Convert uploads**: enable.
3. Drag-drop `input.docx` into the folder. Drive auto-converts it.
4. Rename if needed. Copy the doc URL.

Use this for one-off uploads. Zero dependencies, highest fidelity (Drive
converts the docx server-side using the same code path as "Open with Google
Docs").

#### Path B — Bundled helper script (recommended for repeated use)

This skill ships a helper at `<skill-dir>/scripts/upload_docx_to_gdoc.sh`
that uses the standard `google-api-python-client` library with an OAuth
2.0 user credential.

**One-time setup:**

1. Create an OAuth 2.0 Client ID (Desktop app) in Google Cloud Console:
   <https://console.cloud.google.com/apis/credentials>
2. Save the downloaded JSON to `~/.config/gdoc-upload/credentials.json`
   (override with `--credentials`).
3. Enable the Google Drive API for the same Cloud project.
4. Install the Python dependencies:
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
   If you need a different interpreter, point the wrapper at it:
   ```bash
   export GDOC_UPLOAD_PYTHON=$HOME/.venvs/gdoc-upload/bin/python
   ```

The first invocation opens a browser for consent and caches the token at
`~/.config/gdoc-upload/token.json`. Subsequent runs are silent.

**Invocation:**

```bash
<skill-dir>/scripts/upload_docx_to_gdoc.sh \
    --docx /abs/path/to/input.docx \
    --folder-id <drive_folder_id> \
    --title "Doc Title"
```

Returns JSON:
```json
{
  "id": "<new_doc_id>",
  "name": "Doc Title",
  "parents": ["<folder_id>"],
  "webViewLink": "https://docs.google.com/document/d/<id>/edit?usp=drivesdk",
  "url": "https://docs.google.com/document/d/<id>/edit"
}
```

How it works:
- The `.sh` wrapper finds a Python interpreter (configurable via
  `GDOC_UPLOAD_PYTHON`) and verifies the required Google API libraries
  are importable.
- The `.py` script obtains OAuth user credentials (refreshing or running
  the interactive consent flow as needed), builds a Drive service, then
  calls `drive_service.files().create()` with `mediaMimeType=docx`,
  target `mimeType=application/vnd.google-apps.document`, and
  `parents=[folder_id]`.
- Drive converts the docx to a native Google Doc during upload (Title style,
  headings, tables, bullets all preserved from pandoc output).

### Step 6 — Verify and report

Confirm the resulting Google Doc landed correctly using the Drive API or
by opening the URL returned by the upload helper.

Report to the user:
- Local docx path.
- Google Doc URL.
- Any manual touch-ups needed (e.g., the user needs to change Title style
  font, adjust spacing, add images).

---

## Why docx-with-conversion beats rebuilding from markdown

| Concern | docx → convert | markdown → direct Google Docs API |
|---------|----------------|------------------------------------|
| Title style at the top | Preserved (pandoc YAML `title:`) | Lost (markdown `#` → Heading 1, not Title). Requires an explicit structured-element insert. |
| Real Google Docs tables | Preserved from docx table structure | Direct API path tends to mangle them. |
| Heading hierarchy | Exact from docx | Correct when markdown uses `#` / `##` / `###` consistently. |
| Font / spacing / margins | From docx styles (reference-doc friendly) | Drive defaults. No font control. |
| Chunking | Single upload, no size limit matters | Must chunk ≤ 7 500 chars at newline boundaries. |
| Fidelity to a template | High (pandoc `--reference-doc=template.docx`) | Low. Template has to be inspected and matched by post-hoc structured edits. |

The upload path puts the formatting contract in the docx, where pandoc has
first-class control. The markdown-rebuild path puts it in the Google Docs
API, where the rendering rules are less predictable.

---

## Known quirks

| Quirk | Mitigation |
|-------|-----------|
| Pandoc's default Table style has no borders; markdown tables render borderless in Google Docs. | Always pass `--reference-doc=$HOME/<skill-dir>/reference/pandoc-reference.docx` (this skill bundles a patched reference with `<w:tblBorders>` added to the Table style). |
| Drive "Convert uploads" setting is per-account, not per-upload, in the UI. | Enable once in Drive → Settings → General. Path B sets the target mimeType explicitly, so the setting does not affect it. |
| pandoc defaults to A4 page size. | Not usually a problem for Google Docs (it re-renders to its own page size), but matters if the docx is also distributed as-is. Set `--metadata papersize=letter` or use a reference-doc to pin US Letter. |
| First run of the upload helper opens a browser for OAuth consent. | Click through once; the cached token at `~/.config/gdoc-upload/token.json` is reused silently afterwards. |
| Smart quotes, em dashes, arrows (→), and Unicode characters pass through cleanly. | No mitigation needed. |

---

## Related skills

- `docx` — fine-grained docx authoring (docx-js, tracked changes) when
  pandoc defaults are insufficient and you want to hand-craft the docx.
