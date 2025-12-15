#!/bin/bash
# check.sh

set -e  # Exit on error

echo "🧪 Running test suite..."
echo ""

# 1. Generate fresh data
echo "Step 1: Generating test data..."
python scripts/generate_test_data.py
echo ""

# 2. Run the tool against it
echo "Step 2: Running converter..."
python main.py -i test_input.zip -o test_output.pdf
echo ""

# 3. Verify output exists
echo "Step 3: Verifying output..."
if [ -f "test_output.pdf" ]; then
    echo "✅ Success! PDF created."
    ls -lh test_output.pdf
else
    echo "❌ Failed! PDF missing."
    exit 1
fi
