from __future__ import print_function

import io

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import os

SCOPES = ['https://www.googleapis.com/auth/drive']


def download_files_in_folder(folder_id, keywords=[]):
    """Downloads the files in the specified folder, as long as their names contain one of the keywords.
    Args:
        folder_id: ID of the folder to look for files.
        keywords: list of key strings. The name of the files downloaded needs to contain at least one of the keys.
                  If empty, all files are downloaded.
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("Couldn't load gdrive credentials. Please run drive_connect.py first.")

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        page_token = None
        while True:
            # Call the Drive v3 API
            results = service.files().list(
                    q=f"'{folder_id}' in parents",
                    pageSize=10, fields="nextPageToken, files(id, name)",
                    pageToken=page_token).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                for item in items:
                    foundKey = False
                    for key in keywords:
                        if key in item['name']:
                            foundKey = True
                            break
                        
                    if keywords != [] and not foundKey:
                        continue
                    
                    print(u'{0} ({1})'.format(item['name'], item['id']))


                    file_id = item['id']
                    request = service.files().get_media(fileId=file_id)                            
                    
                    file = io.BytesIO()
                    downloader = MediaIoBaseDownload(file, request)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print(F'Download {int(status.progress() * 100)}%.')
                    
                    with open(item['name'], "wb") as f:
                        f.write(file.getvalue()) 

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')



if __name__ == '__main__':
    keywords = []
    download_files_in_folder('1QKzZFTLCc_OJbOLIwKsnsO5zxGRyCc6v', keywords=keywords)