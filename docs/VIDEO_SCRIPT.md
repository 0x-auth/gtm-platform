# Video Recording Script - GTM Platform Walkthrough
# Target: 8-12 minutes | Required structure per submission spec

---

## BEFORE YOU HIT RECORD

Open these tabs in browser (in order):
1. http://localhost:8000  (the app - start server first, see below)
2. https://github.com/0x-auth/gtm-platform  (GitHub README)
3. docs/architecture.md  (open in VS Code or browser)
4. File explorer / Finder showing the gtm-platform/ folder

Open these in terminal:
- One terminal tab with the server running
- One terminal tab ready for commands

### Start the server first:
```bash
cd /Users/abhissrivasta/github-repos-bitsabhi/gtm-platform
source .venv/bin/activate   # or: pip install -r requirements.txt
python -m uvicorn backbone.api:app --reload
```
Confirm you see: `Uvicorn running on http://127.0.0.1:8000`

---

## SEGMENT 1 — Architecture Overview (0:00 - 1:00)

**TAB: GitHub README → then docs/architecture.md**

Say:
> "This is the GTM Platform - an AI-native go-to-market system.
> The README shows the one-command bring-up, the API keys needed, and links to all docs."

**Show:** GitHub README - scroll slowly through the top, the bring-up section, the links.

Switch to docs/architecture.md, show the ASCII diagram. Point at each box and say:
> "Four layers: the Prospect UI at the top, FastAPI REST layer, the GTMAgent ReAct loop in the middle,
> and at the bottom the data model and integrations framework side by side.
> The agent never calls external APIs directly - everything goes through the integrations module."

**Terminal command to show repo structure:**
```bash
ls -la /Users/abhissrivasta/github-repos-bitsabhi/gtm-platform/
```
Say: "backbone, prospect, infra, docs, traces, tests, data - exactly the required structure."

---

## SEGMENT 2 — Data Model (1:00 - 2:00)

**TAB: docs/architecture.md - scroll to Data Model section**

Say:
> "Five tables: accounts, contacts, signals, opportunities, icp_profiles.
> Every row is scoped by account_id - that's how multi-tenancy works at the data layer."

**Show each table briefly** - accounts, contacts, signals, icp_profiles.

**Terminal - show the live seeded database:**
```bash
cd /Users/abhissrivasta/github-repos-bitsabhi/gtm-platform
python3 -c "
import sqlite3
conn = sqlite3.connect('data/gtm.db')
print('accounts:', conn.execute('SELECT COUNT(*) FROM accounts WHERE domain != \"personas.internal\"').fetchone()[0])
print('contacts:', conn.execute('SELECT COUNT(*) FROM contacts').fetchone()[0])
print('signals:', conn.execute('SELECT COUNT(*) FROM signals').fetchone()[0])
print('icp_profiles:', conn.execute('SELECT COUNT(*) FROM icp_profiles').fetchone()[0])
print()
print('Sample accounts:')
for r in conn.execute('SELECT name, domain, icp_score FROM accounts WHERE domain != \"personas.internal\" LIMIT 5').fetchall():
    print(f'  {r[0]} ({r[1]}) - ICP: {r[2]}')
"
```

Say: "10 companies seeded, 16 contacts, 21 signals, 2 ICP profiles - all loaded automatically on first run."

---

## SEGMENT 3 — Prospect Loop End-to-End (2:00 - 4:00)

**TAB: http://localhost:8000**

Say:
> "Now I'll run the Prospect loop live. I'll type rippling.com - one of the seeded accounts."

**Steps:**
1. Type `rippling.com` in the domain field
2. Leave send_to blank (so it drafts but doesn't send)
3. Click "Run Prospect Loop"
4. **Let it run - don't skip** - narrate while it runs:
   > "The agent is running step 1 - search_news, pulling recent signals from the web via Serper...
   > step 2 - search_contacts, finding decision makers on LinkedIn...
   > step 3 - score_icp, scoring this account against our ICP profile...
   > step 4 - save_contact, persisting the best contact to the database...
   > step 5 - draft_email, writing a personalized cold email using the signal it found."
5. When done, show the metrics cards: ICP score, contacts found, signals, steps
6. Scroll through the trace in the UI slowly

---

## SEGMENT 4 — Agent Traces (4:00 - 6:00)

**TAB: http://localhost:8000 (past traces) + Terminal**

Say:
> "Every agent run is saved as a full JSON trace. Let me open one."

**Terminal - show trace files:**
```bash
ls /Users/abhissrivasta/github-repos-bitsabhi/gtm-platform/traces/
```

**Open a trace and read through it:**
```bash
python3 -c "
import json
t = json.load(open('traces/trace_f0dd9437.json'))
for step in t:
    print(f\"[{step['type']}] {str(step.get('content', step.get('tool',''))[:120]}\")
    print()
" | head -60
```

Say while scrolling:
> "Here's the START - prospecting stripe.com.
> Then LLM step - the agent's THOUGHT: reasoning about what to do first.
> TOOL_CALL: search_news with args company=Stripe.
> OBSERVATION: the results come back - funding news, product launches.
> Then search_contacts... score_icp... save_contact... draft_email...
> And finally FINAL - the complete summary with the drafted email."

**Point out:** "Each step has a timestamp, type, content, and for tool calls - the exact args and the result. This is how you audit what the agent did and why."

---

## SEGMENT 5 — Integration (6:00 - 7:30)

**TAB: VS Code or terminal showing backbone/integrations.py**

```bash
cat /Users/abhissrivasta/github-repos-bitsabhi/gtm-platform/backbone/integrations.py
```

Say:
> "Two real integrations. Serper - one API key, one HTTP call, returns structured search results.
> Gmail - full OAuth2 flow, token refresh, sends real emails via Gmail API."

**Show the search function - point at the SERPER_KEY and the urlopen call with SSL context.**

Say:
> "The integrations module is pure functions - no database imports, no agent imports.
> The agent calls tools by name, the tool dispatcher in agent.py calls these functions.
> To add a third integration - say HubSpot - you add one function here, one elif in _call_tool,
> one line in the system prompt. No other files change."

**Show docs/integrations.md - scroll to "How to add the next integration" section.**

---

## SEGMENT 6 — What's Not Built + What's Next (7:30 - end)

**TAB: GitHub README - scroll to "What's built vs what's stubbed"**

Say:
> "Being honest about what's in iteration 1 and what's not."

Read the stubbed list:
> "Follow-up sequences - the opportunities.stage field exists but sequences table not built yet.
> Reply tracking - not implemented.
> CRM pipeline view - not built.
> Slack notifications - the integration pattern is documented but not wired."

**Switch to docs/architecture.md - scroll to "What the next iteration adds"**

Say:
> "Iteration 2 - Engage: sequences, reply tracking, follow-up scheduling.
> The data model already has opportunities.stage to support this - no schema rework needed.
> Iteration 3 - Manage: full CRM layer, pipeline views, Slack/Teams, webhooks."

**End with terminal - run the tests:**
```bash
cd /Users/abhissrivasta/github-repos-bitsabhi/gtm-platform
pytest tests/ -v 2>&1 | tail -20
```

Say: "26 tests - covering the data model, agent layer, and multi-tenancy isolation."

---

## QUICK REFERENCE - all commands in order

```bash
# Before recording - start server
cd /Users/abhissrivasta/github-repos-bitsabhi/gtm-platform
python -m uvicorn backbone.api:app --reload

# Segment 2 - show seeded data
python3 -c "
import sqlite3; conn = sqlite3.connect('data/gtm.db')
print('accounts:', conn.execute('SELECT COUNT(*) FROM accounts WHERE domain != \"personas.internal\"').fetchone()[0])
print('contacts:', conn.execute('SELECT COUNT(*) FROM contacts').fetchone()[0])
print('signals:', conn.execute('SELECT COUNT(*) FROM signals').fetchone()[0])
print('icp_profiles:', conn.execute('SELECT COUNT(*) FROM icp_profiles').fetchone()[0])
for r in conn.execute('SELECT name, domain, icp_score FROM accounts WHERE domain != \"personas.internal\" LIMIT 5').fetchall():
    print(f'  {r[0]} ({r[1]}) - ICP: {r[2]}')
"

# Segment 4 - list traces
ls traces/

# Segment 4 - read a trace
python3 -c "
import json
t = json.load(open('traces/trace_f0dd9437.json'))
for step in t:
    print(f\"[{step['type']}]\", str(step.get('content', step.get('tool','')))[:120])
    print()
" | head -60

# Segment 5 - show integrations
cat backbone/integrations.py

# Segment 6 - run tests
pytest tests/ -v 2>&1 | tail -20
```
