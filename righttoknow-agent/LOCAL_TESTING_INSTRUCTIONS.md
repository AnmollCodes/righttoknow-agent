# Local Setup & Testing Instructions

Complete guide to run RightToKnow agent locally for evaluation and testing.

---

## ✅ Prerequisites Checklist

Before running the project, ensure your system has:

- **Node.js:** v20 or higher
- **Python:** 3.8 or higher  
- **npm:** 8.0 or higher (comes with Node.js)
- **Git:** 2.30 or higher

### Verify Installation
```bash
node --version      # Should show v20+
python --version    # Should show 3.8+
npm --version       # Should show 8.0+
git --version       # Should show 2.30+
```

---

## 🚀 Setup Steps (5 Minutes)

### Step 1: Clone the Repository
```bash
git clone https://github.com/AnmollCodes/righttoknow-agent.git
cd righttoknow-agent
```

### Step 2: Install gitclaw (One-Time)
```bash
npm install -g gitclaw@1.1.8
```

### Step 3: Get Your API Key

Use **Anthropic Claude** (recommended):
- Get key from: https://console.anthropic.com/api/keys
- Key format: `sk-ant-...`

**Or use OpenAI/Gemini:**
- OpenAI: `sk-...` from https://platform.openai.com/api-keys
- Gemini: From Google Cloud Console

### Step 4: Configure API Key

**Option A: Edit .env file** (Recommended)
```bash
# Windows/macOS/Linux - Open .env file in any text editor
nano .env
```

Replace placeholder with your actual key:
```env
ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
```

**Option B: Set Environment Variable**
```bash
# macOS/Linux/WSL
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

### Step 5: Verify Setup
```bash
# Validate agent structure
npx gitagent validate

# Expected: ✅ All checks pass
```

---

## 🧪 Testing Procedures

### Quick Validation (No API Calls)
```bash
./demo.sh quick
```

**What it checks:**
- ✅ Node.js >= 20
- ✅ Python >= 3.8  
- ✅ Agent structure (agent.yaml, SOUL.md, RULES.md)
- ✅ All 4 skills present
- ✅ Python scripts working
- ✅ Sample RTI letter generation

### Run Complete Demo (With API)
```bash
# Scenario 1: EPFO Pension Delay
./demo.sh scenario 1

# Scenario 2: Passport Not Issued
./demo.sh scenario 2

# Scenario 3: Income Tax Refund
./demo.sh scenario 3

# Scenario 4: First Appeal (RTI Unanswered)
./demo.sh scenario 4

# Scenario 5: State RTI (Ration Card)
./demo.sh scenario 5
```

### Custom Test
```bash
./demo.sh custom "My [problem] has been pending [time period]"
```

### Direct Agent Test
```bash
npx gitclaw --dir . "My EPFO pension hasn't started 6 months after retirement. I'm in Jaipur, Rajasthan."
```

**Expected Output:**
1. Agent identifies authority (EPFO Regional Office)
2. Agent drafts RTI application (Section 6(1))
3. Agent provides filing instructions
4. Agent saves to memory with deadline

---

## 📂 Output Verification

### Check Generated Files
```bash
ls workspace/
```

Should contain `.txt` files with generated RTI letters.

### Check Memory Tracking
```bash
cat memory/MEMORY.md
```

Should show filing history and deadline tracking.

### Validate Letter Quality
```bash
# View generated RTI letter
cat workspace/demo-rti-epfo-pension-*.txt

# Should contain:
# ✓ Date (DD/MM/YYYY format)
# ✓ Section 6(1) citation
# ✓ Correct authority address
# ✓ Specific questions (5-6)
# ✓ Fee information (₹10 for central)
# ✓ 30-day deadline
# ✓ Applicant's bona fide declaration
```

---

## 🔍 Testing Checklist

Run through these to validate full functionality:

- [ ] **Setup Complete**
  - [ ] Node.js v20+ installed
  - [ ] Python 3.8+ installed
  - [ ] API key configured
  - [ ] Repository cloned

- [ ] **Structure Validation**
  - [ ] Run `npx gitagent validate` → All pass
  - [ ] `./demo.sh quick` → No errors

- [ ] **Python Scripts**
  - [ ] Authority mapper working (JSON output)
  - [ ] RTI formatter working (letter generated)
  - [ ] Files in workspace/ directory

- [ ] **Agent Functionality**
  - [ ] Run scenario 1 successfully
  - [ ] Check generated RTI letter format
  - [ ] Verify memory updated
  - [ ] Run custom test works

- [ ] **Output Quality**
  - [ ] RTI letter has proper format
  - [ ] Section 6(1) cited
  - [ ] Authority correctly identified
  - [ ] Fee guidance included
  - [ ] Deadline mentioned (30 days)

---

## 🛠️ Troubleshooting

### Problem: "Node.js >= 20 required"
```bash
# Install/upgrade Node.js
# Visit: https://nodejs.org/
# Download and install the LTS version
node --version  # Verify v20+
```

### Problem: "Python not found"
```bash
# Install Python
# Visit: https://python.org/
# Download and install 3.8+
python --version  # Verify 3.8+
```

### Problem: "gitclaw: command not found"
```bash
npm install -g gitclaw@1.1.8
```

### Problem: "API key not found"
```bash
# Edit .env file and add your key
nano .env
# Add: ANTHROPIC_API_KEY="sk-ant-..."

# Or export as environment variable
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Problem: "Script not found or not executable"
```bash
# Make demo.sh executable
chmod +x demo.sh

# Run again
./demo.sh quick
```

### Problem: "Python script fails"
```bash
# Verify Python is working
python --version

# Test authority mapper directly
python skills/authority-mapper/scripts/find_authority.py "test query"
```

---

## 📊 Expected Results

### Scenario 1 Output (Sample)
```
Authority Identified:
  Name: Employees' Provident Fund Organisation
  CPIO Title: Regional Provident Fund Commissioner (RTI)
  Address: EPFO Regional Office, Jaipur
  Fee: ₹10
  Response Deadline: 30 days

RTI Letter Generated:
  Location: workspace/demo-rti-epfo-pension-2026-03-30.txt
  Size: ~3.5 KB
  Format: Ready to submit

Memory Updated:
  Filing ID: RTI-001
  Status: Pending response
  Deadline Alert: Day 25
```

### Python Script Output (Authority Mapper)
```json
{
  "level": "Central Government",
  "found": true,
  "authority": "Employees' Provident Fund Organisation",
  "ministry": "Ministry of Labour & Employment",
  "cpio_designation": "Regional Provident Fund Commissioner (RTI)",
  "fee": "₹10",
  "response_deadline": "30 days",
  "confidence": "HIGH"
}
```

---

## 📋 Full Test Timeline

| Step | Command | Time | Expected Result |
|------|---------|------|-----------------|
| 1 | `./demo.sh quick` | 30s | ✅ All validations pass |
| 2 | `./demo.sh scenario 1` | 60s | ✅ RTI letter generated |
| 3 | `cat workspace/demo-rti-*.txt` | 10s | ✅ Proper format verified |
| 4 | `cat memory/MEMORY.md` | 10s | ✅ Filing tracked |
| 5 | `./demo.sh scenario 2-5` | 3m | ✅ All scenarios work |
| **Total** | | **~5 minutes** | ✅ Full validation |

---

## ✅ Success Criteria

**Your local testing is successful when:**

✓ `./demo.sh quick` completes without errors  
✓ All 5 scenarios generate RTI letters  
✓ Generated files appear in `workspace/`  
✓ Memory system tracks filings  
✓ Each letter contains:
  - Correct authority
  - Section 6(1) citation
  - ₹10 fee for central RTIs
  - 30-day deadline
  - Proper formatting
  - Bona fide declaration

---

## 📞 Support During Testing

If you encounter issues:

1. **Check Prerequisites**
   ```bash
   node --version
   python --version
   npm --version
   ```

2. **Verify API Key** 
   - Ensure key starts with `sk-ant-` (for Anthropic)
   - Check it's valid and not expired
   - Verify in .env or environment variable

3. **Review Error Messages**
   - Check terminal output for specific error
   - Read error message carefully for hints
   - Search for error in README.md or TESTING.md

4. **Check Documentation**
   - README.md — Full project documentation
   - TESTING.md — Comprehensive test suite
   - QUICKSTART.md — Quick reference

---

## 🎯 For Submission Portal

**Copy this summary into "Local Testing Instructions" field:**

```
SETUP (5 minutes):
1. git clone https://github.com/AnmollCodes/righttoknow-agent.git
2. npm install -g gitclaw@1.1.8
3. Add ANTHROPIC_API_KEY to .env file
4. npx gitagent validate

TESTING:
- Quick validation: ./demo.sh quick
- Full demo: ./demo.sh scenario 1-5
- Custom test: ./demo.sh custom "Your RTI query"

VERIFY:
- Check workspace/ for generated RTI letters
- Check memory/MEMORY.md for tracking
- Verify letters contain Section 6(1), fees, deadlines

EXPECTED: 
- 5 RTI scenario letters generated
- Proper formatting validated
- All Python scripts working
- Memory system functional

TIME: ~5 minutes for full validation
```

---

## 📌 Key Commands Reference

```bash
# Setup
git clone https://github.com/AnmollCodes/righttoknow-agent.git
cd righttoknow-agent
npm install -g gitclaw

# Configuration
export ANTHROPIC_API_KEY="your-key-here"  # Or edit .env

# Validation
npx gitagent validate
./demo.sh quick

# Testing
./demo.sh scenario 1    # EPFO pension
./demo.sh scenario 2    # Passport
./demo.sh scenario 3    # Tax refund
./demo.sh scenario 4    # Appeal
./demo.sh scenario 5    # State RTI

# Verification
ls workspace/           # Generated letters
cat memory/MEMORY.md    # Filing history
```

---

## 🎊 You're Ready!

Follow these steps and you'll have:
✅ Working agent locally  
✅ 5 demo scenarios executing  
✅ Generated RTI letters validated  
✅ Complete testing done  

**Estimated Time: 5-10 minutes**

---

**Last Updated:** April 7, 2026  
**Version:** 1.0.0  
**Status:** Production Ready
