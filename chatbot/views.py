from django.shortcuts import render
from django.http import JsonResponse
import os
import requests
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
GROQ_API_URL = "https://api.groq.com/v1/predict"

def home(request):
    return render(request, "chatbot/index.html")

# def ask_ai(request):
#     question = request.GET.get("q", "").lower()
#     if not question:
#         return JsonResponse({"error": "No question provided."})

#     file_path = None
#     keyword = None

#     # Determine which file to read
#     if "timetable" in question:
#         file_path = os.path.join(DATA_DIR, "timetable.txt")
#     elif "syllabus" in question:
#         file_path = os.path.join(DATA_DIR, "syllabus.txt")
#         # check if user asked for a specific semester
#         if "semester 1" in question:
#             keyword = "Semester 1:"
#         elif "semester 2" in question:
#             keyword = "Semester 2:"
#     elif "rule" in question or "policy" in question:
#         file_path = os.path.join(DATA_DIR, "rules.txt")

#     # Read file if exists
#     if file_path and os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()

#         # If keyword is set, extract only that part
#         if keyword:
#             # Split by semesters
#             parts = content.split("Semester")
#             for part in parts:
#                 if keyword.lower() in ("Semester" + part).lower():
#                     answer = "Semester" + part.strip()
#                     return JsonResponse({"answer": answer})
#             return JsonResponse({"answer": "No information found for that semester."})

#         return JsonResponse({"answer": content})

#     # Fallback to Groq API if not matched
#     headers = {
#         "Authorization": f"Bearer {settings.GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": "gpt-4o-mini",
#         "input": question
#     }

#     try:
#         response = requests.post(GROQ_API_URL, headers=headers, json=payload)
#         response.raise_for_status()
#         data = response.json()
#         answer = data.get("output", ["No answer received"])[0]
#         return JsonResponse({"answer": answer})
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({"error": str(e)})


# import os
# from django.http import JsonResponse


# def ask_ai(request):
#     question = request.GET.get("q", "").lower()
#     if not question:
#         return JsonResponse({"error": "No question provided."})

#     file_path = None
#     keyword = None

#     # Determine which file to read
#     if "timetable" in question or "class" in question or "schedule" in question:
#         file_path = os.path.join(DATA_DIR, "timetable.txt")
#     elif "syllabus" in question:
#         file_path = os.path.join(DATA_DIR, "syllabus.txt")
#         if "semester" in question:
#             for i in range(1, 10):
#                 if f"semester {i}" in question:
#                     keyword = f"Semester {i}:"
#                     break
#     elif "rule" in question or "policy" in question:
#         file_path = os.path.join(DATA_DIR, "rules.txt")

#     # Read file if exists
#     if file_path and os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()

#         # --------------------------
#         # TIMETABLE SEARCH BY DAY
#         # --------------------------
#         if file_path.endswith("timetable.txt"):
#             days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
#             for day in days:
#                 if day in question:
#                     # Split timetable by days
#                     parts = content.lower().split(day + ":")
#                     if len(parts) > 1:
#                         # Get the part after this day until next day or end
#                         remaining = parts[1]
#                         for next_day in days:
#                             if next_day != day and next_day + ":" in remaining:
#                                 remaining = remaining.split(next_day + ":")[0]
#                         schedule = remaining.strip()
#                         return JsonResponse({"answer": f"{day.capitalize()} schedule:\n{schedule}"})
#             # If no day found, return all timetable
#             return JsonResponse({"answer": content})

#         # --------------------------
#         # SYLLABUS SEARCH BY SEMESTER
#         # --------------------------
#         if file_path.endswith("syllabus.txt") and keyword:
#             parts = content.split("Semester")
#             for part in parts:
#                 if keyword.lower() in ("Semester" + part).lower():
#                     answer = "Semester" + part.strip()
#                     return JsonResponse({"answer": answer})
#             return JsonResponse({"answer": "No information found for that semester."})

#         # --------------------------
#         # RULES OR GENERAL FILE
#         # --------------------------
#         return JsonResponse({"answer": content})

#     # --------------------------
#     # FALLBACK
#     # --------------------------
#     return JsonResponse({"answer": "Sorry, I could not find the answer in the text files."})



# from datetime import datetime
 

# def ask_ai(request):
#     question = request.GET.get("q", "").lower()
#     if not question:
#         return JsonResponse({"error": "No question provided."})

#     file_path = None
#     keyword = None

#     # Determine which file to read
#     if "timetable" in question or "class" in question or "schedule" in question:
#         file_path = os.path.join(DATA_DIR, "timetable.txt")
#     elif "syllabus" in question:
#         file_path = os.path.join(DATA_DIR, "syllabus.txt")
#         if "semester" in question:
#             for i in range(1, 10):
#                 if f"semester {i}" in question:
#                     keyword = f"Semester {i}:"
#                     break
#     elif "rule" in question or "policy" in question:
#         file_path = os.path.join(DATA_DIR, "rules.txt")

#     # Read file if exists
#     if file_path and os.path.exists(file_path):
#         with open(file_path, "r", encoding="utf-8") as f:
#             content = f.read()

#         # --------------------------
#         # TIMETABLE SEARCH BY DAY
#         # --------------------------
#         if file_path.endswith("timetable.txt"):
#             days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
            
#             # Detect if user asked "today"
#             if "today" in question:
#                 today_index = datetime.today().weekday()  # Monday=0
#                 if today_index < len(days):
#                     day = days[today_index]
#                 else:
#                     day = "monday"  # fallback
#             else:
#                 # Check question for day
#                 day = None
#                 for d in days:
#                     if d in question:
#                         day = d
#                         break
#                 if not day:
#                     return JsonResponse({"answer": content})  # return full timetable

#             # Extract that day's schedule
#             parts = content.lower().split(day + ":")
#             if len(parts) > 1:
#                 remaining = parts[1]
#                 for next_day in days:
#                     if next_day != day and next_day + ":" in remaining:
#                         remaining = remaining.split(next_day + ":")[0]
#                 schedule = remaining.strip()
#                 return JsonResponse({"answer": f"{day.capitalize()} schedule:\n{schedule}"})
#             else:
#                 return JsonResponse({"answer": f"No schedule found for {day}."})

#         # --------------------------
#         # SYLLABUS SEARCH BY SEMESTER
#         # --------------------------
#         if file_path.endswith("syllabus.txt") and keyword:
#             parts = content.split("Semester")
#             for part in parts:
#                 if keyword.lower() in ("Semester" + part).lower():
#                     answer = "Semester" + part.strip()
#                     return JsonResponse({"answer": answer})
#             return JsonResponse({"answer": "No information found for that semester."})

#         # --------------------------
#         # RULES OR GENERAL FILE
#         # --------------------------
#         return JsonResponse({"answer": content})

#     # --------------------------
#     # FALLBACK
#     # --------------------------
#     return JsonResponse({"answer": "Sorry, I could not find the answer in the text files."})

# import os
# from datetime import datetime
# from django.http import JsonResponse
# from django.conf import settings
# from chatbot.utils.pdf_reader import pdf_to_text   # <-- PDF reader

 

# def ask_ai(request):
#     question = request.GET.get("q", "").lower()
#     if not question:
#         return JsonResponse({"error": "No question provided."})

#     file_path = None
#     keyword = None

#     # -------------------------------------------------
#     # Identify which dataset to use based on question
#     # -------------------------------------------------
#     if "timetable" in question or "class" in question or "schedule" in question:
#         file_path = os.path.join(DATA_DIR, "timetable.txt")

#     elif "syllabus" in question:
#         file_path = os.path.join(DATA_DIR, "syllabus.txt")

#         # detect semester number dynamically
#         if "semester" in question:
#             for i in range(1, 15):
#                 if f"semester {i}" in question:
#                     keyword = f"semester {i}:"
#                     break

#     elif "rule" in question or "policy" in question or "regulation" in question:
#         # PDF file instead of text
#         pdf_path = os.path.join(DATA_DIR, "rules.pdf")
#         pdf_text = pdf_to_text(pdf_path)

#         if pdf_text.strip() == "":
#             return JsonResponse({"answer": "Rules PDF not found or empty."})

#         # Search for specific rule keywords
#         rule_keywords = ["dress code", "attendance", "fees", "discipline", "exam rules"]

#         for word in rule_keywords:
#             if word in question:
#                 parts = pdf_text.lower().split(word)
#                 if len(parts) > 1:
#                     lines = parts[1].split("\n")
#                     return JsonResponse({
#                         "answer": word.upper() + ":\n" + "\n".join(lines[:6])
#                     })

#         # If no specific keyword → return full PDF text
#         return JsonResponse({"answer": pdf_text})

#     # -------------------------------------------------
#     # If no file selected → return fallback
#     # -------------------------------------------------
#     if not file_path:
#         return JsonResponse({"answer": "Sorry, I could not understand the question."})

#     # -------------------------------------------------
#     # Read text file (syllabus / timetable)
#     # -------------------------------------------------
#     if not os.path.exists(file_path):
#         return JsonResponse({"answer": "Data file missing: " + file_path})

#     with open(file_path, "r", encoding="utf-8") as f:
#         content = f.read()

#     # -------------------------------------------------
#     # TIMETABLE SYSTEM
#     # -------------------------------------------------
#     if file_path.endswith("timetable.txt"):
#         days = ["monday", "tuesday", "wednesday", "thursday", "friday"]

#         # 🎯 If user asks "today timetable"
#         if "today" in question:
#             today_idx = datetime.today().weekday()  # Monday=0
#             day = days[today_idx] if today_idx < len(days) else "monday"

#         else:
#             # Detect specific day
#             day = None
#             for d in days:
#                 if d in question:
#                     day = d
#                     break

#         # If no day found → return full timetable
#         if not day:
#             return JsonResponse({"answer": content})

#         # Extract only that day's portion
#         lower = content.lower()
#         if day + ":" not in lower:
#             return JsonResponse({"answer": f"No timetable found for {day.title()}."})

#         part = lower.split(day + ":")[1]

#         # Cut until next day starts
#         for other in days:
#             if other != day and other + ":" in part:
#                 part = part.split(other + ":")[0]
#                 break

#         timetable = part.strip()

#         return JsonResponse({
#             "answer": f"{day.title()} Timetable:\n{timetable}"
#         })

#     # -------------------------------------------------
#     # SYLLABUS SYSTEM
#     # -------------------------------------------------
#     if file_path.endswith("syllabus.txt") and keyword:
#         lower = content.lower()
#         parts = lower.split("semester")

#         for part in parts:
#             if keyword in ("semester" + part).lower():
#                 result = "Semester" + part.strip()
#                 return JsonResponse({"answer": result})

#         return JsonResponse({"answer": "No syllabus found for that semester."})

#     # -------------------------------------------------
#     # General text file (fallback)
#     # -------------------------------------------------
#     return JsonResponse({"answer": content})

from django.http import JsonResponse
from .rag_engine import answer_question
from .calendar_parser import get_day_info_for_query
from chatbot.utils.pdf_reader import pdf_to_text
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# Known PDF locations (handle case differences)
RULES_PDF = os.path.join(DATA_DIR, "rules.pdf")
RULES_TXT = os.path.join(DATA_DIR, "rules.txt")

CAL_PDF = os.path.join(DATA_DIR, "calendar", "calendar.pdf")
CAL_TXT = os.path.join(DATA_DIR, "calendar.txt")

TT_DIR = os.path.join(DATA_DIR, "TimeTable")
if not os.path.exists(TT_DIR):
    TT_DIR = os.path.join(DATA_DIR, "timetable")

TT_PDF = None
if os.path.exists(TT_DIR):
    # find a pdf inside timetable folder
    for f in os.listdir(TT_DIR):
        if f.lower().endswith('.pdf'):
            TT_PDF = os.path.join(TT_DIR, f)
            break

TT_TXT = os.path.join(DATA_DIR, "timetable.txt")


# Convert PDFs → text only once (if present)
if os.path.exists(RULES_PDF) and not os.path.exists(RULES_TXT):
    pdf_to_text(RULES_PDF, RULES_TXT)

if os.path.exists(CAL_PDF) and not os.path.exists(CAL_TXT):
    pdf_to_text(CAL_PDF, CAL_TXT)

if TT_PDF and not os.path.exists(TT_TXT):
    pdf_to_text(TT_PDF, TT_TXT)


def _extract_day_from_timetable(question):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    if "today" in question:
        today_idx = datetime.today().weekday()  # Monday=0
        if today_idx < len(days):
            return days[today_idx]

    for d in days:
        if d in question:
            return d

    return None


def ask_ai(request):
    q = request.GET.get("q", "").lower()
    if not q:
        return JsonResponse({"error": "No question"})

    # TIMETABLE quick-path: try to answer from timetable text without calling RAG
    if any(k in q for k in ["timetable", "time table", "class", "schedule"]):
        if os.path.exists(TT_TXT):
            with open(TT_TXT, "r", encoding="utf-8") as f:
                content = f.read().lower()

            day = _extract_day_from_timetable(q)
            if not day:
                # return full timetable
                return JsonResponse({"answer": content})

            marker = day + ":"
            if marker not in content:
                return JsonResponse({"answer": f"No timetable found for {day.title()}."})

            part = content.split(marker, 1)[1]
            # cut until next day marker
            for other in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                if other != day and other + ":" in part:
                    part = part.split(other + ":")[0]
                    break

            timetable = part.strip()
            return JsonResponse({"answer": f"{day.title()} Timetable:\n{timetable}"})

    # CALENDAR quick-path: look for working-day/holiday mentions in calendar text
    if any(k in q for k in ["calendar", "working day", "holiday", "exam date", "semester start", "day order"]):
        # Use structured calendar parser when possible
        info = get_day_info_for_query(q)
        if info:
            return JsonResponse({"answer": info})

        # fallback: if extraction to CAL_TXT exists, return a short keyword excerpt
        if os.path.exists(CAL_TXT):
            with open(CAL_TXT, "rb") as f:
                cal_text = f.read().decode("utf-8", "ignore").lower()

            keywords = ["working day", "holiday", "exam", "last date", "start"]
            for kw in keywords:
                if kw in q and kw in cal_text:
                    idx = cal_text.find(kw)
                    excerpt = cal_text[idx: idx + 400]
                    return JsonResponse({"answer": excerpt})

    # Fallback to RAG engine for other questions (or when quick-path didn't match)
    response = answer_question(q)
    return JsonResponse({"answer": response})

