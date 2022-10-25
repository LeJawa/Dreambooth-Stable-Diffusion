from __future__ import print_function

import io

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import os

SCOPES = ['https://www.googleapis.com/auth/drive']


def download_file(FOLDER_ID):
    """Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
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
                    q=f"'{FOLDER_ID}' in parents",
                    pageSize=10, fields="nextPageToken, files(id, name)",
                    pageToken=page_token).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                for item in items:
                    print(u'{0} ({1})'.format(item['name'], item['id']))


                    file_id = item['id']
                    request = service.files().get_media(fileId=file_id)

                    with open(item['name'], 'wb') as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()
                            print("Download %d%%." % int(status.progress() * 100))

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')



if __name__ == '__main__':
    print(download_file('1QKzZFTLCc_OJbOLIwKsnsO5zxGRyCc6v'))