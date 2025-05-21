import http
import io
import os

from google.auth.transport.requests import Request

from fastapi import APIRouter, HTTPException, Response
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from .driver import download_file
from .message import http_message
router = APIRouter(
    prefix="/sheets",
    tags=["sheets"]
)


@router.get('/')
async def get_sheet()-> list() :

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'credentials.json')

    SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    #print(json_path)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                json_path, SCOPES
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
        sheets = []
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                sheets.append(item)

        if not items:
            return {
                "message": "No files found."
            }
        #print('Files:')

        # mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        # request = service.files().export_media(fileId=id_sheets[0], mimeType=mime_type)
        # file = io.BytesIO()
        # downloader = MediaIoBaseDownload(file, request)
        # done = False
        # while done is False:
        #     status, done = downloader.next_chunk()
        #     print(f"Download {int(status.progress() * 100)}.")

        return {
             "message": "Sucess",
            "codestatus": http.HTTPStatus.OK,
             "data": download_file(sheets)
         }


    except HttpError as error:
        return {
            "message": "An error occurred: {}".format(error),
            "statuscode": http.HTTPStatus.BAD_REQUEST
        }

