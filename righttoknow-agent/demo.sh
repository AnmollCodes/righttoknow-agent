#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# RightToKnow Agent — Demo Script
# Demonstrates the agent handling real RTI scenarios
# ─────────────────────────────────────────────────────────────────

set -e

AGENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

print_header() {
    echo ""
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${CYAN}  ⚖️  RightToKnow — Citizen RTI Assistant Demo${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_scenario() {
    echo -e "${YELLOW}┌─────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${YELLOW}│ SCENARIO: $1${NC}"
    echo -e "${YELLOW}└─────────────────────────────────────────────────────────────┘${NC}"
    echo ""
}

print_step() {
    echo -e "${GREEN}▶ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_prerequisites() {
    print_step "Checking prerequisites..."

    if ! command -v node &> /dev/null; then
        echo -e "${RED}✗ Node.js not found. Install from nodejs.org${NC}"
        exit 1
    fi

    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ Python3 not found. Install Python 3.8+${NC}"
        exit 1
    fi

    local node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$node_version" -lt 20 ]; then
        echo -e "${RED}✗ Node.js version must be >= 20. Found: $(node --version)${NC}"
        exit 1
    fi

    if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${RED}✗ No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY${NC}"
        echo -e "${YELLOW}  export ANTHROPIC_API_KEY='sk-ant-...'${NC}"
        exit 1
    fi

    if ! command -v gitclaw &> /dev/null; then
        print_step "Installing gitclaw..."
        npm install -g gitclaw
    fi

    echo -e "${GREEN}✓ All prerequisites met${NC}"
    echo ""
}

validate_agent() {
    print_step "Validating agent structure..."

    if command -v npx &> /dev/null; then
        npx gitagent validate --dir "$AGENT_DIR" 2>/dev/null && \
            echo -e "${GREEN}✓ gitagent validation passed${NC}" || \
            echo -e "${YELLOW}⚠ gitagent validate not available — checking manually${NC}"
    fi

    # Manual check
    local required=("agent.yaml" "SOUL.md" "RULES.md")
    for file in "${required[@]}"; do
        if [ -f "$AGENT_DIR/$file" ]; then
            echo -e "${GREEN}  ✓ $file${NC}"
        else
            echo -e "${RED}  ✗ $file MISSING${NC}"
        fi
    done

    local skills=("rti-drafter" "authority-mapper" "appeal-wizard" "status-diary")
    for skill in "${skills[@]}"; do
        if [ -f "$AGENT_DIR/skills/$skill/SKILL.md" ]; then
            echo -e "${GREEN}  ✓ skills/$skill/SKILL.md${NC}"
        else
            echo -e "${RED}  ✗ skills/$skill/SKILL.md MISSING${NC}"
        fi
    done
    echo ""
}

test_python_scripts() {
    print_step "Testing Python utility scripts..."

    # Test authority lookup
    echo -e "${CYAN}  Testing authority lookup for 'EPFO pension'...${NC}"
    local result=$(python3 "$AGENT_DIR/skills/authority-mapper/scripts/find_authority.py" "EPFO pension claim" 2>/dev/null)
    if echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print('  ✓ Authority:', d['authority'])" 2>/dev/null; then
        echo -e "${GREEN}  ✓ authority-mapper script working${NC}"
    else
        echo -e "${YELLOW}  ⚠ Could not run authority-mapper script${NC}"
    fi

    # Test RTI formatter with sample data
    echo -e "${CYAN}  Testing RTI letter formatter...${NC}"
    local sample_input='{
        "applicant_name": "Rajesh Kumar",
        "applicant_address": "123 Civil Lines",
        "applicant_city": "Jaipur",
        "applicant_state": "Rajasthan",
        "applicant_pin": "302006",
        "authority_name": "EPFO Regional Office, Jaipur",
        "authority_address": "Bhavishya Nidhi Bhawan, Sector 10, Jaipur",
        "cpio_designation": "Regional Provident Fund Commissioner (RTI)",
        "subject": "Status of EPS Pension Claim — UAN 100XXXXXXXXX",
        "questions": [
            "Provide the current status of the EPS pension claim for UAN 100XXXXXXXXX.",
            "State the name and designation of the officer currently processing this claim.",
            "Provide copies of all notings and orders made on the pension file to date."
        ],
        "fee_mode": "Indian Postal Order"
    }'

    echo "$sample_input" | python3 "$AGENT_DIR/skills/rti-drafter/scripts/format_rti.py" \
        --output "$AGENT_DIR/workspace/test-rti-sample.txt" 2>/dev/null && \
        echo -e "${GREEN}  ✓ RTI formatter script working — output: workspace/test-rti-sample.txt${NC}" || \
        echo -e "${YELLOW}  ⚠ RTI formatter had an issue${NC}"

    echo ""
}

show_sample_output() {
    print_step "Sample RTI letter preview..."
    echo ""

    if [ -f "$AGENT_DIR/workspace/test-rti-sample.txt" ]; then
        echo -e "${CYAN}┌─────────── GENERATED RTI APPLICATION (preview) ───────────┐${NC}"
        head -30 "$AGENT_DIR/workspace/test-rti-sample.txt" | while IFS= read -r line; do
            echo -e "${NC}  $line"
        done
        echo -e "${CYAN}  ... (full letter in workspace/test-rti-sample.txt)${NC}"
        echo -e "${CYAN}└──────────────────────────────────────────────────────────┘${NC}"
    fi
    echo ""
}

run_demo_scenario() {
    local scenario_num="$1"
    local prompt="$2"
    local description="$3"

    print_scenario "[$scenario_num] $description"
    print_info "Prompt: \"$prompt\""
    echo ""
    print_step "Running agent..."
    echo ""

    gitclaw --dir "$AGENT_DIR" "$prompt"

    echo ""
    echo -e "${GREEN}✓ Scenario $scenario_num complete${NC}"
    echo ""

    if ls "$AGENT_DIR/workspace/"*.txt 2>/dev/null | head -1 > /dev/null; then
        echo -e "${CYAN}Generated files in workspace/:${NC}"
        ls -la "$AGENT_DIR/workspace/"*.txt 2>/dev/null | awk '{print "  " $NF " (" $5 " bytes)"}'
    fi
    echo ""
}

show_usage() {
    echo ""
    echo -e "${BOLD}USAGE:${NC}"
    echo -e "  ${CYAN}./demo.sh${NC}                  — Interactive demo mode"
    echo -e "  ${CYAN}./demo.sh quick${NC}            — Run quick validation + script test"
    echo -e "  ${CYAN}./demo.sh scenario 1${NC}       — Run specific scenario"
    echo -e "  ${CYAN}./demo.sh custom \"prompt\"${NC}  — Run with your own prompt"
    echo ""
    echo -e "${BOLD}SCENARIOS:${NC}"
    echo -e "  1 — EPFO pension delay (6 months pending)"
    echo -e "  2 — Passport not issued (4 months, PV done)"
    echo -e "  3 — Income tax refund stuck"
    echo -e "  4 — RTI unanswered — file First Appeal"
    echo -e "  5 — Ration card delay (Rajasthan state RTI)"
    echo ""
}

# ─── Main ───────────────────────────────────────────────────────

print_header

case "${1:-interactive}" in
    "quick")
        check_prerequisites
        validate_agent
        test_python_scripts
        show_sample_output
        echo -e "${GREEN}${BOLD}✅ Quick demo complete! Agent is ready to run.${NC}"
        echo ""
        echo -e "To run the full agent:"
        echo -e "${CYAN}  gitclaw --dir . \"My EPFO pension hasn't started. Help me file RTI.\"${NC}"
        ;;

    "scenario")
        check_prerequisites
        validate_agent
        SCENARIOS=(
            ""
            "My EPFO pension claim for UAN 100XXXXXXXXX has been pending 6 months since I retired from Infosys in October 2025. I'm 62 years old and need this money. Help me file RTI."
            "I submitted my passport application in November 2025. Police verification was completed in January 2026. It's now April and still no passport. Please help me file an RTI."
            "My income tax refund of Rs 45,000 for AY 2024-25 has not been received. ITR was filed in July 2024 and refund was supposed to be processed. Help me file RTI to find out the status."
            "I filed an RTI with EPFO 42 days ago about my PF withdrawal. No response received. I need to file a First Appeal now."
            "I applied for a new ration card in Jaipur, Rajasthan 8 months ago. They always say 'under process'. I have an acknowledgment number but no update. Help me file RTI."
        )

        DESCRIPTIONS=(
            ""
            "EPFO Pension Delay — 6 months post-retirement"
            "Passport Not Issued — Police Verification Done"
            "Income Tax Refund Stuck — AY 2024-25"
            "First Appeal — RTI Unanswered after 42 days"
            "Ration Card Delay — Rajasthan State RTI"
        )

        NUM="${2:-1}"
        if [ -n "${SCENARIOS[$NUM]}" ]; then
            run_demo_scenario "$NUM" "${SCENARIOS[$NUM]}" "${DESCRIPTIONS[$NUM]}"
        else
            echo -e "${RED}Invalid scenario number. Choose 1-5.${NC}"
            show_usage
        fi
        ;;

    "custom")
        check_prerequisites
        validate_agent
        PROMPT="${2:-}"
        if [ -z "$PROMPT" ]; then
            echo -e "${RED}Please provide a prompt: ./demo.sh custom \"your prompt here\"${NC}"
            exit 1
        fi
        print_scenario "Custom" "$PROMPT"
        gitclaw --dir "$AGENT_DIR" "$PROMPT"
        ;;

    "help"|"--help"|"-h")
        show_usage
        ;;

    *)
        # Interactive mode
        check_prerequisites
        validate_agent
        test_python_scripts
        show_sample_output

        echo -e "${BOLD}${GREEN}Agent is ready! Choose a demo scenario:${NC}"
        echo ""
        echo -e "  ${CYAN}1${NC}) EPFO pension not started (6 months)"
        echo -e "  ${CYAN}2${NC}) Passport delay (police verification done)"
        echo -e "  ${CYAN}3${NC}) Income tax refund stuck"
        echo -e "  ${CYAN}4${NC}) RTI unanswered → First Appeal"
        echo -e "  ${CYAN}5${NC}) Ration card delay (Rajasthan)"
        echo -e "  ${CYAN}c${NC}) Custom prompt"
        echo -e "  ${CYAN}q${NC}) Quit"
        echo ""

        while true; do
            echo -n -e "${YELLOW}Enter choice [1-5/c/q]: ${NC}"
            read -r choice

            SCENARIOS=(
                ""
                "My EPFO pension claim for UAN 100XXXXXXXXX has been pending for 6 months. I retired from my company in October 2025. My name is Ramesh Kumar and I live at 45 Gandhi Nagar, Jaipur, Rajasthan 302015. Help me file an RTI."
                "My passport application submitted in November 2025 still hasn't been issued. Police verification was completed in January 2026. My name is Priya Sharma, 22 MG Road, Jaipur 302001. Please file an RTI."
                "My income tax refund of Rs 38,500 for AY 2024-25 is still pending. I filed my ITR in July 2024. Name: Amit Gupta, 67 Vaishali Nagar, Jaipur 302021. Help me file RTI with income tax."
                "I filed an RTI with EPFO Jaipur office 42 days ago. No response received. The RTI was about my PF withdrawal status. Help me draft the First Appeal now."
                "I applied for a new ration card in Sanganer, Jaipur 8 months ago. They keep saying 'under process'. My acknowledgment number is RC2025001234. Name: Sunita Devi, 12 Sanganer Bazar, Jaipur 302020."
            )

            case "$choice" in
                1|2|3|4|5)
                    run_demo_scenario "$choice" "${SCENARIOS[$choice]}" "Scenario $choice"
                    ;;
                c|C)
                    echo -n -e "${YELLOW}Enter your RTI prompt: ${NC}"
                    read -r custom_prompt
                    gitclaw --dir "$AGENT_DIR" "$custom_prompt"
                    ;;
                q|Q)
                    echo -e "${GREEN}Goodbye! Jai Hind. 🇮🇳${NC}"
                    exit 0
                    ;;
                *)
                    echo -e "${RED}Invalid choice${NC}"
                    ;;
            esac

            echo ""
            echo -n -e "${YELLOW}Run another scenario? [y/n]: ${NC}"
            read -r again
            [[ "$again" =~ ^[Yy]$ ]] || break
        done
        ;;
esac
