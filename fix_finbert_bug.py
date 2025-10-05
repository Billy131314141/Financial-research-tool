#!/usr/bin/env python3
"""Fix the missing 'detailed_results' key bug in FinBERT sentiment analyzer"""

import sys

print("🔧 Fixing FinBERT sentiment analyzer bug...")

# Read the file
with open('src/analysis/finbert_sentiment.py', 'r') as f:
    lines = f.readlines()

# Find and fix the bug (around line 149)
fixed = False
for i, line in enumerate(lines):
    # Look for the line with 'neutral_percentage': 0.0
    if "'neutral_percentage': 0.0" in line and i > 135 and i < 155:
        # Check if the next line doesn't already have detailed_results
        if i + 1 < len(lines) and 'detailed_results' not in lines[i + 1]:
            # Add detailed_results after this line
            indent = ' ' * 16  # Match indentation
            lines.insert(i + 1, f"{indent}'detailed_results': []\n")
            fixed = True
            print(f"✅ Fixed at line {i + 1}: Added 'detailed_results': []")
            break

if fixed:
    # Write back
    with open('src/analysis/finbert_sentiment.py', 'w') as f:
        f.writelines(lines)
    print("✅ Bug fixed successfully!")
else:
    print("⚠️  Bug may already be fixed or line not found")

sys.exit(0)


