import io
from datetime import datetime
import google
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


def download_file(items):

    creds, _ = google.auth.default()

    try:
        #path to the folder
        BACKUP_FOLDER_PATH = 'M:\\Usuários\\Breno Francisco Rafael Pombo\\backup'

        #create drive api client
        service = build("drive", "v3", credentials=creds)

        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        #downloading the files
        for item in items:
            print(f"Downloading file with id {item['id']}")
            request = service.files().export_media(fileId=item['id'],
                                                   mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file = io.FileIO(f'{BACKUP_FOLDER_PATH}\\{item['name']}-{date_time}.xlsx', 'wb', closefd=True)
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.\n")

        return None

    except HttpError as error:
        return error

