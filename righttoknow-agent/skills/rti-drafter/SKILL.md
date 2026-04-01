---
name: rti-drafter
description: "Drafts complete, legally correct RTI applications under the RTI Act 2005 for any public authority. Generates ready-to-submit formatted letters with proper citations, fee details, and filing instructions. Use when user wants to file an RTI, request government information, or ask a public authority for documents, records, or decisions."
license: MIT
allowed-tools: Bash Read Write
metadata:
  author: righttoknow-project
  version: "1.0.0"
  category: civic-tech
  legal_framework: RTI Act 2005
  jurisdiction: india
---

# RTI Application Drafter

## Overview

This skill generates complete, submission-ready RTI applications. A good RTI is:
- Addressed to the correct CPIO (confirmed via authority-mapper)
- Specific and focused (one subject per application)
- Legally sound (cites correct sections)
- Practically helpful (asks for information that *can* be provided)

## Pre-Drafting Checklist

Before drafting, confirm:
1. ✅ Applicant's name and address
2. ✅ State of residence (for fee and state vs central determination)
3. ✅ Correct public authority (from authority-mapper skill)
4. ✅ Specific information needed (not vague complaints)
5. ✅ Timeline of events relevant to the query (if applicable)

## How to Draft

### Step 1: Clarify the Core Question

Transform the user's complaint into specific, answerable information requests:
- BAD: "My pension is pending, I want to complain"
- GOOD: "Provide the current status of my pension claim [reference number], the name of the officer handling it, and the specific reason(s) for any delay."

### Step 2: Generate the Application

Use this exact format:

```
Date: [DD/MM/YYYY]

To,
The Central/State Public Information Officer,
[Full Official Name of Department/Ministry]
[Complete Address]

Subject: Application under the Right to Information Act, 2005

Respected Sir/Madam,

I, [Full Name], a citizen of India, hereby submit this application under Section 6(1) of the Right to Information Act, 2005, and request the following information:

1. [Specific question 1]
2. [Specific question 2]
3. [Specific question 3]
[Continue as needed — maximum 8 questions per application]

[If applicable]
Reference details:
- [Application/Registration/Complaint number]
- [Date of previous application/interaction]
- [Any other relevant reference]

I am enclosing a fee of ₹10/- (Rupees Ten only) as application fee by [Indian Postal Order / Demand Draft / Online Payment as applicable].

[If BPL]: I am a Below Poverty Line (BPL) cardholder and am therefore exempt from paying the application fee, per Section 7(5) of the RTI Act 2005. My BPL card number is [number].

I request you to provide the information within 30 days as mandated under Section 7(1) of the RTI Act, 2005.

If my application is transferred to another public authority under Section 6(3), I request intimation of the same.

This is a bona fide request for information in public interest.

Thanking you,

Yours faithfully,

[Full Name]
[Complete Address]
[City, State, PIN Code]
[Phone Number — optional]
[Email — optional]
[Date]

---
Note: This application is filed under the Right to Information Act, 2005.
This document was prepared with informational assistance. It does not constitute legal advice.
```

### Step 3: Craft Information Requests

Each question must be:
- **Specific**: Ask for named documents, records, dates, names
- **Answerable**: Ask for existing information (not opinions or future actions)
- **Proportionate**: Don't ask for 10,000 pages of records

**Good question patterns:**
- "Provide a certified copy of [specific document]"
- "State the name and designation of the officer who [took specific action] on [date]"
- "Provide the current status of [application/complaint/claim] bearing reference number [X]"
- "State the specific rule/section/notification under which [action] was taken"
- "Provide copies of all correspondence relating to [matter] between [date range]"
- "State the sanctioned strength and actual strength of [department/unit] as on [date]"

**Avoid vague requests:**
- "Provide all documents related to corruption" — too broad
- "Explain why your department is inefficient" — not a request for information
- "Tell me what happened" — rephrase as specific document requests

### Step 4: Output Files

Save the completed RTI application to:
`workspace/rti-[authority-short-name]-[topic-keyword]-[YYYY-MM-DD].txt`

Example: `workspace/rti-epfo-pension-delay-2026-03-29.txt`

Also create a plain-language summary:
`workspace/rti-summary-[YYYY-MM-DD].txt`

## Filing Instructions to Always Provide

After generating the application, always tell the user:

**Central Government RTIs:**
- Online: rtionline.gov.in (fee paid via net banking/UPI)
- Postal: Send to CPIO's address with IPO/DD for ₹10
- Hand delivery: Submit at department's public window

**State RTIs:**
- Check state-specific portal from knowledge base
- State fees vary (₹10-50)
- Submission methods vary by state

**After filing:**
- Keep a copy of the application and payment proof
- Note the date — response due in 30 days
- If no response in 30 days → file First Appeal (use appeal-wizard skill)

## Special Cases

### Life and Liberty Matters
If the RTI involves imminent threat to life or personal liberty (hospital denying treatment records, illegal detention, etc.), note prominently:
"This matter pertains to life/liberty under Section 7(1) proviso — response required within 48 HOURS."

### Third-Party Information
If asking for information about a named third party, acknowledge Section 11 implications. The CPIO may need to notify the third party, potentially extending the response timeline.

### Appeal-Ready Language
Always draft questions in a way that if rejected, the rejection itself is informative and appealable. Include: "If any part of this information is withheld, please provide the specific exemption under Section 8 or Section 9 of the RTI Act 2005 applicable to each withheld item."
