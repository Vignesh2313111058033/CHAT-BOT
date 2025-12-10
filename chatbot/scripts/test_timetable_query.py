import sys
import os
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

from chatbot import rag_engine as rg

q = 'what is the timetable for day 1'
print('Query:', q)

stores = rg.load_syllabus_stores()
misc_stores = rg.load_misc_stores()

print('Detected subject:', rg.detect_subject(q))
print('Detected unit:', rg.detect_unit(q))

# Since no subject is detected, it should search misc stores (timetable)
timetable_store = misc_stores.get('timetable')
if timetable_store:
    docs = timetable_store.similarity_search(q, k=4)
    print(f'\nTimetable vectorstore returned {len(docs)} docs:\n')
    for i, d in enumerate(docs):
        print(f'--- DOC {i} ---')
        print(d.page_content)
        print('\n')
else:
    print('Timetable store not found')
