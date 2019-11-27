import json


def get_user_password(username: str):
    with open('json/users.json', 'r+') as f:
        data = json.load(f)
        for i in data['users']:
            if i['username'] == username:
                return i['password']
        

def get_user_object(username: str):
    with open('json/users.json', 'r+') as f:
        data = json.load(f)
        for i in data['users']:
            if i['username'] == username:
                return i