#!/bin/bash

# StyleSense.AI Setup Verification Script
# This script checks if all required components are properly set up

echo "🔍 StyleSense.AI Setup Verification"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track overall status
all_good=true

# Function to check command existence
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed ($($1 --version 2>&1 | head -n1))"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is not installed"
        all_good=false
        return 1
    fi
}

# Function to check file existence
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 not found"
        all_good=false
        return 1
    fi
}

# Function to check directory existence
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 not found"
        all_good=false
        return 1
    fi
}

echo "1. Checking Prerequisites"
echo "-------------------------"
check_command python3
check_command node
check_command npm
check_command git
echo ""

echo "2. Checking Project Structure"
echo "-----------------------------"
check_dir "backend"
check_dir "frontend"
check_dir "ml-models"
check_dir "datasets"
check_dir "docs"
echo ""

echo "3. Checking Backend Files"
echo "------------------------"
check_file "backend/app.py"
check_file "backend/config.py"
check_file "backend/database.py"
check_file "backend/requirements.txt"
check_file "backend/.env.example"
echo ""

echo "4. Checking Frontend Files"
echo "--------------------------"
check_file "frontend/package.json"
check_file "frontend/src/App.js"
check_file "frontend/src/index.js"
check_file "frontend/tailwind.config.js"
echo ""

echo "5. Checking ML Models"
echo "--------------------"
check_file "ml-models/body_detection.py"
check_file "ml-models/recommendation_engine.py"
check_file "ml-models/ar_tryon.py"
check_file "ml-models/segmentation.py"
echo ""

echo "6. Checking Documentation"
echo "------------------------"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "CONTRIBUTING.md"
check_file "docs/system_design.md"
check_file "docs/api_specification.md"
check_file "docs/project_timeline.md"
echo ""

echo "7. Checking Configuration"
echo "------------------------"
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓${NC} backend/.env exists"
    
    # Check for required variables
    if grep -q "MONGODB_URI" backend/.env; then
        echo -e "${GREEN}  ✓${NC} MONGODB_URI is set"
    else
        echo -e "${YELLOW}  ⚠${NC} MONGODB_URI not found in .env"
    fi
    
    if grep -q "FLASK_SECRET_KEY" backend/.env; then
        echo -e "${GREEN}  ✓${NC} FLASK_SECRET_KEY is set"
    else
        echo -e "${YELLOW}  ⚠${NC} FLASK_SECRET_KEY not found in .env"
    fi
else
    echo -e "${YELLOW}⚠${NC} backend/.env not found (copy from .env.example)"
fi
echo ""

echo "8. Python Syntax Check"
echo "---------------------"
if command -v python3 &> /dev/null; then
    python_files=$(find backend ml-models -name "*.py" -type f)
    syntax_errors=0
    
    for file in $python_files; do
        if python3 -m py_compile "$file" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $file"
        else
            echo -e "${RED}✗${NC} $file has syntax errors"
            syntax_errors=$((syntax_errors + 1))
            all_good=false
        fi
    done
    
    if [ $syntax_errors -eq 0 ]; then
        echo -e "${GREEN}All Python files have valid syntax${NC}"
    fi
else
    echo -e "${YELLOW}⚠${NC} Python3 not available, skipping syntax check"
fi
echo ""

echo "9. Package Dependencies"
echo "----------------------"
if [ -d "backend/venv" ]; then
    echo -e "${GREEN}✓${NC} Python virtual environment exists"
else
    echo -e "${YELLOW}⚠${NC} Python virtual environment not found"
    echo -e "  Run: cd backend && python -m venv venv"
fi

if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✓${NC} Node modules installed"
else
    echo -e "${YELLOW}⚠${NC} Node modules not installed"
    echo -e "  Run: cd frontend && npm install"
fi
echo ""

echo "=================================="
echo ""

if [ "$all_good" = true ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Set up backend/.env (copy from .env.example)"
    echo "2. Install backend dependencies: cd backend && pip install -r requirements.txt"
    echo "3. Install frontend dependencies: cd frontend && npm install"
    echo "4. Start backend: cd backend && python app.py"
    echo "5. Start frontend: cd frontend && npm start"
    echo ""
    echo "See QUICKSTART.md for detailed instructions."
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    echo ""
    echo "Please fix the issues above before proceeding."
    echo "See README.md and QUICKSTART.md for setup instructions."
    exit 1
fi
