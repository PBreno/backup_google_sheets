import io
import os
from datetime import datetime
import google
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


#path to the folder
BACKUP_FOLDER_PATH = 'M:\\Usuários\\Estevan Silva\\backup planilhas'

def download_files(items):

    creds, _ = google.auth.default()

    try:

        #create drive api client
        service = build("drive", "v3", credentials=creds)

        # Create a folder if not exists in the specified path.
        if not os.path.exists(BACKUP_FOLDER_PATH):
            print(f"Creating folder {BACKUP_FOLDER_PATH}")
            os.mkdir(BACKUP_FOLDER_PATH)

        date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        #downloading the files
        for item in items:
            print(f"Downloading da planilha {item('name')}")
            request = service.files().export_media(fileId=item[('id'),
                                                   mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            file = io.FileIO(f'{BACKUP_FOLDER_PATH}\\{item('name')}-{date_time}.xlsx', 'wb', closefd=True)
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.\n")

        return None

    except HttpError as error:
        return error



def remove_duplicate_files(items):

    if not os.path.exists(BACKUP_FOLDER_PATH):
        return

    backup_folder_items = os.listdir(BACKUP_FOLDER_PATH)

    for item in items:
        name = item['name'].split('-').pop().strip()
        for file in backup_folder_items:
            file_filtered = file.split('-')[0].strip()
            if name == file_filtered:
                print(f"Removing the file {file} from folderg")
                os.remove(f'{BACKUP_FOLDER_PATH}\\{file}')
