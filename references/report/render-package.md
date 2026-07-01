# Render Package

When this skill renders a client-facing package, use the following default output contract.

## Main Files

- `research-report.html`
- `topic-appendix.html`
- `research-report-preview.png`
- `topic-appendix-preview.png`

## Supporting Files

- `report-summary.md`
- `report-speaker-notes.md`
- `report-evidence-map.md`
- `report-output.json`
- `report-structure.json`

## Render Logic

### Main Report

Use for:

- client presentation
- delivery meeting
- review with the client

Rules:

- concise
- page-like structure
- representative topics only

### Topic Appendix

Use for:

- internal review
- content planning
- detailed delivery attachment

Rules:

- full topic inventory
- compact table layout
- no extra explanation blocks

## Preview Requirement

Every rendered HTML package should have a preview image generated before delivery.

Check:

- text is readable
- no blocks overflow
- no page section is visually broken
- main report and appendix have clearly different information density
