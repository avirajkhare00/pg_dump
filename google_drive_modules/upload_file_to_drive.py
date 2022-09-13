from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
import json


def upload_to_drive(source_path):

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_drive_modules/credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)

    """
    Upload a file to an Google Dive Folder.
    """
    folder_id = json.loads(open('config/config.json', 'r').read())['google_drive_modules']['folder_id']

    file_metadata = {
        'name': source_path,
        'parents': [folder_id]
    }

    media = MediaFileUpload(source_path,
                            mimetype='application/x-binary',
                            resumable=True)

    file = drive_service.files().create(body=file_metadata,
                            media_body=media,
                            fields='id').execute()

