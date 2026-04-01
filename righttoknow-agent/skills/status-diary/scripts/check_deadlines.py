#!/usr/bin/env python3
"""
Check RTI Deadlines — RightToKnow Agent
Parses memory/MEMORY.md to find overdue RTI filings.

Usage:
  python3 check_deadlines.py --memory-file memory/MEMORY.md
"""

import argparse
import re
import sys
from datetime import datetime, timedelta


def parse_rti_table(content: str) -> list:
    """Parse RTI portfolio table from MEMORY.md."""
    entries = []
    in_table = False
    header_seen = False

    for line in content.split('\n'):
        line = line.strip()
        # Look for the table header
        if '| ID |' in line and 'Filed On' in line:
            in_table = True
            header_seen = True
            continue
        if header_seen and line.startswith('|---'):
            continue  # Skip separator row
        if in_table and line.startswith('|') and '|' in line[1:]:
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]  # Remove empty strings
            if len(parts) >= 6:
                try:
                    entry = {
                        'id': parts[0],
                        'filed_on': parts[1],
                        'authority': parts[2],
                        'subject': parts[3],
                        'due_by': parts[4],
                        'status': parts[5],
                        'notes': parts[6] if len(parts) > 6 else ''
                    }
                    if entry['id'].startswith('RTI-'):
                        entries.append(entry)
                except (IndexError, Exception):
                    pass
        elif in_table and not line.startswith('|'):
            if line and not line.startswith('#'):
                in_table = False

    return entries


def check_deadlines(entries: list) -> dict:
    """Check each entry for overdue status."""
    today = datetime.today()
    report = {
        'overdue': [],
        'due_soon': [],    # within 5 days
        'active': [],
        'resolved': [],
        'today': today.strftime('%Y-%m-%d')
    }

    for entry in entries:
        status = entry['status'].lower()
        due_str = entry['due_by']

        if 'resolved' in status or 'closed' in status:
            report['resolved'].append(entry)
            continue

        # Try to parse the due date
        due_date = None
        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
            try:
                due_date = datetime.strptime(due_str, fmt)
                break
            except ValueError:
                continue

        if due_date:
            days_remaining = (due_date - today).days
            entry['days_remaining'] = days_remaining

            if days_remaining < 0:
                entry['days_overdue'] = abs(days_remaining)
                report['overdue'].append(entry)
            elif days_remaining <= 5:
                report['due_soon'].append(entry)
            else:
                report['active'].append(entry)
        else:
            report['active'].append(entry)

    return report


def format_report(report: dict) -> str:
    lines = []
    lines.append(f"📋 RTI PORTFOLIO STATUS — {report['today']}")
    lines.append("=" * 50)

    if report['overdue']:
        lines.append(f"\n🔴 OVERDUE ({len(report['overdue'])} filing(s)):")
        for e in report['overdue']:
            lines.append(
                f"  {e['id']} | {e['authority']} | {e['subject']}"
            )
            lines.append(
                f"       Was due: {e['due_by']} ({e.get('days_overdue',0)} days ago)"
            )
            lines.append(f"       Status: {e['status']}")
            lines.append(f"       ACTION: File First Appeal immediately → appeal-wizard skill")

    if report['due_soon']:
        lines.append(f"\n🟡 DUE SOON ({len(report['due_soon'])} filing(s)):")
        for e in report['due_soon']:
            lines.append(
                f"  {e['id']} | {e['authority']} | {e['subject']}"
            )
            lines.append(
                f"       Due: {e['due_by']} ({e.get('days_remaining',0)} days left)"
            )

    if report['active']:
        lines.append(f"\n🟢 ACTIVE ({len(report['active'])} filing(s)):")
        for e in report['active']:
            lines.append(
                f"  {e['id']} | {e['authority']} | {e['subject']}"
                + (f" — {e.get('days_remaining','?')} days left" if 'days_remaining' in e else "")
            )

    if report['resolved']:
        lines.append(f"\n✅ RESOLVED: {len(report['resolved'])} filing(s)")

    total = len(report['overdue']) + len(report['due_soon']) + len(report['active']) + len(report['resolved'])
    lines.append(f"\nTotal tracked: {total}")

    if not report['overdue'] and not report['due_soon'] and not report['active']:
        lines.append("\nNo active filings. Use rti-drafter to start your first RTI!")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check RTI filing deadlines")
    parser.add_argument("--memory-file", default="memory/MEMORY.md",
                        help="Path to MEMORY.md file")
    args = parser.parse_args()

    try:
        with open(args.memory_file, encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Memory file not found: {args.memory_file}")
        print("No active RTI filings tracked yet.")
        sys.exit(0)

    entries = parse_rti_table(content)
    report = check_deadlines(entries)
    print(format_report(report))


if __name__ == "__main__":
    main()
