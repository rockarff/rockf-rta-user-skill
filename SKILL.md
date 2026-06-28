---
name: rta-user-skill
description: Use this skill when the user wants an AI Agent to run a structured user interview or analyze an interview transcript, then produce RTA-based user profiles and a ten-stage user lifecycle. It supports live Q&A interviews and transcript analysis, outputs four user profile types, a fixed ten-stage lifecycle, Markdown, JSON, and Mermaid chart drafts for later content, sales, presentation, or product-design skills.
---

# RTA-USER Skill

RTA-USER is a user insight interview skill based on the RTA model.

Use it to turn real answers or interview transcripts into:

- four user profiles
- a ten-stage user lifecycle
- Markdown reports
- JSON data for downstream skills
- Mermaid chart drafts

Do not limit the analysis to one industry. Start from the customer's business, users, scenes, pains, trust, and purchase decisions.

## Core Model

RTA = Reach - Trust - Asset.

This skill focuses mainly on Trust:

- who the users are
- what situations they are in
- why they hesitate
- why they trust
- why they buy
- why they recommend

The output must still serve the larger loop:

`content -> user -> business`

## Choose The Mode

Before starting, identify the mode.

### Live Interview Mode

Use this when the user wants the agent to interview them directly.

Process:

1. Ask one group of questions at a time.
2. Do not dump the full question bank at once.
3. After each answer, decide whether to proceed or ask a follow-up.
4. Keep probing until there is enough evidence to build profiles and lifecycle.
5. Generate outputs only after the interview is complete.

Read:

- `references/interview-flow.md`
- `references/question-bank.md`
- `references/output-schema.md`

### Transcript Analysis Mode

Use this when the user provides a transcript from an interview.

Process:

1. Read the transcript.
2. Extract business context, user types, scenes, pains, trust signals, and decision barriers.
3. Judge information quality: high, medium, or low.
4. If there are gaps, ask 3-8 focused follow-up questions.
5. Generate outputs after enough evidence is available.

Read:

- `references/interview-flow.md`
- `references/output-schema.md`

## Required Outputs

Always produce two core outputs:

1. User profiles
2. User lifecycle

Do not produce a content opportunity map in the MVP unless the user explicitly asks.

## Four User Profile Types

Always distinguish:

- potential users
- core users
- high-value users
- unfit users

For each type, include:

- user name
- one-line description
- identity
- current situation
- typical needs
- surface problems
- deep pains
- trigger scenarios
- decision barriers
- trust sources
- payment willingness
- fit judgment
- identification signals
- source evidence

## Ten Lifecycle Stages

Always use these fixed stages:

`无意识 -> 有意识 -> 记住你 -> 关注你 -> 了解你 -> 接触你 -> 好朋友 -> 选择你 -> 有收获 -> 转介绍`

For each stage, include:

- stage goal
- typical scenarios
- touchpoints
- user thoughts
- user behaviors
- core pains
- trust barriers
- progress actions
- signals

Important:

`core_pains` must include at least 3 items per stage. Prefer 3-5 specific pains.

## Evidence Rules

Do not invent user profiles.

If the source does not support a conclusion, mark it as:

`待补充`

Use the customer's wording, cases, examples, and transaction facts as evidence.

A user profile is not a demographic table. Focus on:

- situation
- problem
- decision
- trust
- payment
- fit

## Output Files

When file creation is requested or possible, generate:

```text
outputs/
├── user-profiles.md
├── user-lifecycle.md
├── user-insights.json
├── user-profiles-chart.mmd
├── user-lifecycle-chart.mmd
└── report.md
```

Use templates from:

- `templates/user-profiles.md`
- `templates/user-lifecycle.md`
- `templates/report.md`
- `templates/user-insights.schema.json`

For chart requirements, read:

- `references/chart-spec.md`

