---
name: status-diary
description: "Tracks and manages the user's RTI filing portfolio across sessions. Records filed RTIs, updates their status (pending/appealed/resolved), stores outcomes, and surfaces overdue follow-ups. Use at the end of every RTI session to record what was filed, and at the start of sessions to check what needs follow-up."
license: MIT
allowed-tools: Bash Read Write
metadata:
  author: righttoknow-project
  version: "1.0.0"
  category: civic-tech
---

# Status Diary — RTI Portfolio Tracker

## Purpose

Every citizen who fights for transparency deserves a record of their victories and an alert when follow-up is needed. The status diary is your RTI logbook, persisted in git-committed memory across sessions.

## Check Deadlines at Session Start

Run this script at the beginning of every session to surface overdue filings:

```bash
python3 skills/status-diary/scripts/check_deadlines.py --memory-file memory/MEMORY.md
```

Example output:
```
📋 RTI PORTFOLIO STATUS — 2026-04-05
==================================================
🔴 OVERDUE (1 filing):
  RTI-002 | JVVNL Jaipur | Meter replacement
       Was due: 2026-04-04 (1 day ago)
       Status: Awaiting Response
       ACTION: File First Appeal immediately → appeal-wizard skill

🟢 ACTIVE (2 filings):
  RTI-001 | EPFO | Pension claim — 23 days left
  RTI-003 | Income Tax | TDS refund — 15 days left

Total tracked: 3
```

## Memory Format

The RTI diary is stored in `memory/MEMORY.md`. Each entry follows this structure:

```markdown
## RTI Portfolio

### Active Filings

| ID | Filed On | Authority | Subject | Due By | Status | Notes |
|----|----------|-----------|---------|--------|--------|-------|
| RTI-001 | 2026-03-29 | EPFO | Pension claim delay | 2026-04-28 | Awaiting Response | |
| RTI-002 | 2026-03-15 | JVVNL | Meter replacement | 2026-04-14 | First Appeal Filed | No response to RTI |
| RTI-003 | 2026-02-01 | Income Tax | TDS correction | RESOLVED | Resolved 2026-03-10 | Got refund |
```

## Operations

### Add New Filing

When a new RTI application is drafted and ready to submit, add it to the diary:

1. Assign a sequential ID: RTI-001, RTI-002, etc.
2. Record: filing date, authority name (short), subject (3-5 words), due date (30 days from today)
3. Set status to "Ready to File"
4. Save using the `memory` tool: action="save", content=[updated MEMORY.md content]

### Status Transitions

| Status | Meaning | Next Action |
|--------|---------|-------------|
| Ready to File | Document generated, not yet submitted | File it today |
| Filed | Submitted to authority | Wait 30 days |
| Awaiting Response | Within 30-day window | Monitor |
| Overdue | 30+ days, no response | File First Appeal NOW |
| First Appeal Filed | Section 19(1) filed | Wait 30 days |
| First Appeal Overdue | No FAA decision in 30 days | File Second Appeal |
| Second Appeal Filed | Section 19(3) at CIC/SIC | Wait for hearing |
| Partially Resolved | Some info received | Follow up on remainder |
| Resolved | Complete, satisfactory response | Move to resolved section |
| Closed | User chose to stop | Archive |

### Update Memory

To update an RTI's status, load the current memory, modify the table entry, and save:

```
Load memory → Find the RTI row → Update the Status cell → Save memory
```

Use the `memory` tool with:
- action: "load" → to read current state
- action: "save" → to write updated state (with message like "Update RTI-002 to First Appeal Filed")

## Session Start Protocol

1. Run: `python3 skills/status-diary/scripts/check_deadlines.py --memory-file memory/MEMORY.md`
2. Report overdue filings to the user immediately
3. Ask if any status updates are needed before proceeding

## Session End Protocol

After every session where an RTI was filed or updated:
1. Confirm with user that they plan to submit (or have already submitted)
2. Add/update the entry in the diary
3. Calculate the 30-day due date: filing_date + 30 days
4. Save memory with a descriptive commit message

## Privacy Rules

NEVER store in memory:
- Aadhaar numbers, PAN numbers, bank account numbers
- Medical records or health conditions
- Details about third parties not the user
- Any financial amounts beyond general reference (e.g., "pension claim" not exact rupee amount)

STORE only: RTI ID, authority name, general subject (3-5 words), dates, status, outcome notes.
