---
name: rta-discovery-skill
description: Use this skill when the user needs to decide what kind of client they are interviewing before any RTA user analysis starts, then generate the right interview script and material checklist. It classifies the client as zero-based, validated, or mixed, outputs a Discovery diagnosis, interview path, question set, required research materials, and a manual confirmation handoff before RTA-USER begins.
---

# RTA-DISCOVERY Skill

RTA-DISCOVERY is the entry skill for the RTA workflow.

Use it before:

- RTA-USER
- user profiles
- user lifecycle
- persona design

It does not generate final user insights.  
It only does three things:

1. classify the client type
2. generate the right interview path
3. define what materials must be collected next

## Workflow

Always follow this order:

`classify -> build interview script -> collect materials -> manual confirmation -> handoff`

Read these files before acting:

- `references/client-types.md`
- `references/interview-paths.md`
- `references/question-design-rules.md`
- `references/material-checklist.md`
- `references/handoff-schema.md`

Use templates from:

- `templates/diagnosis-form.md`
- `templates/zero-based-interview.md`
- `templates/validated-interview.md`
- `templates/mixed-interview.md`
- `templates/discovery-output.schema.json`

## Step 1: Classify The Client

Always classify the client first.

Supported types:

- `zero_based`
- `validated`
- `mixed`

If the user has not provided enough information, ask only the minimum questions needed to classify them.

## Step 2: Generate The Interview Script

After classification, choose only one interview path:

- zero-based path
- validated path
- mixed path

Do not dump every question.  
Generate a structured interview script with:

- interview goal
- modules
- questions
- what each module must discover

## Step 3: Define The Material Checklist

Always output three levels:

- required
- recommended
- bonus

The checklist must support later work in:

- RTA-USER
- RTA-PERSONA

## Step 4: Manual Confirmation Gate

Discovery never auto-starts RTA-USER.

After Discovery, always output:

- client type judgment
- evidence for the judgment
- whether the next stage should be `validated` or `inference_based`
- what is still missing

Then stop and wait for human confirmation.

## Output Rules

Always produce:

1. a human-readable Markdown result
2. a JSON result matching `templates/discovery-output.schema.json`

If file creation is appropriate, create:

```text
outputs/
├── discovery-diagnosis.md
├── discovery-interview-script.md
├── discovery-material-checklist.md
└── discovery-output.json
```

## Important Rules

- Do not ask validated-case questions to a zero-based client.
- Do not confuse guesses with facts.
- Mark inference-heavy sections clearly.
- Optimize for usable interview input, not for elegant theory.
- The purpose of this skill is to make later USER and PERSONA work reliable.
