import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import Field
from ..base_tool import BaseTool
from src.utils import SCOPES

class CalendarTool(BaseTool):
    """
    A tool for booking events on Google Calendar
    """
    event_name: str = Field(description='Name of the event to be created')
    event_datetime: str = Field(
        description='Date and time of the event. This must be converted into a Python datetime.datetime object before use.'
    )
    event_description: str = Field(default="", description='Optional description of the event')

    def get_credentials(self):
        """
        Get and refresh Google Calendar API credentials
        """
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def create_event(self):
        """
        Creates an event on Google Calendar
        """
        try:
            creds = self.get_credentials()
            service = build("calendar", "v3", credentials=creds)
            
            # Convert the string to a datetime object
            event_datetime = datetime.datetime.fromisoformat(self.event_datetime)

            event = {
                'summary': self.event_name,
                'description': self.event_description,
                'start': {
                    'dateTime': event_datetime.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': (event_datetime + datetime.timedelta(hours=1)).isoformat(),
                    'timeZone': 'UTC',
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            return f"Event created successfully. Event ID: {event.get('id')}"

        except HttpError as error:
            return f"An error occurred: {error}"

    def run(self):
        return self.create_event()