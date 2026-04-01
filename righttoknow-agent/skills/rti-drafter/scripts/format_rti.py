#!/usr/bin/env python3
"""
RTI Letter Formatter — RightToKnow Agent
Generates a formatted RTI application from structured JSON input.

Usage:
  echo '{"applicant_name": "Ramesh Kumar", ...}' | python3 format_rti.py
  python3 format_rti.py --file input.json
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path


def format_rti_application(data: dict) -> str:
    """Generate a complete, formatted RTI application letter."""

    today = datetime.today().strftime("%d/%m/%Y")
    date = data.get("date", today)

    # Use `or default` pattern to handle both missing keys AND explicit None values
    applicant_name = data.get("applicant_name") or "[APPLICANT NAME]"
    applicant_address = data.get("applicant_address") or "[APPLICANT ADDRESS]"
    applicant_city = data.get("applicant_city") or "[CITY]"
    applicant_state = data.get("applicant_state") or "[STATE]"
    applicant_pin = str(data.get("applicant_pin") or "[PIN CODE]")
    applicant_phone = data.get("applicant_phone") or ""
    applicant_email = data.get("applicant_email") or ""

    authority_name = data.get("authority_name") or "[PUBLIC AUTHORITY NAME]"
    authority_address = data.get("authority_address") or "[AUTHORITY ADDRESS]"
    cpio_designation = data.get("cpio_designation") or "Central/State Public Information Officer"

    subject = data.get("subject") or "Application under the Right to Information Act, 2005"
    is_bpl = bool(data.get("is_bpl", False))
    bpl_card_number = data.get("bpl_card_number") or ""
    is_life_liberty = bool(data.get("is_life_liberty", False))
    fee_mode = data.get("fee_mode") or "Indian Postal Order"
    reference_details = data.get("reference_details") or []
    questions_raw = data.get("questions") or []
    questions = [str(q) for q in questions_raw] if questions_raw else ["[STATE YOUR INFORMATION REQUEST HERE]"]

    lines = []

    lines.append(f"Date: {date}")
    lines.append("")
    lines.append("To,")
    lines.append(f"The {cpio_designation},")
    lines.append(authority_name)
    lines.append(authority_address)
    lines.append("")
    lines.append(f"Subject: {subject}")
    lines.append("")
    lines.append("Respected Sir/Madam,")
    lines.append("")

    intro = (
        f"I, {applicant_name}, a citizen of India, hereby submit this application "
        f"under Section 6(1) of the Right to Information Act, 2005, and respectfully "
        f"request the following information:"
    )
    lines.append(intro)
    lines.append("")

    if is_life_liberty:
        lines.append("⚠ URGENT — LIFE/LIBERTY MATTER: Pursuant to the proviso to Section 7(1)")
        lines.append("of the RTI Act 2005, this matter concerns life or personal liberty.")
        lines.append("A response is required within 48 HOURS of receipt of this application.")
        lines.append("")

    for i, question in enumerate(questions, 1):
        lines.append(f"{i}. {question}")
    lines.append("")

    if reference_details:
        lines.append("Reference Details:")
        for detail in reference_details:
            lines.append(f"  - {detail}")
        lines.append("")

    lines.append(
        "Additionally, if any part of this information is withheld, I request that you "
        "please cite the specific provision of Section 8 or Section 9 of the RTI Act, "
        "2005 applicable to each withheld item, along with the reasons for such exemption."
    )
    lines.append("")

    if is_bpl:
        lines.append(
            f"I am a Below Poverty Line (BPL) cardholder bearing card number {bpl_card_number or '[BPL CARD NUMBER]'}, "
            f"and am therefore exempt from paying the application fee under Section 7(5) of the RTI Act, 2005."
        )
    else:
        lines.append(
            f"I am enclosing a fee of ₹10/- (Rupees Ten only) as the prescribed application "
            f"fee, payable by {fee_mode}."
        )
    lines.append("")

    lines.append(
        "I request you to provide the said information within 30 days as mandated under "
        "Section 7(1) of the Right to Information Act, 2005. In case this application is "
        "transferred to another public authority under Section 6(3), I request prior "
        "intimation of the same."
    )
    lines.append("")
    lines.append("I hereby declare that this is a bona fide request for information.")
    lines.append("")
    lines.append("Thanking you,")
    lines.append("")
    lines.append("Yours faithfully,")
    lines.append("")
    lines.append(applicant_name)
    lines.append(applicant_address)
    lines.append(f"{str(applicant_city)}, {str(applicant_state)} - {str(applicant_pin)}")

    if applicant_phone:
        lines.append(f"Phone: {applicant_phone}")
    if applicant_email:
        lines.append(f"Email: {applicant_email}")

    lines.append(f"Date: {date}")
    lines.append("")
    lines.append("─" * 70)
    lines.append("IMPORTANT NOTES:")
    lines.append(
        "1. Keep a photocopy of this application and payment proof before submitting."
    )
    lines.append(
        "2. The authority must respond within 30 days (or 48 hours for life/liberty matters)."
    )
    lines.append(
        "3. If no response in 30 days, you may file a First Appeal under Section 19(1)."
    )
    lines.append(
        "4. This document was prepared with informational assistance. "
        "It does not constitute legal advice. For complex legal matters, "
        "consult a licensed advocate."
    )
    lines.append("─" * 70)

    return "\n".join(str(line) for line in lines)


def main():
    parser = argparse.ArgumentParser(description="Format RTI application letter")
    parser.add_argument("--file", help="Input JSON file path")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    else:
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError:
            data = {}

    letter = format_rti_application(data)

    if args.output:
        # Security: resolve path and ensure it stays within safe boundaries
        from pathlib import Path as _P
        out_path = _P(args.output).resolve()
        # Allow writes to /tmp, /home, current dir, or relative paths under workspace
        safe = (
            str(out_path).startswith("/tmp") or
            str(out_path).startswith("/home") or
            "workspace" in str(out_path) or
            not str(out_path).startswith("/")
        )
        if not safe:
            print(f"⚠ Output path restricted for safety. Writing to: workspace/rti-output.txt")
            out_path = _P("workspace/rti-output.txt")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(letter)
        print(f"✅ RTI application saved to: {out_path}")
    else:
        print(letter)


if __name__ == "__main__":
    main()
