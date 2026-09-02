# BriefPilot design system

BriefPilot remains its own product, but its visual language is intentionally aligned with the **current Kitoki Studio palette**.

## Kitoki palette used

Source: current `kitoki-red-system.css` in `kitoki-studio-showcase-main`.

- Kitoki Red: `hsl(355 100% 45%)`
- Kitoki Red Strong: `hsl(355 100% 39%)`
- Kitoki Red Soft: `hsl(354 77% 95%)`
- Washed Blue: `hsl(216 18% 36%)`
- Washed Blue Strong: `hsl(216 19% 30%)`
- Washed Blue Soft: `hsl(216 18% 95%)`
- Ink: `hsl(220 13% 9%)`
- Pearl: `hsl(45 22% 98%)`
- Radius: 6px
- Primary typeface: General Sans with system fallbacks

## How BriefPilot uses the palette

- **Pearl** is the main background so the interface stays calm and editorial.
- **Ink** anchors primary information and the human-decision panel.
- **Washed Blue** structures panels, informational states, labels, and successful routine agent work.
- **Kitoki Red** is intentionally reserved for action, attention, active states, and the wordmark dot.
- **Red Soft** is used for the final human-decision state instead of introducing a foreign green/yellow status palette.

## Borrowed interaction pattern

The agent activity panel reuses the restrained loading language from Kitoki's Website Check:
- a red pulse dot for the current active/waiting step;
- a narrow animated red scan track;
- no fake percentage or implied completion estimate.

This gives BriefPilot more visual identity while staying honest about what the agent is actually doing.

## Product rule

BriefPilot should feel visibly related to Kitoki without looking like a copied section of the Kitoki website. The palette is stronger now, but color remains disciplined rather than decorative.
