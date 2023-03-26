from google.oauth2 import service_account
from googleapiclient.discovery import build
from dateutil import rrule, weekday
from datetime import datetime, timedelta

# Enter the path to your service account JSON file here
SERVICE_ACCOUNT_FILE = '/path/to/your/service/account.json'

# Enter your calendar ID here
CALENDAR_ID = 'your_calendar_id@group.calendar.google.com'

# Enter the name of the event you want to create
EVENT_NAME = 'Full Weekend'

# Set up the Google Calendar API client
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/calendar'],
)
service = build('calendar', 'v3', credentials=creds)

# Find the first full weekend of each month and create an event
for dtstart in rrule.rrule(
    rrule.MONTHLY,
    dtstart=datetime.today(),
    count=12,
):
    # Find the first Saturday of the month
    first_saturday = dtstart + timedelta(
        days=(5 - dtstart.weekday()) % 7
    )

    # Find the first Sunday after the first Saturday
    first_sunday = first_saturday + timedelta(days=1)

    # Check if the Sunday is in the same month as the Saturday
    if first_saturday.month == first_sunday.month:
        # Create the event start and end times
        event_start = first_saturday.strftime('%Y-%m-%dT09:00:00')
        event_end = first_sunday.strftime('%Y-%m-%dT18:00:00')

        # Create the event object
        event = {
            'summary': EVENT_NAME,
            'start': {
                'dateTime': event_start,
                'timeZone': 'Your Time Zone',
            },
            'end': {
                'dateTime': event_end,
                'timeZone': 'Your Time Zone',
            },
            'reminders': {
                'useDefault': True,
            },
        }

        # Create the event on your calendar
        service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

