import re

fn = 'chatbot/data/calendar_extracted.txt'
txt = open(fn,'rb').read().decode('utf-8','ignore')

dates = re.finditer(r'(20\d{2}-\d{2}-\d{2})', txt)
mapping = {}
for m in dates:
    d = m.group(1)
    start = max(0, m.start()-200)
    end = min(len(txt), m.end()+200)
    block = txt[start:end]
    # find day
    day_m = re.search(r'\"?day\"?\s*[:]\s*\"?([A-Za-z]{3,9})\"?', block)
    order_m = re.search(r'\"?day_order\"?\s*[:]\s*(null|\d+)', block)
    work_m = re.search(r'\"?working_day_number\"?\s*[:]\s*(null|\d+)', block)
    event_m = re.search(r'\"?event\"?\s*[:]\s*(null|\"([^\"]*)\")', block)
    day = day_m.group(1) if day_m else None
    order = None if (not order_m or order_m.group(1)=='null') else int(order_m.group(1))
    work = None if (not work_m or work_m.group(1)=='null') else int(work_m.group(1))
    event = None
    if event_m:
        if event_m.group(1) != 'null':
            event = event_m.group(2)

    mapping[d] = {'day': day, 'day_order': order, 'working_day_number': work, 'event': event}

print('found', len(mapping), 'dates')
for k in sorted(mapping)[:10]:
    print(k, mapping[k])
