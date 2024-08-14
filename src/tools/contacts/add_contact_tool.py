import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from pydantic import Field
from ..base_tool import BaseTool
from src.utils import SCOPES

class AddContactTool(BaseTool):
    """
    A tool for adding a new contact to Google Contacts
    """
    name: str = Field(description='Full name of the contact')
    phone: str = Field(description='Phone number of the contact')
    email: str = Field(default=None, description='Email address of the contact (optional)')

    def get_credentials(self):
        """
        Get and refresh Google Contacts API credentials
        """
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def add_contact(self):
        """
        Adds a new contact to Google Contacts
        """
        try:
            creds = self.get_credentials()
            service = build('people', 'v1', credentials=creds)

            contact_body = {
                "names": [{"givenName": self.name}],
                "phoneNumbers": [{"value": self.phone}]
            }

            if self.email:
                contact_body["emailAddresses"] = [{"value": self.email}]

            contact = service.people().createContact(body=contact_body).execute()

            return f"Contact added successfully. Contact ID: {contact.get('resourceName')}"

        except HttpError as error:
            return f"An error occurred: {error}"

    def run(self):
        return self.add_contact()