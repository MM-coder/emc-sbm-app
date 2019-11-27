import json


def get_proposals():
    with open('json/proposals.json', 'r+') as fp:
        data = json.load(fp)
        return data['proposals']