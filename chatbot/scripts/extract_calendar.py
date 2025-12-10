from chatbot.utils.pdf_reader import pdf_to_text
import os

BASE = os.path.dirname(os.path.dirname(__file__))
PDF = os.path.join(BASE, "data", "calendar", "calendar.pdf")
OUT = os.path.join(BASE, "data", "calendar_extracted.txt")

res = pdf_to_text(PDF, OUT)
if res is None:
    print("PDF not found or extraction failed")
else:
    print(f"Extracted {len(res)} characters to {OUT}")
