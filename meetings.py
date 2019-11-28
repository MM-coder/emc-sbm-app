import json

next_meeting = {"time": "13:40PM", "date": None, "location": None}

def get_next_meeting_text():
    time = next_meeting.get('time')
    date = next_meeting.get('date')
    location = next_meeting.get('location')
    if date == None and location == None:
        return "No details are avalible regarding the next meeting."
    if date == None:
        return f"The next meeting will be in {location} at {time} but there isn't a current meeting date set"
    if location == None:
        return f"The next meeting will be on the {date} at the {time} but there isn't a current location set"
    if time == None:
        return f"The next meeting will be on the {date} at {location} but there isn't a current time set"

def get_last_meeting_info():
    with open('json/lastmeeting.json', 'r+') as f:
        data = json.load(f)
    return data