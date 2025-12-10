import sys
import os
import re
import traceback

proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from chatbot import rag_engine as rg

out_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'run_se_unit_test_output.txt')

try:
    q = 'second unit software engineering'
    subject = rg.detect_subject(q)
    unit = rg.detect_unit(q)
    stores = rg.load_syllabus_stores()

    lines = []
    lines.append(f"Query: {q}")
    lines.append(f"Detected subject: {subject}")
    lines.append(f"Detected unit: {unit}")

    store = stores.get(subject)
    if store is None:
        store = stores.get(subject + ' syllabus')

    if store is None:
        lines.append(f"No store found for subject {subject}")
    else:
        candidates = store.similarity_search(q, k=12)
        lines.append(f"Candidates: {len(candidates)}")
        roman_map = {1:'i',2:'ii',3:'iii',4:'iv',5:'v',6:'vi'}
        word_map = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six'}
        for i,d in enumerate(candidates):
            txt = (d.page_content or '')
            low = txt.lower()
            match_unit = False
            if unit:
                requested_roman = roman_map.get(unit)
                requested_word = word_map.get(unit)
                if re.search(rf"unit\W*{unit}\b", low):
                    match_unit = True
                if requested_word and re.search(rf"unit\W*{requested_word}\b", low):
                    match_unit = True
                if requested_roman and (re.search(rf"unit\W*{requested_roman}\b", low) or re.search(rf"(?m)^\s*{requested_roman}\b", low)):
                    match_unit = True
            lines.append(f"--- Candidate {i} match_unit={match_unit} ---")
            lines.append(txt[:2000])
            lines.append('\n')

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Wrote output to {out_path}")

except Exception:
    tb = traceback.format_exc()
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('ERROR:\n')
        f.write(tb)
    print(f"Error occurred; wrote traceback to {out_path}")
