# Agentic QA Hub

A local-first AI-assisted QA workbench with three specialized agents:
1. **Test Designer** — analyzes requirements and drafts scenarios/test cases.
2. **Failure Analyzer** — triages test failures and suggests evidence-based hypotheses.
3. **Evidence Generator** — consolidates requirements, tests and execution results into reports.

Includes a coordinating workflow, human review states, audit events, CSV/JSON imports, PDF/Excel/HTML exports, editable skill files, and an optional Anthropic provider. The default `local` provider works without an API key.

> This is a demonstrator/MVP, not a SOC 2 or PIPEDA certification or a production compliance guarantee. Use synthetic data until your organization has approved the model, retention, access and data-processing controls.

## Requirements
- Python 3.10+
- VS Code (recommended)
- Optional: Anthropic API key for model-assisted generation

## Run on Windows (PowerShell)
```powershell
cd agentic-qa-hub
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

## Run on macOS/Linux
```bash
cd agentic-qa-hub
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Optional Claude integration
1. Put your Anthropic key in `.env` as `ANTHROPIC_API_KEY`.
2. Set `AI_PROVIDER=anthropic`.
3. Restart the server.
4. Do not submit client confidential or personal data unless your organization's policies and contractual controls explicitly permit it.

## Demo workflow
1. Open **Test Design** and paste a user story.
2. Generate scenarios and inspect each result.
3. Mark scenarios approved/rejected in **Review Queue**.
4. Open **Failure Triage**, paste a test log, and review the hypotheses.
5. Open **Evidence & Reports** and export HTML, PDF or Excel.
6. Use **Audit Log** to inspect recorded actions.

## Project structure
```text
app/
  main.py                 FastAPI routes and static UI hosting
  core/                   configuration, storage, audit, AI provider
  agents/                 three agents and orchestrator
  models/                 Pydantic schemas
  services/               export services
  static/                 dashboard UI
skills/                   editable agent skill instructions
.github/agents/           GitHub Copilot custom-agent profiles
.claude/skills/           Claude Code skill definitions
tests/                    automated tests
data/                     local JSON persistence
```

## Safety / human review
- AI outputs are drafts, not approved test evidence.
- Human approval is explicit and recorded.
- Failure analysis labels root causes as hypotheses, not facts.
- Local provider uses deterministic heuristics; Anthropic provider sends prompts to Anthropic.
- Audit log stores action metadata. Avoid logging secrets or raw client payloads.
- For production, add SSO, RBAC, encrypted database, secrets management, retention/deletion policies, DLP, tenant isolation, monitoring, threat modeling and formal security/privacy review.

## GitHub
```bash
git init
git add .
git commit -m "Initial Agentic QA Hub"
git branch -M main
git remote add origin https://github.com/YOUR-USER/agentic-qa-hub.git
git push -u origin main
```

## API endpoints
- `GET /api/health`
- `GET /api/dashboard`
- `POST /api/test-design`
- `POST /api/failure-triage`
- `POST /api/evidence`
- `GET /api/reviews`
- `POST /api/reviews/{item_id}`
- `GET /api/audit`
- `GET /api/reports/{format}` where format is `html`, `pdf`, or `xlsx`

## Tests
```bash
pytest
```
