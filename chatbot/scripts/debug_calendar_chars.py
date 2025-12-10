fn = 'chatbot/data/calendar_extracted.txt'
with open(fn, 'rb') as f:
    raw = f.read().decode('utf-8', 'ignore')

print('len', len(raw))
start = raw.find('{')
print('first brace index', start)
print('first 80 chars snippet:')
print(repr(raw[start:start+200]))

idx = raw.find('date')
print('\nindex of substring "date"', idx)
if idx!=-1:
    print('context around date:')
    for i in range(max(0, idx-6), idx+6):
        ch = raw[i]
        print(i, repr(ch), hex(ord(ch)))

 # show first 40 chars char codes
print('\nfirst 40 char codes:')
for i,ch in enumerate(raw[:40]):
    print(i, repr(ch), hex(ord(ch)))
