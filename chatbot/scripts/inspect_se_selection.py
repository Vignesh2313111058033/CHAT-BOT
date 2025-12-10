import sys
import os
# ensure project root is on sys.path so 'chatbot' package can be imported when running as script
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

import re
from chatbot import rag_engine as rg

q = 'second unit software engineering'
print('Query:', q)

stores = rg.load_syllabus_stores()
subject = rg.detect_subject(q)
unit = rg.detect_unit(q)
print('Detected subject:', subject)
print('Detected unit:', unit)

if subject is None:
    print('No subject detected.')
    raise SystemExit(1)

store = stores.get(subject)
if store is None:
    # try folder name fallback
    store = stores.get(subject + ' syllabus')

if store is None:
    print('No store found for subject', subject)
    raise SystemExit(1)

# emulate the selection logic used in answer_question for subject+unit
if unit:
    candidates = store.similarity_search(q, k=12)
    unit_matches = []
    for d in candidates:
        txt = (d.page_content or '').lower()
        matched = False
        if re.search(rf"unit\W*{unit}\b", txt):
            matched = True
        # words and romans handled inside rag_engine helper logic, reuse that by importing functions
    
    # Use the engine's internal selection by calling answer_question but avoid LLM call by
    # printing the top candidate passages and whether they match unit heuristics.
    print('\nCandidates:')
    for i,d in enumerate(candidates):
        txt = (d.page_content or '')
        low = txt.lower()
        match_unit = False
        if rg.detect_unit(q) == unit:
            # reuse detection heuristics from rag_engine
            requested_roman = {1:'i',2:'ii',3:'iii',4:'iv',5:'v',6:'vi'}.get(unit)
            requested_word = {1:'one',2:'two',3:'three',4:'four',5:'five',6:'six'}.get(unit)
            if re.search(rf"unit\W*{unit}\b", low) or (requested_word and re.search(rf"unit\W*{requested_word}\b", low)):
                match_unit = True
            if requested_roman and (re.search(rf"unit\W*{requested_roman}\b", low) or re.search(rf"(?m)^\s*{requested_roman}\b", low)):
                match_unit = True
        print('--- Candidate', i, 'match_unit=', match_unit, '---')
        print(txt[:1200])
        print('\n')
else:
    docs = store.similarity_search(q, k=6)
    print('Top docs:')
    for i,d in enumerate(docs):
        print('--- DOC', i, '---')
        print(d.page_content[:1200])
        print('\n')
