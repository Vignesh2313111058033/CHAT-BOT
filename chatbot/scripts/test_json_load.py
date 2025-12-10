import json
fn = 'chatbot/data/calendar_extracted.txt'
with open(fn, 'r', encoding='utf-8') as f:
    s = f.read()

try:
    data = json.loads(s)
    print('loaded keys:', list(data.keys())[:5])
except Exception as e:
    print('json error:', repr(e))
    # print a prefix to help debug
    print('prefix:', s[:400])
