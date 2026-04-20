# scientific-schematics

Create publication-quality scientific diagrams via a copy-paste image-gen workflow. Claude writes an optimized prompt, you paste it into any image-gen tool (ChatGPT/DALL-E, Gemini, Ideogram, Firefly, etc.), then Claude reviews the result against document-type quality thresholds and iterates if needed.

**No API keys required.**

## Contents

- **`SKILL.md`** — primary skill definition (overview, workflow, prompt engineering, color conventions, example prompts, troubleshooting).
- **`references/best_practices.md`** — publication standards: journal column widths (Nature, Science, Cell, PLOS, IEEE), Okabe-Ito colorblind-friendly palette, line weights, common pitfalls, WCAG contrast ratios, 10 Golden Rules for scientific figures. Tool-agnostic reference on what "publication-ready" means for a specific venue.

## Attribution

Adapted from [K-Dense AI's scientific-schematics skill](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/scientific-skills/scientific-schematics) (MIT). The upstream version assumed an OpenRouter + Nano Banana 2 + Gemini automated pipeline; this version is rewritten for a copy-paste workflow so it works in any environment without model-provider credentials.
