import os, re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from pydantic import Field
from ..base_tool import BaseTool
from src.utils import SCOPES

class FetchContactTool(BaseTool):
    """
    A tool for fetching contact information from Google Contacts
    """
    contact_name: str = Field(description='Name (first or last) of the contact to search for')

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

    def fetch_contact(self):
        """
        Fetches contact information from Google Contacts
        """
        try:
            creds = self.get_credentials()
            service = build('people', 'v1', credentials=creds)

            # Search for the contact
            results = service.people().searchContacts(
                query=self.contact_name,
                readMask='names,phoneNumbers,emailAddresses'
            ).execute()

            connections = results.get('results', [])

            if not connections:
                return f"No contact found with the name: {self.contact_name}"

            matching_contacts = []

            for connection in connections:
                contact = connection['person']
                names = contact.get('names', [])
                if names:
                    unstructured_name = names[0].get('unstructuredName', '').lower()
                    # Prepare regex to identify first and last names
                    first_name_pattern = r'^(\w+)'  # Match first word
                    last_name_pattern = r'(\w+)$'   # Match last word
                    first_match = re.search(first_name_pattern, unstructured_name)
                    last_match = re.search(last_name_pattern, unstructured_name)
                    
                    if (first_match and self.contact_name.lower() == first_match.group(1)) or \
                       (last_match and self.contact_name.lower() == last_match.group(1)):
                        full_name = names[0].get('displayName', 'N/A')
                        phone_numbers = [phone.get('value', 'N/A') for phone in contact.get('phoneNumbers', [])]
                        emails = [email.get('value', 'N/A') for email in contact.get('emailAddresses', [])]

                        matching_contacts.append({
                            'name': full_name,
                            'phone_numbers': phone_numbers,
                            'emails': emails
                        })

            if not matching_contacts:
                return f"No contact found with the matching criteria: {self.contact_name}"

            return str(matching_contacts)

        except HttpError as error:
            return f"An error occurred: {error}"

    def run(self):
        return self.fetch_contact()
