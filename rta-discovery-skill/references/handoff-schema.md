# Handoff Schema

Discovery should hand off only after manual confirmation.

## Required handoff fields

- client_type
- confidence
- evidence_summary
- interview_path_used
- materials_collected
- missing_items
- recommended_next_mode
- manual_confirmation_required

## Recommended next mode

Use one of:

- `validated`
- `inference_based`
- `hold_for_more_material`

## Manual Confirmation

Before RTA-USER starts, a human must confirm:

1. the classification is acceptable
2. the interview direction is acceptable
3. the material set is enough
4. inference-based output is acceptable if the client is zero-based
