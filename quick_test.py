from chatbot.calendar_parser import _parse_date_from_query, get_day_info_for_query

print("Testing date format: 10-12-2025")
parsed = _parse_date_from_query('10-12-2025')
print(f"Parsed to: {parsed}")

if parsed:
    result = get_day_info_for_query('day order for 10-12-2025')
    print(f"Query result: {result}")
else:
    print("Failed to parse date")

# Also test the expected date
print("\n\nTesting date format: 2025-12-10 (YYYY-MM-DD)")
parsed2 = _parse_date_from_query('2025-12-10')
print(f"Parsed to: {parsed2}")
result2 = get_day_info_for_query('day order 2025-12-10')
print(f"Query result: {result2}")
