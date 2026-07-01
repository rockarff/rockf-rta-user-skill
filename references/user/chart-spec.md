# Chart Spec

The MVP outputs Mermaid chart drafts.

If the environment supports SVG or PNG export, convert Mermaid or HTML/SVG later. Do not block the core analysis on image export.

## User Profiles Chart

Show four user groups:

- potential users
- core users
- high-value users
- unfit users

Each group should show:

- identity
- current situation
- key pains
- decision barriers
- trust sources
- fit judgment

Recommended Mermaid type:

`flowchart` or `mindmap`

## User Lifecycle Chart

Show ten fixed stages:

`无意识 -> 有意识 -> 记住你 -> 关注你 -> 了解你 -> 接触你 -> 好朋友 -> 选择你 -> 有收获 -> 转介绍`

Each stage should include:

- user thoughts
- user behaviors
- core pains
- progress actions
- signals

Recommended format:

- Mermaid flowchart for compact display
- Markdown table for full detail
- SVG/HTML table for final visual output when available

## Visual Priority

Charts are for the customer to understand quickly.

Markdown and JSON are for downstream skills.

Do not sacrifice structured data quality for a prettier chart.

