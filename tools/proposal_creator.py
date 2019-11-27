import json

do = True
    
while do:
    with open('proposals.json', 'r+') as fp:
        data = json.load(fp)
    name = str(input('Proposal Name? '))
    if name.upper() == 'END':
        break
    description = str(input('Descriptor? '))
    link = str(input('PDF link? '))
    old = bool(int(input('Old? (0/1) ')))
    dicto = {"title": name, "description": description, "document": link, "old": old}
    data['proposals'].append(dicto)
    with open('proposals.json', 'w+') as write:
        json.dump(data, write)