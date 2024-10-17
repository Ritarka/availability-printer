import os.path
from datetime import datetime, time, date, timezone, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def event_info(event):
    start = event["start"].get("dateTime", event["start"].get("date"))
    end = event["end"].get("dateTime", event["end"].get("date"))
    summary = event['summary']
    
    start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z')
    end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S%z')
    
    zone = datetime.now(timezone.utc).astimezone().tzinfo
        
    # print(f"Event starts at {start.time()} (time zone: {start.tzinfo}), ends at {end.time()} (time zone: {end.tzinfo})")
        
    start = start.astimezone(zone)
    end = end.astimezone(zone)
    
    # print(f"Event starts at {start.time()} (time zone: {start.tzinfo}), ends at {end.time()} (time zone: {end.tzinfo})")
    
    assert start < end

    return start, end, summary


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days)+1
    for n in range(days):
        yield start_date + timedelta(n)

def get_availability(start_date, end_date, event_info):

    events_day = {}
    for event in event_info:
        # TODO: Make this resilient to events that cross midnight
        start, end, _ = event
        date = start.date()
        
        if date not in events_day:
            events_day[date] = []
        events_day[date].append(event)
        
    # print(events_day)
    # TODO: Loosen assumptions on 9-5 availability
    zone = datetime.now(timezone.utc).astimezone().tzinfo
    begin_day = datetime.combine(date, time(9, 0)).astimezone(zone)
    end_day = datetime.combine(date, time(17, 0)).astimezone(zone)

    available = {}
    for day in daterange(start_date, end_date):
        
        day_of_week = day.weekday()
        if day_of_week >= 5: # Skip Saturdays and Sundays
            continue
        
        date = day.date()
        available[date] = []
        
        if date not in events_day:
            available[date].append((begin_day, end_day))
            continue
        
        start = begin_day
        end = None
        for start_event, end_event, _ in events_day[date]:
            if start_event.time() == begin_day.time():
                start = end_event
                continue
            if start_event.time() < time(9, 0): 
                continue
            
            end = min(start_event, end_day)
            # if end.time() >= time(17, 0):
            #     pass
            available[date].append((start, end))
            start = end_event

        if start.time() < time(17, 0):
            available[date].append((start, end_day))
                        
    return available

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    
    start_date = datetime.now().astimezone()
    end_date = datetime.now().astimezone()+timedelta(days=21)

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_date.isoformat(),
            timeMax=end_date.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    # Prints the start and name of the next 10 events
    events_info_list = []
    for event in events:
        all_day = event["start"].get("date")
        if all_day is not None: continue

        start, end, summary = event_info(event)
        # print(start, " ---- ", end, " ---- ", summary)
        events_info_list.append((start, end, summary))
        
    availability = get_availability(start_date, end_date, events_info_list)
    print_availability(availability)

def print_availability(available):
    zone = datetime.now(timezone.utc).astimezone().tzinfo
    print(f"Here is when I will be available (all times in {zone})")
    for date, times in available.items():
        day_name = date.strftime('%A').ljust(10)
        print("   ", end="")
        print(f"{day_name} ({date.month:02}/{date.day:02}): ", end="")
        
        size = len(times)
        for i, busy_time in enumerate(times):
            start, end = busy_time
            start = start.strftime('%I:%M %p')
            end = end.strftime('%I:%M %p')
            
            if i == size - 1:
                print(f"{start} - {end}", end="")
            else:
                print(f"{start} - {end}, ", end="")
            
        print()

if __name__ == "__main__":
    main()