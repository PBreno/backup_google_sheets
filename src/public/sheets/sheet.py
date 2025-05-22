import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .driver import download_file, remove_duplicate_files

#Getting the path to the credentials file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'credentials.json')

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def get_sheet()-> list[str] | HttpError:

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                JSON_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name, mimeType, size)")
            .execute()
        )

        items = results.get('files', [])

        if not items:
            raise Exception('No files found.')

        #Getting only spreadsheet from drive
        sheets = []
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                sheets.append(item)

        return remove_duplicate_files(sheets)

    except HttpError as error:
        return error

