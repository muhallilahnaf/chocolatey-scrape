import json

codedict = dict()

with open('chocolatey.json', 'r') as f1:
    items = json.load(f1)

    for item in items:
        code = item['code']
        dotpos = code.find('.')
        if (dotpos == -1):
            if code not in codedict:
                codedict[code] = [{
                    'name': item['name'],
                    'link': item['link'],
                    'downloads': item['downloads']
                }]
        else:
            fpart = code[:dotpos]
            lpart = code[dotpos+1:]
            if fpart in codedict:
                codedict[fpart].append({
                    'name': item['name'],
                    'link': item['link'],
                    'extension': lpart,
                    'downloads': item['downloads']
                })
            else:
                codedict[fpart] = [{
                    'name': item['name'],
                    'link': item['link'],
                    'extension': lpart,
                    'downloads': item['downloads']
                }]

    # if everything okay
    with open('chocodict.json', 'w') as f2:
        json.dump(codedict, f2)

    appcodes = list(codedict.keys())
    with open('appcodes.json', 'w') as f3:
        json.dump(appcodes, f3)
