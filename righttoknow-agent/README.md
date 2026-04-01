# RightToKnow — AI-Powered RTI Filing Assistant

> *"The right to seek information is the foundation of all other rights."*
> — Aruna Roy, RTI Movement Pioneer

An AI agent built on the **gitagent standard** that empowers 1.4 billion Indian citizens to exercise their **Right to Information Act 2005** rights — turning legal confusion into clear, ready-to-file government applications.

**GitAgent Hackathon 2026 Submission** | Built with [gitagent](https://github.com/open-gitagent/gitagent) + [gitclaw](https://github.com/open-gitagent/gitclaw)

---

## The Problem

India's RTI Act 2005 is one of the world's most powerful transparency laws. Every citizen has the legal right to demand information from any government authority within 30 days. Yet:

- **40% of RTIs are rejected on technicalities** — wrong section cited, vague questions, wrong authority
- **60% of citizens never follow up** after no response — appeal deadlines lapse unnoticed
- **Rural and semi-urban citizens** have near-zero RTI literacy despite needing it most
- **The cost of a lawyer** to help file RTI defeats the purpose of a free democratic right

**RightToKnow solves all four problems in under 60 seconds.**

---

## Quick Start

```bash
# Prerequisites: Node.js >= 20, Python 3.8+
npm install -g gitclaw

# Clone the agent
git clone https://github.com/yourusername/righttoknow-agent.git
cd righttoknow-agent

# Set your API key (supports Claude, GPT-4, Gemini)
export ANTHROPIC_API_KEY="sk-ant-..."

# Run the agent
gitclaw --dir . "My EPFO pension of Rs 2.5 lakhs is stuck for 6 months. My name is Ramesh Kumar, Jaipur, Rajasthan."
```

**What happens in < 60 seconds:**
1. Authority identified → EPFO Regional Office, Jaipur (Central Government)
2. Python script queries authority database → correct CPIO details
3. 5-6 legally precise questions drafted automatically
4. RTI letter formatted and saved → `workspace/rti-epfo-pension-2026-03-30.txt`
5. Step-by-step filing instructions provided (rtionline.gov.in)
6. RTI-001 recorded in git-committed memory with 30-day deadline alert

---

## Live Demo

```bash
# Quick validation + script tests (no API key needed)
./demo.sh quick

# Run 5 real RTI scenarios end-to-end
./demo.sh scenario 1    # EPFO pension delay
./demo.sh scenario 2    # Passport not issued
./demo.sh scenario 3    # Income tax refund stuck
./demo.sh scenario 4    # First appeal (RTI ignored after 42 days)
./demo.sh scenario 5    # Ration card delay (state RTI)

# Custom prompt
./demo.sh custom "My municipal water connection was disconnected 3 months ago without notice"
```

---

## Agent Architecture

```
righttoknow-agent/
│
├── agent.yaml              ← Manifest: model, skills, runtime, tags
├── SOUL.md                 ← Identity: civic activist, not a chatbot
├── RULES.md                ← Hard constraints: accuracy, no PII storage, no legal advice
├── AGENTS.md               ← Framework-agnostic fallback instructions
│
├── skills/                 ← 4 focused, documented capabilities
│   ├── rti-drafter/        ← Draft complete RTI applications
│   │   ├── SKILL.md        ← Full instructions with format templates and edge cases
│   │   └── scripts/
│   │       └── format_rti.py     ← Python: formats letter (BPL, life/liberty, normal)
│   │
│   ├── authority-mapper/   ← Map any problem to the correct CPIO
│   │   ├── SKILL.md        ← Central vs State decision logic, 18+ authority mappings
│   │   └── scripts/
│   │       └── find_authority.py ← Python: keyword-based authority database
│   │
│   ├── appeal-wizard/      ← Draft Section 19(1) and 19(3) appeals
│   │   ├── SKILL.md        ← When to appeal, strongest grounds, CIC/SIC addresses
│   │   └── scripts/
│   │       └── format_appeal.py  ← Python: complete first + second appeal letters
│   │
│   └── status-diary/       ← Track RTI portfolio in git memory
│       └── SKILL.md        ← Portfolio management, overdue alerts, session protocol
│
├── knowledge/              ← 5-document knowledge base (3 always-loaded)
│   ├── index.yaml                   ← gitclaw knowledge index
│   ├── rti-act-key-sections.md      ← Sections 2,3,4,6,7,8,11,19,20 with practicals
│   ├── state-portals-and-fees.md    ← 15+ state portals, fees, SIC contacts
│   ├── central-authorities.md       ← 12+ central department CPIO reference
│   ├── common-rejection-reasons.md  ← Top 10 rejections + legal counter-arguments
│   └── effective-rti-strategies.md  ← Insider strategies for success
│
├── tools/
│   ├── letter-formatter.yaml   ← MCP-compatible: generates RTI letters
│   └── authority-lookup.yaml   ← MCP-compatible: looks up CPIOs
│
├── workflows/
│   └── rti-complete-workflow.yaml  ← 6-step end-to-end filing workflow
│
├── memory/
│   ├── MEMORY.md            ← Git-committed RTI portfolio tracker
│   └── memory.yaml          ← Memory layer config
│
├── examples/
│   ├── good-outputs.md      ← Calibration: ideal agent responses
│   └── bad-outputs.md       ← Calibration: what to avoid
│
├── compliance/
│   └── risk-assessment.md   ← Risk tier: Low (civic empowerment only)
│
├── workspace/               ← All generated RTI applications saved here
│   ├── demo-rti-epfo-pension-2026-03-29.txt
│   └── demo-rti-passport-2026-03-29.txt
│
└── demo.sh                  ← Interactive demo with 5 RTI scenarios
```

---

## Skills

### `rti-drafter` (Core Skill)
Converts citizen complaints into specific, legally answerable RTI questions. Uses `format_rti.py` to generate complete letters. Handles: normal RTIs, BPL fee-exempt applicants, life/liberty 48-hour urgent matters, third-party information requests.

### `authority-mapper`
The most critical pre-filing step. Maps 14 categories of citizen problems to the correct Central/State authority with HIGH confidence. Prevents the #1 RTI mistake: sending to the wrong department and wasting 30 days.

### `appeal-wizard`
When RTIs are ignored or rejected, this skill drafts Section 19(1) First Appeals (30-day deadline) and Section 19(3) Second Appeals to the Central/State Information Commission (90-day deadline). Automatically selects the strongest grounds based on the rejection type.

### `status-diary`
Persistent RTI portfolio tracker using gitclaw's git-committed memory. Tracks filing dates, due dates, status transitions (Filed → Overdue → Appealed → Resolved), and surfaces follow-up alerts at session start.

---

## Technical Details

| Component | Choice | Why |
|-----------|--------|-----|
| Agent Standard | gitagent v0.1.0 | Framework-agnostic, portable |
| Runtime | gitclaw SDK | Python support, git memory, multi-model |
| Model | Claude Sonnet 4.5 | Best balance of legal reasoning + speed |
| Fallback | Claude Haiku 4.5 | Fast, cost-efficient for simple queries |
| Scripts | Python 3.8+ stdlib | Zero external dependencies, runs everywhere |
| Knowledge | Markdown + YAML index | Always-loaded for instant access |
| Memory | Git-committed Markdown | Full history, diff-able, portable |

### Multi-Model Support

```bash
# Claude (default — best for legal language)
gitclaw --dir . --model anthropic:claude-sonnet-4-5-20250929 "Help me file RTI"

# GPT-4o
gitclaw --dir . --model openai:gpt-4o "Help me file RTI"

# Gemini
gitclaw --dir . --model google:gemini-2.0-flash "Help me file RTI"
```

### Export for Other Frameworks

```bash
npx gitagent validate --dir .          # Validate against spec
npx gitagent info --dir .              # Agent summary
npx gitagent export --format system-prompt --dir .   # System prompt preview
npx gitagent export --format claude-code --dir .     # Claude Code export
npx gitagent export --format cursor --dir .          # Cursor export
```

---

## Example Output

Given input: *"EPFO pension of Rs 2.5 lakhs pending for 6 months, Jaipur"*

The agent generates `workspace/rti-epfo-pension-2026-03-30.txt`:

```
Date: 30/03/2026

To,
The Regional Provident Fund Commissioner (RTI),
Employees' Provident Fund Organisation, Regional Office
Bhavishya Nidhi Bhawan, Sector 10, Jaipur - 302033

Subject: Status of EPS-95 Pension Claim — UAN 100XXXXXXXXX

Respected Sir/Madam,

I, Ramesh Kumar, a citizen of India, hereby submit this application under
Section 6(1) of the Right to Information Act, 2005...

1. Provide the current status of pension claim bearing UAN 100XXXXXXXXX...
2. State the name and designation of the officer currently handling this claim...
3. Provide certified copies of all noting sheets and file movement records...
4. State the specific provision under which payment was delayed beyond 90 days...
5. State whether employer contributions are fully deposited till date...

[Full formatted letter with legal disclaimers, fee info, section citations]
```

---

## Real-World Impact

| Metric | Value |
|--------|-------|
| RTIs filed annually in India | ~6 million |
| Rejection rate (technicalities) | ~40% |
| Citizens who never follow up | ~60% |
| Average RTI filing time (manual) | 2-4 hours |
| With RightToKnow | < 60 seconds |

**RightToKnow doesn't replace lawyers. It fills the enormous gap between having a right and knowing how to use it.**

---

## Why This Agent is Different

Most AI projects in civic tech are chatbots that explain government processes. RightToKnow **does the work** — it produces actual, submission-ready legal documents. The difference between telling someone how to file an RTI and handing them a filed RTI is the difference between a tutorial and a tool.

The agent lives in a git repo. Its knowledge is version-controlled. Its memory is git-committed. Every RTI it helps file is a tiny act of democracy — and every session builds on the last.

---

## License

MIT — fork it, adapt it, deploy it for your state's citizens.

---

## Disclaimer

This agent provides informational assistance under the Right to Information Act, 2005 (India). It does not constitute legal advice. For complex legal matters, consult a licensed advocate registered with the Bar Council of India.

---

*Built on the gitagent open standard. Your agent is a git repo. Make it count.*
