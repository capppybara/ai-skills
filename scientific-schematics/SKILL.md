---
name: scientific-schematics
description: Create publication-quality scientific diagrams. Claude generates optimized image prompts, user pastes into any image gen tool and shares back, Claude reviews quality against document-type thresholds. No API key required. Specialized in neural network architectures, system diagrams, flowcharts, biological pathways, and complex scientific visualizations.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Ke Jiang
    adapted-from: K-Dense-AI/scientific-agent-skills/scientific-skills/scientific-schematics
---

# Scientific Schematics and Diagrams

> Adapted from [K-Dense AI's scientific-schematics SKILL.md](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/scientific-schematics/SKILL.md) (MIT). Color guidance updated for our workflow.

## Overview

Scientific schematics and diagrams transform complex concepts into clear visual representations for publication. **This skill uses Claude to generate optimized image prompts and review results, with you generating the image in any image gen tool.**

**How it works:**
- Describe your diagram in natural language
- Claude generates an optimized image generation prompt
- You paste the prompt into any image gen tool (ChatGPT, Gemini, Ideogram, DALL-E, etc.) and share the result back
- **Claude reviews quality** against document-type thresholds
- **Smart iteration**: Only re-prompts if quality is below threshold
- Publication-ready output in minutes
- No API key required

**Quality Thresholds by Document Type:**
| Document Type | Threshold | Description |
|---------------|-----------|-------------|
| journal | 8.5/10 | Nature, Science, peer-reviewed journals |
| conference | 8.0/10 | Conference papers |
| thesis | 8.0/10 | Dissertations, theses |
| grant | 8.0/10 | Grant proposals |
| preprint | 7.5/10 | arXiv, bioRxiv, etc. |
| report | 7.5/10 | Technical reports |
| poster | 7.0/10 | Academic posters |
| presentation | 6.5/10 | Slides, talks |
| default | 7.5/10 | General purpose |

**Simply describe what you want, and Claude crafts the prompt.** All diagrams are stored in the figures/ subfolder and referenced in papers/posters.

## Quick Start: Generate Any Diagram

Create any scientific diagram by simply describing it to Claude:

1. Tell Claude what diagram you want and the document type (journal, poster, presentation, etc.)
2. Claude generates an optimized image prompt
3. Paste the prompt into your image gen tool of choice and share the result back
4. Claude reviews and scores the result — if below threshold, it refines the prompt and you repeat

**What happens:**
1. **Prompt 1**: Claude constructs a detailed prompt following scientific diagram best practices
2. **Review 1**: **Claude** evaluates the image quality against document-type threshold
3. **Decision**: If quality >= threshold → **DONE** (no more iterations needed!)
4. **If below threshold**: Claude refines the prompt based on critique
5. **Repeat**: Until quality meets threshold OR max iterations reached (max 2)

**Smart Iteration Benefits:**
- ✅ Higher quality standards for journal papers
- ✅ Faster turnaround for presentations/posters
- ✅ Appropriate quality for each use case
- ✅ No API key required

**Output**: Versioned images plus a detailed review log with quality scores, critiques, and early-stop information.

### Configuration

No API key required. Just use any image generation tool you have access to (ChatGPT with DALL-E, Gemini, Ideogram, Adobe Firefly, etc.).

### AI Generation Best Practices

**Effective Prompts for Scientific Diagrams:**

✓ **Good prompts** (specific, detailed):
- "CONSORT flowchart showing participant flow from screening (n=500) through randomization to final analysis"
- "Transformer neural network architecture with encoder stack on left, decoder stack on right, showing multi-head attention and cross-attention connections"
- "Biological signaling cascade: EGFR receptor → RAS → RAF → MEK → ERK → nucleus, with phosphorylation steps labeled"
- "Block diagram of IoT system: sensors → microcontroller → WiFi module → cloud server → mobile app"

✗ **Avoid vague prompts**:
- "Make a flowchart" (too generic)
- "Neural network" (which type? what components?)
- "Pathway diagram" (which pathway? what molecules?)

**Key elements to include:**
- **Type**: Flowchart, architecture diagram, pathway, circuit, etc.
- **Components**: Specific elements to include
- **Flow/Direction**: How elements connect (left-to-right, top-to-bottom)
- **Labels**: Key annotations or text to include
- **Style**: Any specific visual requirements

**Scientific Quality Guidelines** (automatically applied):
- Clean white/light background
- High contrast for readability
- Clear, readable labels (minimum 10pt)
- Professional typography (sans-serif fonts)
- Colorblind-friendly colors (Okabe-Ito palette)
- Proper spacing to prevent crowding
- Scale bars, legends, axes where appropriate

## When to Use This Skill

This skill should be used when:
- Creating neural network architecture diagrams (Transformers, CNNs, RNNs, etc.)
- Illustrating system architectures and data flow diagrams
- Drawing methodology flowcharts for study design (CONSORT, PRISMA)
- Visualizing algorithm workflows and processing pipelines
- Creating circuit diagrams and electrical schematics
- Depicting biological pathways and molecular interactions
- Generating network topologies and hierarchical structures
- Illustrating conceptual frameworks and theoretical models
- Designing block diagrams for technical papers

## How to Use This Skill

**Simply describe your diagram in natural language.** Claude generates the prompt automatically.

**That's it!** Claude handles:
- ✓ Layout and composition
- ✓ Labels and annotations
- ✓ Colors and styling
- ✓ Quality review and refinement
- ✓ Publication-ready output

**Works for all diagram types:**
- Flowcharts (CONSORT, PRISMA, etc.)
- Neural network architectures
- Biological pathways
- Circuit diagrams
- System architectures
- Block diagrams
- Any scientific visualization

**No coding, no templates, no manual drawing required.**

---

# Generation Workflow (Claude Prompt + User Image Gen + Claude Review)

## Smart Iterative Refinement Workflow

The workflow uses **smart iteration** - it only re-prompts if quality is below the threshold for your document type:

### How Smart Iteration Works

```
┌─────────────────────────────────────────────────────┐
│  1. Claude generates optimized image prompt         │
│                    ↓                                │
│  2. Prompt presented to user                        │
│                    ↓                                │
│  3. User generates image and shares back            │
│                    ↓                                │
│  4. Claude reviews quality                          │
│                    ↓                                │
│  5. Score >= threshold?                             │
│       YES → DONE! (early stop)                      │
│       NO  → Improve prompt, go to step 2            │
│                    ↓                                │
│  6. Repeat until quality met OR max iterations      │
└─────────────────────────────────────────────────────┘
```

### Iteration 1: Initial Generation
**Prompt Construction:**
```
Scientific diagram guidelines + User request
```

**Output:** `diagram_v1.png`

### Quality Review by Claude

Claude evaluates the diagram on:
1. **Scientific Accuracy** (0-2 points) - Correct concepts, notation, relationships
2. **Clarity and Readability** (0-2 points) - Easy to understand, clear hierarchy
3. **Label Quality** (0-2 points) - Complete, readable, consistent labels
4. **Layout and Composition** (0-2 points) - Logical flow, balanced, no overlaps
5. **Professional Appearance** (0-2 points) - Publication-ready quality

**Example Review Output:**
```
SCORE: 8.0

STRENGTHS:
- Clear flow from top to bottom
- All phases properly labeled
- Professional typography

ISSUES:
- Participant counts slightly small
- Minor overlap on exclusion box

VERDICT: ACCEPTABLE (for poster, threshold 7.0)
```

### Decision Point: Continue or Stop?

| If Score... | Action |
|-------------|--------|
| >= threshold | **STOP** - Quality is good enough for this document type |
| < threshold | Continue to next iteration with improved prompt |

**Example:**
- For a **poster** (threshold 7.0): Score of 7.5 → **DONE after 1 iteration!**
- For a **journal** (threshold 8.5): Score of 7.5 → Continue improving

### Subsequent Iterations (Only If Needed)

If quality is below threshold, the system:
1. Extracts specific issues from Claude's review
2. Enhances the prompt with improvement instructions
3. You regenerate using your image gen tool
4. Claude reviews again
5. Repeats until threshold met or max iterations reached

## Advanced AI Generation Usage

### Prompt Engineering Tips

**1. Be Specific About Layout:**
```
✓ "Flowchart with vertical flow, top to bottom"
✓ "Architecture diagram with encoder on left, decoder on right"
✓ "Circular pathway diagram with clockwise flow"
```

**2. Include Quantitative Details:**
```
✓ "Neural network with input layer (784 nodes), hidden layer (128 nodes), output (10 nodes)"
✓ "Flowchart showing n=500 screened, n=150 excluded, n=350 randomized"
✓ "Circuit with 1kΩ resistor, 10µF capacitor, 5V source"
```

**3. Specify Visual Style:**
```
✓ "Minimalist block diagram with clean lines"
✓ "Detailed biological pathway with protein structures"
✓ "Technical schematic with engineering notation"
```

**4. Request Specific Labels:**
```
✓ "Label all arrows with activation/inhibition"
✓ "Include layer dimensions in each box"
✓ "Show time progression with timestamps"
```

**5. Mention Color Requirements:**
```
✓ "Use colorblind-friendly colors"
✓ "Grayscale-compatible design"
✓ "Color-code by function: blue for input, green for processing, red for output"
```

### Color Guidance

Default to **colorblind-friendly** palettes (Okabe-Ito). Color-code by function:

- **Grey** — input / source data
- **Blue** — processing / transformation steps
- **Yellow** — decisions / branch points
- **Green** — output / terminal states

For terminal / output cells specifically, split by valence: **green** for positive outcomes (success, pass, gain) and **red** for negative outcomes (failure, error, loss).

For business / corporate slides, adapt to a brand palette. A reasonable generic default:
- Blue `#2563EB` — primary, headers
- Teal `#14B8A6` — secondary / accent
- Green `#16A34A` — success / "go"
- Purple `#9333EA` — alt / optional path
- Neutral `#111827` dark / `#F9FAFB` light background

Substitute your organization's brand colors where applicable.

Ensure grayscale-compatible contrast; don't rely on color alone — use shape / pattern redundancy.

## Example Prompts

Paste any of these into your image gen tool. They illustrate the level of specificity that produces good results.

### Example 1: CONSORT Flowchart

> CONSORT participant flow diagram for randomized controlled trial. Start with "Assessed for eligibility (n=500)" at top. Show "Excluded (n=150)" with reasons: age<18 (n=80), declined (n=50), other (n=20). Then "Randomized (n=350)" splits into two arms: "Treatment group (n=175)" and "Control group (n=175)". Each arm shows "Lost to follow-up" (n=15 and n=10). End with "Analyzed" (n=160 and n=165). Use blue boxes for process steps, orange for exclusion, green for final analysis.

### Example 2: Neural Network Architecture

> Transformer encoder-decoder architecture diagram. Left side: Encoder stack with input embedding, positional encoding, multi-head self-attention, add & norm, feed-forward, add & norm. Right side: Decoder stack with output embedding, positional encoding, masked self-attention, add & norm, cross-attention (receiving from encoder), add & norm, feed-forward, add & norm, linear & softmax. Show cross-attention connection from encoder to decoder with dashed line. Use light blue for encoder, light red for decoder. Label all components clearly.

### Example 3: Biological Pathway

> MAPK signaling pathway diagram. Start with EGFR receptor at cell membrane (top). Arrow down to RAS (with GTP label). Arrow to RAF kinase. Arrow to MEK kinase. Arrow to ERK kinase. Final arrow to nucleus showing gene transcription. Label each arrow with "phosphorylation" or "activation". Use rounded rectangles for proteins, different colors for each. Include membrane boundary line at top.

### Example 4: System Architecture

> IoT system architecture block diagram. Bottom layer: Sensors (temperature, humidity, motion) in green boxes. Middle layer: Microcontroller (ESP32) in blue box. Connections to WiFi module (orange box) and Display (purple box). Top layer: Cloud server (gray box) connected to mobile app (light blue box). Show data flow arrows between all components. Label connections with protocols: I2C, UART, WiFi, HTTPS.

## Best Practices Summary

### Design Principles

1. **Clarity over complexity** - Simplify, remove unnecessary elements
2. **Consistent styling** - Use templates and style files
3. **Colorblind accessibility** - Use Okabe-Ito palette, redundant encoding
4. **Appropriate typography** - Sans-serif fonts, minimum 7-8 pt
5. **Vector format** - Always use PDF/SVG for publication

### Technical Requirements

1. **Resolution** - Vector preferred, or 300+ DPI for raster
2. **File format** - PDF for LaTeX, SVG for web, PNG as fallback
3. **Color space** - RGB for digital, CMYK for print (convert if needed)
4. **Line weights** - Minimum 0.5 pt, typical 1-2 pt
5. **Text size** - 7-8 pt minimum at final size

### Integration Guidelines

1. **Include in LaTeX** - Use `\includegraphics{}` for generated images
2. **Caption thoroughly** - Describe all elements and abbreviations
3. **Reference in text** - Explain diagram in narrative flow
4. **Maintain consistency** - Same style across all figures in paper
5. **Version control** - Keep prompts and generated images in repository

## Troubleshooting Common Issues

### Output Doesn't Match Prompt

**Problem**: Text in labels is garbled, misspelled, or hallucinated
- Quote each label exactly in the prompt: `Label the box "Randomized (n=350)"` — not `Label it as randomized`
- Enumerate every label; don't rely on the tool inferring them
- If text quality stays poor across attempts, switch image gen tools — text rendering varies significantly between them

**Problem**: Layout is wrong (wrong direction, wrong positions)
- State flow direction explicitly: `vertical flow, top to bottom` or `horizontal flow, left to right`
- Use capitalized position words: `Encoder on the LEFT, Decoder on the RIGHT`
- Describe the connection pattern: `arrows from A to B, then B splits into C and D`

**Problem**: Elements are missing or extras appear
- Enumerate the complete element list as a bulleted list in the prompt
- For extras, re-prompt with: `remove [X], keep everything else the same`
- For missing items, re-prompt with: `add [X] in position [where], keep the rest`

### Output Has Visual Issues

**Problem**: Labels overlap shapes or each other
- Ask for labels outside shapes with leader lines: `place labels outside each box with leader lines pointing to the shape`
- Specify relative positioning: `label above the arrow, not overlapping it`

**Problem**: Colors don't match the convention you asked for
- Restate the convention in the re-prompt; tools often revert to defaults between attempts
- If a tool keeps ignoring color guidance, assign colors per element: `RAS in grey, RAF in blue, ERK in green`

**Problem**: Style is wrong (cartoony, cluttered, not publication-ready)
- Add style keywords: `clean, technical, minimalist, publication-quality, flat design, thin strokes`
- Request a specific aesthetic: `in the style of a scientific journal figure`

## Resources and References

### Detailed References

Load these files for comprehensive information on specific topics:

- **`references/best_practices.md`** - Publication standards, journal column widths, Okabe-Ito palette with hex values, line weights, common pitfalls, WCAG contrast ratios
- **`references/README.md`** - Upstream usage notes (inherited from K-Dense AI)

### External Resources

**Python Libraries** (for manual diagram drawing when image gen isn't a fit)
- Schemdraw Documentation: https://schemdraw.readthedocs.io/
- NetworkX Documentation: https://networkx.org/documentation/
- Matplotlib Documentation: https://matplotlib.org/

**Publication Standards**
- Nature Figure Guidelines: https://www.nature.com/nature/for-authors/final-submission
- Science Figure Guidelines: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- CONSORT Diagram: http://www.consort-statement.org/consort-statement/flow-diagram

## Integration with Other Skills

This skill works synergistically with:

- **Scientific Writing** - Diagrams follow figure best practices
- **Scientific Visualization** - Shares color palettes and styling
- **LaTeX Posters** - Generate diagrams for poster presentations
- **Research Grants** - Methodology diagrams for proposals
- **Peer Review** - Evaluate diagram clarity and accessibility

## Quick Reference Checklist

Before submitting diagrams, verify:

### Visual Quality
- [ ] High-quality image format (PNG from AI generation)
- [ ] No overlapping elements (AI handles automatically)
- [ ] Adequate spacing between all components (AI optimizes)
- [ ] Clean, professional alignment
- [ ] All arrows connect properly to intended targets

### Accessibility
- [ ] Colorblind-safe palette (Okabe-Ito) used
- [ ] Works in grayscale (tested with accessibility checker)
- [ ] Sufficient contrast between elements (verified)
- [ ] Redundant encoding where appropriate (shapes + colors)
- [ ] Colorblind simulation passes all checks

### Typography and Readability
- [ ] Text minimum 7-8 pt at final size
- [ ] All elements labeled clearly and completely
- [ ] Consistent font family and sizing
- [ ] No text overlaps or cutoffs
- [ ] Units included where applicable

### Publication Standards
- [ ] Consistent styling with other figures in manuscript
- [ ] Comprehensive caption written with all abbreviations defined
- [ ] Referenced appropriately in manuscript text
- [ ] Meets journal-specific dimension requirements
- [ ] Exported in required format for journal (PDF/EPS/TIFF)

### Documentation and Version Control
- [ ] Source files (.tex, .py) saved for future revision
- [ ] Quality reports archived in `quality_reports/` directory
- [ ] Configuration parameters documented (colors, spacing, sizes)
- [ ] Git commit includes source, output, and quality reports
- [ ] README or comments explain how to regenerate figure

### Final Integration Check
- [ ] Figure displays correctly in compiled manuscript
- [ ] Cross-references work (`\ref{}` points to correct figure)
- [ ] Figure number matches text citations
- [ ] Caption appears on correct page relative to figure
- [ ] No compilation warnings or errors related to figure


