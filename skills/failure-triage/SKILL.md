# Skill: Failure Triage
## Purpose
Triage test failures from logs and observed behavior.
## Procedure
1. Extract timestamps, error codes, stack traces, correlation IDs and environment clues.
2. Classify likely domain: functional, data, environment, integration, authentication or test automation.
3. Separate observed facts from hypotheses.
4. Rank hypotheses by evidence and impact.
5. Recommend the next diagnostic checks and missing information.
## Guardrails
Never present a hypothesis as a confirmed root cause. Do not fabricate log evidence or claim a fix.
