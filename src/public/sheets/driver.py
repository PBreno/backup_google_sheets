import io
from typing import Any

import google
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


def download_file(items):
    """Downloads a file
  Args:
      real_file_id: ID of the file to download
  Returns : IO object with location.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        for item in items:
            print(f"Downloading file with id {item['id']}")
            request = service.files().export_media(fileId=item['id'],
                                                   mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file = io.FileIO(f'{item['name'] }.xlsx', 'wb')
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.\n")

        return None

    except HttpError as error:
        return error
