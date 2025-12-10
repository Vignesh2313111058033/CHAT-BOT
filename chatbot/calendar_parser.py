import os
import json
import re
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CAL_TXT = os.path.join(BASE, "data", "calendar_extracted.txt")


def _load_calendar():
    if not os.path.exists(CAL_TXT):
        return {}

    with open(CAL_TXT, "rb") as f:
        raw_bytes = f.read()

    # If there are null bytes it's likely UTF-16-LE/BE
    if b'\x00' in raw_bytes:
        for enc in ('utf-16-le', 'utf-16-be', 'utf-16'):
            try:
                raw = raw_bytes.decode(enc)
                break
            except Exception:
                raw = None
        if raw is None:
            raw = raw_bytes.decode('utf-8', 'ignore')
    else:
        try:
            raw = raw_bytes.decode('utf-8')
        except Exception:
            try:
                raw = raw_bytes.decode('utf-16')
            except Exception:
                raw = raw_bytes.decode('utf-8', 'ignore')

    # Try to extract JSON part — file appears to be JSON-like
    # Find first '{' and last '}' to get JSON text
    start = raw.find('{')
    end = raw.rfind('}')
    if start == -1 or end == -1:
        return {}

    jtext = raw[start:end+1]

    try:
        data = json.loads(jtext)
    except Exception:
        # As a fallback, attempt to fix common issues (trailing commas)
        jtext_fixed = jtext.replace('\xa0', ' ')
        jtext_fixed = re.sub(r",\s*\]", "]", jtext_fixed)
        jtext_fixed = re.sub(r",\s*\}", "}", jtext_fixed)
        try:
            data = json.loads(jtext_fixed)
        except Exception:
            # Final fallback: parse individual entry objects with regex
            date_map = {}
            # find blocks that look like {..."date": "YYYY-MM-DD"...}
            # match object blocks that contain date: "YYYY-MM-DD" (allow unquoted keys)
            for m in re.finditer(r"\{[^}]*date\s*:\s*\"(20\\d{2}-\\d{2}-\\d{2})\"[^}]*\}", jtext_fixed):
                block = m.group(0)
                date = m.group(1)
                day = None
                day_order = None
                working = None
                event = None

                md = re.search(r'\"day\"\s*:\s*\"([^\"]+)\"', block)
                if md:
                    day = md.group(1)

                mo = re.search(r'\"day_order\"\s*:\s*(null|\d+)', block)
                if mo:
                    day_order = None if mo.group(1) == 'null' else int(mo.group(1))

                mw = re.search(r'\"working_day_number\"\s*:\s*(null|\d+)', block)
                if mw:
                    working = None if mw.group(1) == 'null' else int(mw.group(1))

                me = re.search(r'\"event\"\s*:\s*(null|\"([^\"]*)\")', block)
                if me:
                    if me.group(1) == 'null':
                        event = None
                    else:
                        event = me.group(2)

                date_map[date] = {
                    'date': date,
                    'day': day,
                    'day_order': day_order,
                    'working_day_number': working,
                    'event': event,
                }

            return date_map

    # Flatten entries into date->entry map
    date_map = {}
    for month, entries in data.items():
        for e in entries:
            d = e.get("date")
            if d:
                date_map[d] = e

    return date_map


# Cache on import (lazy)
_CAL_MAP = None


def _parse_date_from_query(q):
    q = q.lower()

    # Try YYYY-MM-DD first
    m = re.search(r"(20\d{2})[-/](\d{1,2})[-/](\d{1,2})", q)
    if m:
        y, mo, da = m.groups()
        try:
            return datetime(int(y), int(mo), int(da)).date().isoformat()
        except Exception:
            pass

    # Try DD-MM-YYYY or DD/MM/YYYY format
    # Check if the numbers look like DD-MM-YYYY (first number <= 31, second number <= 12)
    m_ddmmyyyy = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](20\d{2})", q)
    if m_ddmmyyyy:
        da, mo, y = m_ddmmyyyy.groups()
        da_int = int(da)
        mo_int = int(mo)
        # Heuristic: if day > 12, it's definitely DD-MM, if month > 12, it's definitely MM-DD
        # Otherwise try DD-MM first as it's more common in many regions
        if da_int <= 31 and mo_int <= 12:
            try:
                # Try as DD-MM-YYYY
                return datetime(int(y), mo_int, da_int).date().isoformat()
            except Exception:
                # If that fails, try as MM-DD-YYYY
                try:
                    return datetime(int(y), da_int, mo_int).date().isoformat()
                except Exception:
                    pass

    # D Month YYYY or D Month
    months = {
        'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
        'july':7,'august':8,'september':9,'october':10,'november':11,'december':12
    }

    m2 = re.search(r"(\d{1,2})\s+([a-zA-Z]+)(?:\s+(20\d{2}))?", q)
    if m2:
        da, mon, y = m2.groups()
        mon_l = mon.lower()
        if mon_l in months:
            year = int(y) if y else datetime.today().year
            try:
                return datetime(year, months[mon_l], int(da)).date().isoformat()
            except Exception:
                pass

    # 'today'
    if 'today' in q:
        return datetime.today().date().isoformat()

    return None


def get_day_info_for_query(query):
    """Return a human-friendly answer for queries asking about day order/working day.

    Examples handled:
    - "what is the day order on 2025-12-05"
    - "day order for 5 December"
    - "what is the working day on monday"
    - "today's day order"
    """
    global _CAL_MAP
    if _CAL_MAP is None:
        _CAL_MAP = _load_calendar()

    q = query.lower()

    # Try to parse an explicit date
    date_key = _parse_date_from_query(q)
    if date_key:
        # First try the in-memory map
        if _CAL_MAP and date_key in _CAL_MAP:
            entry = _CAL_MAP[date_key]
            day = entry.get('day')
            day_order = entry.get('day_order')
            working = entry.get('working_day_number')
            event = entry.get('event')
            parts = []
            if day:
                parts.append(f"Day: {day}")
            if day_order is not None:
                parts.append(f"Day order: {day_order}")
            if working is not None:
                parts.append(f"Working-day number: {working}")
            if event:
                parts.append(f"Event: {event}")
            return ", ".join(parts)

        # Next try direct file search in calendar_extracted.txt (robust simple fallback)
        try:
            if os.path.exists(CAL_TXT):
                with open(CAL_TXT, 'r', encoding='utf-8') as f:
                    txt = f.read()
                if date_key in txt:
                    # Find the exact entry object containing this date
                    # Match {... "date": "YYYY-MM-DD" ...}
                    pattern = r'\{[^}]*"date"\s*:\s*"' + re.escape(date_key) + r'"[^}]*\}'
                    m = re.search(pattern, txt)
                    if m:
                        entry_block = m.group(0)
                        # Now extract day, day_order, and event from this specific block
                        md = re.search(r'"day"\s*:\s*"([^"]+)"', entry_block)
                        mo = re.search(r'"day_order"\s*:\s*(null|\d+)', entry_block)
                        me = re.search(r'"event"\s*:\s*(null|"([^"]*)")', entry_block)
                        
                        day = md.group(1) if md else None
                        day_order = None if (not mo or mo.group(1) == 'null') else int(mo.group(1))
                        event = None
                        if me and me.group(1) != 'null':
                            event = me.group(2)
                        
                        parts = []
                        if day:
                            parts.append(f"Day: {day}")
                        if day_order is not None:
                            parts.append(f"Day order: {day_order}")
                        if event:
                            parts.append(f"Event: {event}")
                        return ", ".join(parts)
        except Exception:
            pass

        # Fallback: try to search the FAISS calendar vectorstore to find a matching passage
        try:
            from langchain_community.vectorstores import FAISS
            from langchain_community.embeddings import HuggingFaceEmbeddings
            vs_path = os.path.join(os.path.dirname(__file__), 'vectorstores', 'calendar')
            embedder = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
            if os.path.exists(vs_path):
                store = FAISS.load_local(vs_path, embedder, allow_dangerous_deserialization=True)
                docs = store.similarity_search(date_key, k=4)
                for d in docs:
                    txt = d.page_content
                    # try to find the date token or yyyy-mm-dd inside text
                    if date_key in txt:
                        # find day_order nearby
                        m = re.search(r'"?day_order"?\s*[:]\s*(null|\d+)', txt)
                        mo = None
                        if m:
                            mo = None if m.group(1) == 'null' else int(m.group(1))
                        # find day
                        md = re.search(r'"?day"?\s*[:]\s*"?([A-Za-z]{3,9})"?', txt)
                        day = md.group(1) if md else None
                        return f"Day: {day}, Day order: {mo}"
        except Exception:
            pass

        # Year-agnostic fallback: try the same month-day in adjacent years
        try:
            y, m, d = date_key.split('-')
            for delta in (1, -1):
                alt_year = str(int(y) + delta)
                alt_key = f"{alt_year}-{m}-{d}"
                if _CAL_MAP and alt_key in _CAL_MAP:
                    entry = _CAL_MAP[alt_key]
                    day = entry.get('day')
                    day_order = entry.get('day_order')
                    event = entry.get('event')
                    parts = []
                    if day:
                        parts.append(f"Day: {day}")
                    if day_order is not None:
                        parts.append(f"Day order: {day_order}")
                    if event:
                        parts.append(f"Event: {event}")
                    return (f"Date {date_key} not found. Closest match {alt_key}: " + ", ".join(parts))

                # also try direct text search for the alt_key in file
                if os.path.exists(CAL_TXT):
                    with open(CAL_TXT, 'r', encoding='utf-8') as f:
                        txt = f.read()
                    if alt_key in txt:
                        pattern = r'\{[^}]*"date"\s*:\s*"' + re.escape(alt_key) + r'"[^}]*\}'
                        m = re.search(pattern, txt)
                        if m:
                            entry_block = m.group(0)
                            md = re.search(r'"day"\s*:\s*"([^\"]+)"', entry_block)
                            mo = re.search(r'"day_order"\s*:\s*(null|\d+)', entry_block)
                            me = re.search(r'"event"\s*:\s*(null|"([^\"]*)")', entry_block)
                            day = md.group(1) if md else None
                            day_order = None if (not mo or mo.group(1) == 'null') else int(mo.group(1))
                            event = None
                            if me and me.group(1) != 'null':
                                event = me.group(2)
                            parts = []
                            if day:
                                parts.append(f"Day: {day}")
                            if day_order is not None:
                                parts.append(f"Day order: {day_order}")
                            if event:
                                parts.append(f"Event: {event}")
                            return (f"Date {date_key} not found. Closest match {alt_key}: " + ", ".join(parts))
        except Exception:
            pass

    # If user asked by weekday name (e.g., 'monday'), try to find next matching date in calendar
    weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    for wd in weekdays:
        if wd in q:
            # find first calendar entry matching weekday name
            for d, entry in sorted(_CAL_MAP.items()):
                if entry.get('day') and entry.get('day').lower().startswith(wd[:3]):
                    eo = entry.get('day_order')
                    return f"{wd.title()} on {d}: Day order {eo} (event: {entry.get('event')})"

    return None
