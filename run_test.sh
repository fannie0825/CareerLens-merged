#!/bin/bash
# Quick test script for resume generation

echo "=========================================="
echo "Resume Generation Test Suite"
echo "=========================================="
echo ""

# Check dependencies
echo "1. Checking dependencies..."
python3 -c "import streamlit, requests, numpy, sklearn" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ All dependencies installed"
else
    echo "   ❌ Missing dependencies. Run: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "2. Running prompt generation test..."
python3 test_resume_generation.py
if [ $? -eq 0 ]; then
    echo "   ✅ Prompt generation test passed"
else
    echo "   ❌ Prompt generation test failed"
    exit 1
fi

echo ""
echo "3. Running integration test..."
python3 test_resume_integration.py
if [ $? -eq 0 ]; then
    echo "   ✅ Integration test passed"
else
    echo "   ❌ Integration test failed"
    exit 1
fi

echo ""
echo "4. Checking secrets configuration..."
if [ -f ".streamlit/secrets.toml" ]; then
    echo "   ✅ secrets.toml found"
    # Check if keys are set (not just placeholders)
    if grep -q "your_key\|your-website" .streamlit/secrets.toml; then
        echo "   ⚠️  secrets.toml contains placeholder values"
        echo "   ⚠️  Update with actual API keys to test full functionality"
    else
        echo "   ✅ secrets.toml appears to have real keys"
    fi
else
    echo "   ⚠️  secrets.toml not found"
    echo "   ⚠️  Create .streamlit/secrets.toml with API keys to test full functionality"
    echo "   💡 Copy from: .streamlit/secrets.toml.example"
fi

echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "✅ Code logic: Working"
echo "✅ Prompt generation: Working"
echo "✅ Data structures: Valid"
if [ -f ".streamlit/secrets.toml" ] && ! grep -q "your_key\|your-website" .streamlit/secrets.toml; then
    echo "✅ API configuration: Ready"
    echo ""
    echo "🚀 To run the app:"
    echo "   streamlit run app.py"
else
    echo "⚠️  API configuration: Needs setup"
    echo ""
    echo "📝 To test with real API:"
    echo "   1. Create .streamlit/secrets.toml"
    echo "   2. Add your Azure OpenAI and RapidAPI keys"
    echo "   3. Run: streamlit run app.py"
fi
echo "=========================================="
