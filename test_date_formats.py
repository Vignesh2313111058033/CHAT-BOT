#!/usr/bin/env python
"""Test different date formats."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from chatbot.calendar_parser import get_day_info_for_query, _parse_date_from_query

# Test date parsing
test_dates = [
    'what is day order on 10-12-2025',  # DD-MM-YYYY
    'day order for 10-12-2025',
    'day order 10 december 2025',
    'what is the day order on 2025-12-10',  # YYYY-MM-DD (current format)
    '10-12-2025',
    '10/12/2025',
]

print("Testing date parsing...")
for query in test_dates:
    parsed = _parse_date_from_query(query)
    result = get_day_info_for_query(query)
    print(f"\nQuery: '{query}'")
    print(f"  Parsed date: {parsed}")
    print(f"  Result: {result}")
