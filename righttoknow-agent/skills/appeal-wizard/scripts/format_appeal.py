#!/usr/bin/env python3
"""
Appeal Formatter — RightToKnow Agent
Generates complete First Appeals (Section 19(1)) and Second Appeals (Section 19(3)).

Usage:
  echo '{"appeal_type": "first", ...}' | python3 format_appeal.py
  python3 format_appeal.py --file input.json --output appeal.txt
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path


def format_first_appeal(data: dict) -> str:
    today = datetime.today().strftime("%d/%m/%Y")
    date = data.get("date", today)

    applicant_name = data.get("applicant_name") or "[APPLICANT NAME]"
    applicant_address = data.get("applicant_address") or "[APPLICANT ADDRESS]"
    appellate_authority_name = data.get("appellate_authority_name") or "[FIRST APPELLATE AUTHORITY NAME]"
    appellate_authority_address = data.get("appellate_authority_address") or "[FAA ADDRESS]"
    authority_name = data.get("authority_name") or "[PUBLIC AUTHORITY]"
    rti_date = data.get("rti_date") or "[RTI DATE]"
    rti_subject = data.get("rti_subject") or "[SUBJECT]"
    rti_reference = data.get("rti_reference") or ""
    response_status = data.get("response_status") or "no_response"
    days_elapsed = int(data.get("days_elapsed") or 30)
    response_date = data.get("response_date") or ""
    rejection_grounds = data.get("rejection_grounds") or ""
    unanswered_questions = data.get("unanswered_questions") or ""
    custom_grounds = data.get("grounds") or []

    lines = []
    lines.append(f"Date: {date}")
    lines.append("")
    lines.append("To,")
    lines.append("The First Appellate Authority,")
    lines.append(appellate_authority_name)
    lines.append(appellate_authority_address)
    lines.append("")
    lines.append("Subject: First Appeal under Section 19(1) of the Right to Information Act, 2005")
    lines.append(f"         — against the order/non-response of the CPIO, {authority_name}")
    lines.append("")
    lines.append("Respected Sir/Madam,")
    lines.append("")
    lines.append(
        f"I, {applicant_name}, a citizen of India, hereby file this First Appeal under "
        f"Section 19(1) of the Right to Information Act, 2005."
    )
    lines.append("")
    lines.append("1. DETAILS OF ORIGINAL RTI APPLICATION:")
    lines.append(f"   a. Date of RTI application: {rti_date}")
    lines.append(f"   b. Filed with: The CPIO, {authority_name}")
    lines.append(f"   c. Subject of application: {rti_subject}")
    if rti_reference:
        lines.append(f"   d. Registration/Reference Number: {rti_reference}")
    lines.append("")

    lines.append("2. STATUS OF RESPONSE:")
    if response_status == "no_response":
        lines.append(
            f"   No response has been received as of this date. {days_elapsed} days have elapsed "
            f"since the RTI application was filed. This constitutes a deemed refusal under "
            f"Section 7(2) of the RTI Act, 2005, as the statutory 30-day period under "
            f"Section 7(1) has lapsed."
        )
    elif response_status == "rejected":
        lines.append(
            f"   A response was received on {response_date} refusing the information. "
            f"The grounds cited were: \"{rejection_grounds}\""
        )
    elif response_status == "incomplete":
        lines.append(
            f"   A partial response was received on {response_date}. "
            f"Questions {unanswered_questions} from the original application remain unanswered."
        )
    else:
        lines.append(
            f"   The CPIO's response was unsatisfactory. Response received: {response_date}."
        )
    lines.append("")

    lines.append("3. GROUNDS OF APPEAL:")
    if custom_grounds:
        for i, ground in enumerate(custom_grounds, 1):
            lines.append(f"   {i}. {ground}")
    else:
        # Default grounds based on response_status
        grounds = []
        if response_status == "no_response":
            grounds.append(
                "The CPIO failed to respond within the mandatory 30-day period prescribed under "
                "Section 7(1) of the RTI Act, 2005. This non-response amounts to deemed refusal "
                "under Section 7(2)."
            )
        if response_status == "rejected":
            grounds.append(
                "The information sought does not fall within any of the exemptions enumerated "
                "under Section 8(1) of the RTI Act, 2005. The claim of exemption is erroneous."
            )
            grounds.append(
                "The CPIO has not provided reasons in writing for the refusal as mandated under "
                "Section 7(8) of the RTI Act, 2005, which requires the CPIO to communicate "
                "reasons for any rejection, the period of appeal, and the appellate authority's particulars."
            )
        grounds.append(
            "The information sought pertains to a public authority's discharge of its statutory "
            "duties and is clearly a matter of public interest. There is no reasonable basis to "
            "withhold this information from a citizen."
        )
        grounds.append(
            "Under Section 19(5) of the RTI Act, 2005, the burden of proving that refusal "
            "of the request was justified lies with the CPIO."
        )
        for i, g in enumerate(grounds, 1):
            lines.append(f"   {i}. {g}")
    lines.append("")

    lines.append("4. RELIEF SOUGHT:")
    lines.append(
        "   This Appellate Authority is respectfully prayed to:"
    )
    lines.append(
        "   a. Direct the CPIO to furnish the complete information sought within 7 days;"
    )
    lines.append(
        "   b. Impose a penalty on the CPIO under Section 20(1) of the RTI Act, 2005 "
        "for wrongful refusal/delay (Rs 250 per day up to Rs 25,000);"
    )
    lines.append(
        "   c. Award appropriate compensation to the undersigned for the detriment "
        "suffered due to delay, under Section 19(8)(b) of the RTI Act, 2005."
    )
    lines.append("")
    lines.append("5. DECLARATION:")
    lines.append(
        "   I declare that the facts stated in this First Appeal are true and correct "
        "to the best of my knowledge and belief, and that this appeal is filed in good faith."
    )
    lines.append("")
    lines.append("Thanking you,")
    lines.append("")
    lines.append("Yours faithfully,")
    lines.append("")
    lines.append(applicant_name)
    lines.append(applicant_address)
    lines.append(f"Date: {date}")
    lines.append("")
    lines.append("Enclosures:")
    lines.append("  1. Copy of original RTI application with proof of submission")
    lines.append("  2. Acknowledgement / dispatch proof of RTI application")
    if response_status != "no_response":
        lines.append("  3. Copy of CPIO's response")
    lines.append("")
    lines.append("─" * 60)
    lines.append("NEXT STEPS:")
    lines.append(
        "  • If this First Appeal is not decided within 30 days, file a Second Appeal"
    )
    lines.append(
        "    with the Central Information Commission at: cic.gov.in/secondappeal"
    )
    lines.append(
        "  • For state matters, file Second Appeal with the State Information Commission"
    )
    lines.append("")
    lines.append("This appeal is filed under the Right to Information Act, 2005.")
    lines.append("Informational assistance only. This is not legal advice.")
    lines.append("Consult a licensed advocate for complex legal matters.")
    lines.append("─" * 60)

    return "\n".join(str(line) for line in lines)


def format_second_appeal(data: dict) -> str:
    today = datetime.today().strftime("%d/%m/%Y")
    date = data.get("date", today)

    applicant_name = data.get("applicant_name", "[APPLICANT NAME]")
    applicant_address = data.get("applicant_address", "[APPLICANT ADDRESS]")
    authority_name = data.get("authority_name", "[PUBLIC AUTHORITY]")
    rti_date = data.get("rti_date", "[RTI DATE]")
    rti_subject = data.get("rti_subject", "[SUBJECT]")
    rti_reference = data.get("rti_reference", "")
    first_appeal_date = data.get("first_appeal_date", "[FIRST APPEAL DATE]")
    first_appeal_outcome = data.get("first_appeal_outcome", "No response received from the First Appellate Authority")
    is_central = data.get("is_central", True)
    commission = "Central Information Commission" if is_central else "State Information Commission"
    commission_address = (
        "August Kranti Bhawan, Bhikaji Cama Place, New Delhi - 110066"
        if is_central
        else "[State Information Commission Address]"
    )
    commission_portal = "cic.gov.in/secondappeal" if is_central else "[State IC Portal]"

    lines = []
    lines.append(f"Date: {date}")
    lines.append("")
    lines.append("To,")
    lines.append("The Registrar,")
    lines.append(commission)
    lines.append(commission_address)
    lines.append("")
    lines.append(
        f"Subject: Second Appeal under Section 19(3) of the Right to Information Act, 2005"
    )
    lines.append(f"         — against the CPIO and First Appellate Authority, {authority_name}")
    lines.append("")
    lines.append("Respected Sir/Madam,")
    lines.append("")
    lines.append(
        f"I, {applicant_name}, a citizen of India, hereby file this Second Appeal before the "
        f"Hon'ble {commission} under Section 19(3) of the Right to Information Act, 2005."
    )
    lines.append("")
    lines.append("1. DETAILS OF ORIGINAL RTI APPLICATION:")
    lines.append(f"   Date of RTI filing: {rti_date}")
    lines.append(f"   Filed with: The CPIO, {authority_name}")
    lines.append(f"   Subject: {rti_subject}")
    if rti_reference:
        lines.append(f"   Reference No: {rti_reference}")
    lines.append("")
    lines.append("2. DETAILS OF FIRST APPEAL:")
    lines.append(f"   Date of First Appeal: {first_appeal_date}")
    lines.append(f"   Outcome: {first_appeal_outcome}")
    lines.append("")
    lines.append("3. GROUNDS FOR SECOND APPEAL:")
    lines.append(
        "   a. The Public Information Officer and/or First Appellate Authority have failed "
        "to provide the requested information within the period prescribed under the RTI Act, 2005."
    )
    lines.append(
        "   b. The information sought is not covered by any exemption under Section 8 of "
        "the RTI Act, 2005, and there is no lawful basis for non-disclosure."
    )
    lines.append(
        "   c. The conduct of the PIO constitutes malafide/willful obstruction within the "
        "meaning of Section 20(1) of the RTI Act, 2005, warranting imposition of penalty."
    )
    lines.append("")
    lines.append("4. PRAYERS:")
    lines.append("   This Hon'ble Commission is respectfully prayed to:")
    lines.append(
        "   a. Direct the public authority to provide complete information within 7 days;"
    )
    lines.append(
        "   b. Impose maximum penalty of Rs 25,000/- on the PIO under Section 20(1);"
    )
    lines.append(
        "   c. Award compensation to the appellant for detriment suffered under Section 19(8)(b);"
    )
    lines.append(
        "   d. Issue a show-cause notice to the PIO and recommend disciplinary action under "
        "Section 20(2) if the violation is found to be persistent."
    )
    lines.append("")
    lines.append(
        "I declare that the facts stated above are true to the best of my knowledge."
    )
    lines.append("")
    lines.append("Yours faithfully,")
    lines.append("")
    lines.append(applicant_name)
    lines.append(applicant_address)
    lines.append(f"Date: {date}")
    lines.append("")
    lines.append("Enclosures:")
    lines.append("  1. Copy of original RTI application")
    lines.append("  2. Proof of RTI submission")
    lines.append("  3. Copy of First Appeal")
    lines.append("  4. CPIO's response (if any)")
    lines.append("  5. First Appellate Authority's order (if any)")
    lines.append("")
    lines.append(f"Online filing portal: {commission_portal}")
    lines.append("")
    lines.append("─" * 60)
    lines.append("This appeal is filed under the Right to Information Act, 2005.")
    lines.append("Informational assistance only. This is not legal advice.")
    lines.append("─" * 60)

    return "\n".join(str(line) for line in lines)


def main():
    parser = argparse.ArgumentParser(description="Format RTI appeal letter")
    parser.add_argument("--file", help="Input JSON file path")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()

    if args.file:
        with open(args.file) as f:
            data = json.load(f)
    else:
        try:
            data = json.load(sys.stdin)
        except (json.JSONDecodeError, Exception):
            data = {}

    appeal_type = data.get("appeal_type", "first")

    if appeal_type == "second":
        letter = format_second_appeal(data)
    else:
        letter = format_first_appeal(data)

    if args.output:
        from pathlib import Path as _P
        out_path = _P(args.output).resolve()
        safe = (
            str(out_path).startswith("/tmp") or
            str(out_path).startswith("/home") or
            "workspace" in str(out_path) or
            not str(out_path).startswith("/")
        )
        if not safe:
            print(f"⚠ Output path restricted for safety. Writing to: workspace/appeal-output.txt")
            out_path = _P("workspace/appeal-output.txt")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(letter)
        print(f"Appeal saved to: {out_path}")
    else:
        print(letter)


if __name__ == "__main__":
    main()
