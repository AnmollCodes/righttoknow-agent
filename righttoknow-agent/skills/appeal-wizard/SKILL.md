---
name: appeal-wizard
description: "Drafts Section 19(1) First Appeals and Section 19(3) Second Appeals / Complaints when RTI applications receive no response, are rejected, or receive incomplete information. Use when a user's RTI was ignored, refused, or partially answered. Also handles complaints to Information Commissions."
license: MIT
allowed-tools: Bash Read Write
metadata:
  author: righttoknow-project
  version: "1.0.0"
  category: civic-tech
---

# Appeal Wizard

## When to Use This Skill

| Situation | Action |
|-----------|--------|
| No response within 30 days | Section 19(1) First Appeal |
| Response received but information refused/incomplete | Section 19(1) First Appeal |
| First Appeal not decided within 30 days | Section 19(3) Second Appeal |
| First Appellate Authority denied appeal | Section 19(3) Second Appeal |
| PIO gave false/misleading information | Complaint to Information Commission |
| PIO obstructed access to information | Complaint to Information Commission |

## Timeline Awareness

- **First Appeal**: Must be filed within **30 days** of RTI response date (or 30 days after response was due if no response)
- **Second Appeal**: Must be filed within **90 days** of First Appellate Authority's decision (or its due date)
- **Compensation/Penalty**: Can request information commission to impose penalty on PIO under Section 20

## First Appeal Format (Section 19(1))

```
Date: [DD/MM/YYYY]

To,
The First Appellate Authority,
[Full Name of Department/Ministry]
[Complete Address]

Subject: First Appeal under Section 19(1) of the Right to Information Act, 2005
         against the order of the CPIO, [Department Name]

Respected Sir/Madam,

I, [Full Name], a citizen of India, hereby file this First Appeal under Section 19(1) 
of the Right to Information Act, 2005, against the [non-response / partial response / 
rejection] of my RTI application dated [DD/MM/YYYY].

1. PARTICULARS OF ORIGINAL RTI APPLICATION:
   a. Date of RTI application: [DD/MM/YYYY]
   b. Sent to: The CPIO, [Department Name]
   c. Subject: [Brief description]
   d. Registration/Tracking Number (if any): [Number]

2. STATUS OF RESPONSE:
   [Choose applicable:]
   a. No response has been received till date, though [X] days have elapsed since filing.
      The information was due by [DD/MM/YYYY] as per Section 7(1) of the RTI Act.
   
   OR
   
   b. A response was received on [DD/MM/YYYY] refusing information on grounds of 
      Section [8(1)(X)] of the RTI Act. The grounds cited are:
      "[Paste the CPIO's exact refusal reason]"

3. GROUNDS OF APPEAL:
   [Use relevant grounds below:]

   a. The information sought does not fall within any exemption under Section 8 of the 
      RTI Act, 2005 as claimed, because: [Your specific reason]
   
   b. The CPIO failed to respond within the statutory 30-day period prescribed under 
      Section 7(1), which amounts to deemed refusal under Section 7(2).
   
   c. The information provided is incomplete and does not address Questions [X, Y, Z] 
      in my original application.
   
   d. The refusal does not cite a specific provision of Section 8 with justification, 
      as required under Section 7(8).
   
   e. The information sought relates to a public activity and there is no reasonable 
      ground to withhold it from a citizen.

4. RELIEF SOUGHT:
   I respectfully pray that this Hon'ble First Appellate Authority may:
   a. Direct the CPIO to furnish the information sought within [7/15] days;
   b. [If applicable] Impose a penalty on the CPIO under Section 20(1) for wrongful 
      refusal / delayed response;
   c. Award compensation for the delay and inconvenience caused, under Section 19(8)(b).

5. DECLARATION:
   I declare that the facts stated in this appeal are true and correct to the best of my 
   knowledge and belief.

Thanking you,

Yours faithfully,

[Full Name]
[Complete Address]
[City, State, PIN Code]
[Phone Number]
[Email]
Date: [DD/MM/YYYY]

Enclosures:
1. Copy of original RTI application
2. Proof of dispatch/submission
3. Copy of CPIO's response (if received)
4. [Any other supporting document]

---
This appeal is filed under the Right to Information Act, 2005.
Informational assistance provided — not legal advice. Consult a licensed advocate for legal counsel.
```

## Second Appeal / Complaint Format (Section 19(3))

For filing with the Central Information Commission (CIC) or State Information Commission (SIC):

**CIC Online Portal**: cic.gov.in/secondappeal
**CIC Address**: Central Information Commission, August Kranti Bhawan, Bhikaji Cama Place, New Delhi - 110066

```
Date: [DD/MM/YYYY]

To,
The Registrar,
[Central / State] Information Commission,
[Address]

Subject: Second Appeal / Complaint under Section 19(3) / Section 18 of the 
         Right to Information Act, 2005

[Follow similar format as First Appeal, additionally including:]

DETAILS OF FIRST APPEAL:
- Date of First Appeal: [DD/MM/YYYY]
- Filed with: [First Appellate Authority Name & Designation]
- Outcome: [No response / Decision received — unfavorable]
- Date of First Appellate Authority's Decision (or due date): [DD/MM/YYYY]

PRAYERS TO THE INFORMATION COMMISSION:
1. Direct the CPIO to provide complete information within [7] days
2. Impose maximum penalty of ₹25,000/- on the CPIO under Section 20(1) for 
   malafide/willful obstruction
3. Award compensation for detriment suffered
4. Issue a show cause notice to the CPIO
```

## How to Draft Appeals Effectively

### Strongest Grounds (in priority order):

1. **Deemed refusal** (no response in 30 days) — Always mention specific days elapsed
2. **Section cited incorrectly** — If they cited Section 8(1)(d) but you are not asking for commercial confidence, challenge it
3. **Incomplete information** — Reference exact questions from original RTI that were not answered
4. **No reasons given** — Section 7(8) requires reasons in writing for refusal
5. **Information not in exempt category** — Counter their Section 8 claim with facts

### Tone and Language

Keep appeals formal, factual, and unemotional. Cite section numbers. Do not make personal accusations against PIOs by name. Focus on the statutory obligations, not the officer's character.

### Save Appeals to Memory

After drafting, use the `status-diary` skill to update the filing status from "Filed" to "First Appeal Filed" in memory.
