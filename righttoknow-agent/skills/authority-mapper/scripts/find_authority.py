#!/usr/bin/env python3
"""
Authority Lookup — RightToKnow Agent
Finds the correct Central/State public authority for a given RTI matter.

Usage:
  python3 find_authority.py "EPFO pension claim"
  echo "passport delay" | python3 find_authority.py
"""

import sys
import json

# Central Authority Database
CENTRAL_AUTHORITIES = {
    "epfo": {
        "name": "Employees' Provident Fund Organisation",
        "ministry": "Ministry of Labour & Employment",
        "cpio": "Regional Provident Fund Commissioner (RTI)",
        "address": "EPFO Regional Office, [Your City]",
        "online": "https://epfigms.gov.in (Grievance) | rtionline.gov.in (RTI)",
        "fee": "₹10 (IPO/DD/Online)",
        "keywords": ["epfo", "pf", "provident fund", "pension", "employee pension", "eps", "withdrawal", "epf"]
    },
    "income_tax": {
        "name": "Income Tax Department",
        "ministry": "Ministry of Finance (CBDT)",
        "cpio": "CPIO, Income Tax Department",
        "address": "Office of the Commissioner of Income Tax, [Your City]",
        "online": "https://rtionline.gov.in",
        "fee": "₹10 (Online/IPO)",
        "keywords": ["income tax", "itr", "tds", "pan", "tax refund", "cbdt", "tax demand"]
    },
    "passport": {
        "name": "Passport Seva / Ministry of External Affairs",
        "ministry": "Ministry of External Affairs",
        "cpio": "CPIO, Regional Passport Office",
        "address": "Regional Passport Office, [Your City]",
        "online": "https://rtionline.gov.in",
        "fee": "₹10 (Online/IPO)",
        "keywords": ["passport", "visa", "oci", "pcc", "police verification", "mea"]
    },
    "aadhaar": {
        "name": "Unique Identification Authority of India (UIDAI)",
        "ministry": "Ministry of Electronics & IT",
        "cpio": "CPIO, UIDAI Regional Office",
        "address": "UIDAI Regional Office, [Your City]",
        "online": "https://rtionline.gov.in",
        "fee": "₹10",
        "keywords": ["aadhaar", "uid", "uidai", "biometric", "enrolment", "update"]
    },
    "railways": {
        "name": "Indian Railways",
        "ministry": "Ministry of Railways",
        "cpio": "CPIO, Divisional Railway Manager",
        "address": "O/o Divisional Railway Manager, [Your Division]",
        "online": "https://rtionline.gov.in",
        "fee": "₹10",
        "keywords": ["railway", "train", "irctc", "ticket", "reservation", "railway police", "accident"]
    },
    "post_office": {
        "name": "Department of Posts",
        "ministry": "Ministry of Communications",
        "cpio": "CPIO, Divisional Superintendent of Post Offices",
        "address": "O/o Superintendent of Post Offices, [Your Division]",
        "online": "https://rtionline.gov.in",
        "fee": "₹10 (IPO preferred)",
        "keywords": ["post office", "postal", "speed post", "money order", "savings", "nsc", "postal life"]
    },
    "esic": {
        "name": "Employees' State Insurance Corporation",
        "ministry": "Ministry of Labour & Employment",
        "cpio": "CPIO, ESIC Regional Office",
        "address": "ESIC Regional Office, [Your City]",
        "online": "https://rtionline.gov.in",
        "fee": "₹10",
        "keywords": ["esic", "esi", "employee state insurance", "medical benefit", "ip dispensary"]
    },
    "central_bank": {
        "name": "Respective Nationalized Bank / RBI",
        "ministry": "Ministry of Finance",
        "cpio": "CPIO, [Bank Name] - Head Office / Nodal Branch",
        "address": "Head Office of [Bank Name]",
        "online": "https://rtionline.gov.in",
        "fee": "₹10",
        "keywords": ["bank", "sbi", "pnb", "ubi", "canara", "bank of baroda", "rbi", "loan", "account"]
    },
    "upsc": {
        "name": "Union Public Service Commission",
        "ministry": "UPSC (Autonomous)",
        "cpio": "CPIO, Union Public Service Commission",
        "address": "Dholpur House, Shahjahan Road, New Delhi - 110069",
        "online": "https://rtionline.gov.in",
        "fee": "₹10",
        "keywords": ["upsc", "civil services", "ias", "ips", "ifs", "nda", "cds", "capf"]
    },
    "nhai": {
        "name": "National Highways Authority of India",
        "ministry": "Ministry of Road Transport & Highways",
        "cpio": "CPIO, NHAI Regional Office",
        "address": "NHAI Regional/Project Office",
        "online": "https://rtionline.gov.in",
        "fee": "₹10",
        "keywords": ["nhai", "highway", "national highway", "toll", "land acquisition highway"]
    }
}

# State authorities (Rajasthan focus, extensible)
STATE_AUTHORITIES = {
    "land_records": {
        "name": "Revenue Department",
        "cpio": "CPIO, Office of the Tehsildar / Collector",
        "address": "Revenue Department, District Collectorate",
        "keywords": ["land", "khasra", "jamabandi", "patta", "mutation", "registry", "nakal", "bhu-abhilekh"]
    },
    "municipal": {
        "name": "Municipal Corporation / Nagar Palika",
        "cpio": "CPIO, Municipal Commissioner",
        "address": "Municipal Corporation / Nagar Palika Headquarters",
        "keywords": ["municipal", "corporation", "nagar palika", "water supply", "road", "garbage", "drainage", "property tax", "building permission"]
    },
    "police": {
        "name": "State Police Department",
        "cpio": "CPIO, Superintendent of Police",
        "address": "O/o the Superintendent of Police, [District]",
        "keywords": ["police", "fir", "complaint", "theft", "crime", "custody", "arrest"]
    },
    "electricity": {
        "name": "State Electricity Distribution Company",
        "cpio": "CPIO, Chief Engineer (Distribution)",
        "address": "Office of the Chief Engineer, [DISCOM]",
        "keywords": ["electricity", "power", "bill", "connection", "meter", "discom", "jvvnl", "avvnl"]
    },
    "education": {
        "name": "State Education Department",
        "cpio": "CPIO, District Education Officer",
        "address": "O/o District Education Officer",
        "keywords": ["school", "teacher", "admission", "board exam", "scholarship", "midday meal", "education"]
    },
    "health": {
        "name": "State Health Department",
        "cpio": "CPIO, Chief Medical Officer",
        "address": "O/o Chief Medical Officer, District Hospital",
        "keywords": ["hospital", "health", "doctor", "medicine", "ambulance", "health centre", "ayushman"]
    },
    "ration": {
        "name": "Food & Civil Supplies Department",
        "cpio": "CPIO, District Supply Officer",
        "address": "O/o District Supply Officer",
        "keywords": ["ration", "pds", "fair price shop", "ration card", "grain", "kerosene", "food security"]
    }
}

def find_authority(query: str) -> dict:
    query_lower = query.lower()

    # Check central authorities first
    for key, auth in CENTRAL_AUTHORITIES.items():
        if any(kw in query_lower for kw in auth["keywords"]):
            return {
                "level": "Central Government",
                "found": True,
                "authority": auth["name"],
                "ministry": auth["ministry"],
                "cpio_designation": auth["cpio"],
                "address": auth["address"],
                "online_portal": auth["online"],
                "fee": auth["fee"],
                "response_deadline": "30 days",
                "confidence": "HIGH",
                "matched_authority_type": key
            }

    # Check state authorities
    for key, auth in STATE_AUTHORITIES.items():
        if any(kw in query_lower for kw in auth["keywords"]):
            return {
                "level": "State Government",
                "found": True,
                "authority": auth["name"],
                "ministry": "State Government Department",
                "cpio_designation": auth["cpio"],
                "address": auth["address"],
                "online_portal": "State RTI Portal (check state government website)",
                "fee": "₹10-50 (varies by state — check state RTI rules)",
                "response_deadline": "30 days",
                "confidence": "MEDIUM",
                "note": "State-specific rules apply. Verify at your state's official RTI portal.",
                "matched_authority_type": key
            }

    # Default — suggest filing with transfer request
    return {
        "level": "Unknown — needs clarification",
        "found": False,
        "suggestion": (
            "The authority could not be automatically determined. "
            "Please provide more context about: which government department issued the decision, "
            "which state you are in, and the nature of the service involved."
        ),
        "fallback_advice": (
            "If uncertain, address to the most likely department and include: "
            "'If this is not within your jurisdiction, please transfer this application "
            "to the competent authority as per Section 6(3) of the RTI Act, 2005.'"
        ),
        "confidence": "LOW"
    }

def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:]).strip()
    else:
        try:
            query = sys.stdin.read().strip()
        except Exception:
            query = ""

    if not query:
        # Return a valid JSON result instead of exiting with error
        result = {
            "level": "Unknown — query was empty",
            "found": False,
            "suggestion": "Please provide a description of the government issue or department.",
            "fallback_advice": "Describe the problem (e.g., 'EPFO pension', 'income tax refund', 'passport delay').",
            "confidence": "LOW"
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    result = find_authority(query)
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
