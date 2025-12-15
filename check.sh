#!/bin/bash
# test.sh

# 1. Generate fresh data
python scripts/generate_test_data.py

# 2. Run the tool against it
python main.py -i test_input.zip -o test_output.pdf

# 3. Verify output exists
if [ -f "test_output.pdf" ]; then
    echo "✅ Success! PDF created."
else
    echo "❌ Failed! PDF missing."
    exit 1
fi
