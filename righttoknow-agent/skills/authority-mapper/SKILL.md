---
name: authority-mapper
description: "Identifies the correct public authority (CPIO) for any government-related RTI query. Maps citizen problems to the right Central Ministry, Department, State Government, or PSU. Use before drafting any RTI application to ensure it goes to the right place — a misdirected RTI wastes 30 days."
license: MIT
allowed-tools: Bash Read
metadata:
  author: righttoknow-project
  version: "1.0.0"
  category: civic-tech
---

# Authority Mapper

## Purpose

The single most common RTI mistake: sending it to the wrong authority. This skill prevents that. It maps any citizen grievance to the exact public authority responsible.

## Decision Logic

### Step 1: Central or State?

**File with Central Government if:**
- The department/ministry is listed under Government of India (Union List)
- The authority is a Central PSU, nationalized bank, or central university
- The matter relates to: income tax, central excise, customs, passport, EPFO, ESIC, railways, post office, central armed forces, central government employment

**File with State Government if:**
- The department handles state subjects (police, public health, land records, state PSUs, state universities, state electricity/water boards, RTO, municipal corporations)
- The matter relates to: state government employment, state schools/colleges, state hospitals, panchayats, local bodies

**If unclear:** Default to the State Government first, as they have concurrent jurisdiction. You can also file with both if the matter genuinely involves both.

### Step 2: Identify the Specific Authority

**Central Ministries and Their CPIO:**

| Subject Matter | Ministry / Authority | Filing Address |
|----------------|---------------------|----------------|
| Income Tax, TDS, PAN | CBDT, Ministry of Finance | O/o the CPIO, Income Tax Dept, [Local IT Office] |
| GST, Customs, Excise | CBIC, Ministry of Finance | O/o the CPIO, CBIC, North Block, New Delhi |
| Passport, OCI | MEA, Passport Seva | CPIO, Regional Passport Office [City] |
| EPFO — PF/Pension | EPFO | CPIO, Regional PF Commissioner Office [City] |
| ESIC (Health Insurance) | ESIC | CPIO, ESIC Regional Office [City] |
| Railways (tickets, complaints) | Indian Railways (Zonal) | CPIO, [Zonal Railway Headquarters] |
| Post Office | Dept of Posts | CPIO, Divisional/Regional Superintendent of Post Offices |
| Aadhaar, UIDAI | Ministry of Electronics | CPIO, UIDAI Regional Office [City] |
| Central Bank accounts | RBI / respective bank | CPIO, [Bank Branch / Head Office] |
| Central Govt Jobs (UPSC) | UPSC | CPIO, Union Public Service Commission, Dholpur House, New Delhi |
| Central Govt Jobs (SSC) | Staff Selection Commission | CPIO, SSC Regional Office [City] |
| Defence procurement | Ministry of Defence | CPIO, Ministry of Defence, South Block, New Delhi |
| Environment clearances | MoEFCC | CPIO, Ministry of Environment, Indira Paryavaran Bhawan, New Delhi |
| Company registrations | MCA | CPIO, Ministry of Corporate Affairs [Regional Office] |
| Land acquisition (NHAI) | NHAI | CPIO, National Highways Authority of India [Regional Office] |
| Telecom complaints | TRAI / DoT | CPIO, TRAI, Mahanagar Doorsanchar Bhawan, New Delhi |
| Aviation complaints | DGCA | CPIO, DGCA, Opp. Safdarjung Airport, New Delhi |
| Consumer disputes | Consumer Affairs | CPIO, Ministry of Consumer Affairs, Krishi Bhawan, New Delhi |

### Step 3: Find CPIO Contact Details

**For Central Govt:** Most departments list their CPIO on their official website under "RTI" section. Standard URL pattern: `[dept].gov.in/rti`

**Online lookup commands:**
```bash
# Check official RTI portal for Central authority details
echo "Visit: https://rtionline.gov.in to find ministry-wise CPIO details"

# For state authorities, check
echo "Visit: https://rti.rajasthan.gov.in (example for Rajasthan)"
```

### Step 4: State-Specific Authorities

**Rajasthan (relevant for Jaipur users):**
- State RTI Portal: rajasthan.gov.in/rti
- Fee: ₹50 per application
- Payment: Court Fee Stamp or Cash at department

**State Department Map:**
| Subject | State Authority |
|---------|----------------|
| Land records, Jamabandi | Revenue Department / Tehsildar Office |
| State police complaints | SP Office / Home Department |
| State government jobs | State PSC, respective department |
| Municipal services (water, roads) | Municipal Corporation / Nagar Palika |
| State electricity supply | DISCOMS (JVVNL, AVVNL, JdVVNL in Rajasthan) |
| State hospitals | State Health Department / Hospital Administration |
| PDS / Ration cards | Food & Civil Supplies Department |
| State schools | Education Department / DEO Office |
| Building approvals | UDH / Town Planning / UIT |

## Output Format

After mapping, provide:

```
AUTHORITY IDENTIFIED
====================
Level: [Central / State — {State Name}]
Public Authority: [Full Official Name]
CPIO Designation: [Exact Title]
Address: [Complete postal address]
Online Filing: [URL if available]
Fee: [Amount and payment method]
Response Timeline: [30 days / 48 hours]

CONFIDENCE: [HIGH / MEDIUM — with explanation if medium]

ALTERNATIVE AUTHORITY (if applicable):
[Name, with reason why this could also be the right authority]

NEXT STEP: Use the rti-drafter skill with this authority information.
```

## Special Cases

### PSU / Government Companies
Banks (nationalized), LIC, SAIL, BSNL, Air India, ONGC etc. are public authorities under Section 2(h). File with the CPIO of the specific company, usually at their Head Office or the regional branch involved.

### Panchayats and Local Bodies
RTI applies to Gram Panchayats, Municipal Corporations, Development Authorities. State RTI rules govern these.

### Private Bodies with Government Funding
Institutions substantially financed by the government (aided schools, colleges) fall under RTI. Use the definition from Section 2(h)(d).

### When Genuinely Unsure
File with the most likely authority AND mention in the application: "If this application does not fall within your jurisdiction, please transfer it to the appropriate public authority as per Section 6(3) of the RTI Act, 2005."
