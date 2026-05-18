# GTM Platform - AI-Native Go-to-Market

An AI-native platform that automates the full prospect loop: research a company, find decision makers, score ICP fit, draft personalized outreach, and send via Gmail - all driven by an autonomous agent.

## What this is

Sales reps spend 70% of their time on non-selling work: researching accounts, finding contacts, writing emails, updating the CRM. This platform builds the operating layer underneath - a unified data model (accounts, contacts, opportunities, signals) with an agent orchestration layer that does the research and outreach automatically.

## External API keys needed

| Key | Purpose | Get it at |
|-----|---------|-----------|
| `ANTHROPIC_API_KEY` | Claude Haiku for agent reasoning | console.anthropic.com |
| `SERPER_API_KEY` | Google Search via Serper for news + contact discovery | serper.dev |

Gmail OAuth credentials are optional (for real email sending). Without them, the agent drafts emails but does not send.

## One-command bring-up

```bash
# Clone and set keys
git clone <repo>
cd gtm-platform
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY and SERPER_API_KEY

# Docker (recommended)
docker compose -f infra/docker-compose.yml up

# OR local Python 3.11+
pip install -r requirements.txt
python -m uvicorn backbone.api:app --reload
```

Open http://localhost:8000

## How to run the Prospect loop

1. Open http://localhost:8000
2. Type a company domain (e.g. `stripe.com`)
3. Optionally add an email address to send outreach to
4. Click "Run Prospect Loop"
5. Watch the agent reasoning trace in real time

The agent runs 6 steps in order:
1. `search_news` - pulls recent signals from the web via Serper
2. `search_contacts` - finds decision makers on LinkedIn via Serper
3. `score_icp` - scores the account against the ICP profile (0.0-1.0)
4. `save_contact` - persists the best contact to the database
5. `draft_email` - writes a personalized cold email using the signal found
6. ANSWER - summarizes the full prospect run

## Seeded demo environment

On first run the platform auto-seeds two accounts:
- **Rippling** (rippling.com) - ICP score 0.92, 3 contacts, 4 signals
- **Linear** (linear.app) - ICP score 0.87, 2 contacts, 3 signals

Reviewers can immediately run the Prospect loop on these or any new domain.

## Repository map

```
/backbone   - platform backbone (data model, agent, integrations framework)
/prospect   - vertical slice UI (dark theme, trace viewer)
/infra      - Docker + compose
/docs       - architecture, agent design, integration docs
/traces     - saved agent execution traces
/tests      - automated integration tests
/data       - seeded demo data (SQLite)
README.md
```

## Running tests

```bash
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

## What's deliberately not built

- No mock data - every Serper call hits the real API
- No fake LLM responses - every agent step uses real Claude Haiku
- No hardcoded email templates - the agent drafts each email from the actual signal it found
- Multi-tenancy via `account_id` isolation at the DB layer (every table foreign-keys to accounts)

## Links

- Architecture: [docs/architecture.md](docs/architecture.md)
- Agent design: [docs/agents.md](docs/agents.md)
- Integrations: [docs/integrations.md](docs/integrations.md)
