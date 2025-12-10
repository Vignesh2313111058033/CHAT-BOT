#!/usr/bin/env python
"""Test script to verify calendar parser fixes."""

import sys
import os

# Add repo root to path
sys.path.insert(0, os.path.dirname(__file__))

from chatbot.calendar_parser import get_day_info_for_query

test_cases = [
    ('what is the day order on 2025-12-05', 'Fri', 4),
    ('what is the day order on 2025-12-08', 'Mon', 6),
    ('day order 2025-12-01', 'Mon', 6),
    ('day order 2025-12-02', 'Tue', 1),
]

print("Testing calendar parser...")
for query, expected_day, expected_order in test_cases:
    result = get_day_info_for_query(query)
    print(f"\nQuery: {query}")
    print(f"Result: {result}")
    print(f"Expected: Day: {expected_day}, Day order: {expected_order}")
    
    if result and expected_day in result and str(expected_order) in result:
        print("✓ PASS")
    else:
        print("✗ FAIL")
