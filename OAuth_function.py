from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import OAuth_function

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.metadata.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1zM-9tdsbCMwqEdGILtiHE6WPUMCkpEk5kdKcYBAICA4'
RANGE_NAME = 'OPT subscription tracking!A:G'

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    #Get information from OPT subscription tracking sheets
    values = OAuth_function.get_values(SPREADSHEET_ID, RANGE_NAME, creds)[1:]
    
    #loop into each person
    for row, person in enumerate(values):
        #get name and day
        month, day, year, name = person[0].split('-')

        #add sheet id if miss
        if len(person) <= 6 or person[6] == "No files found.":
            cur_id = OAuth_function.get_sheet_id(name, creds)
            OAuth_function.update_values(SPREADSHEET_ID,
                  "OPT subscription tracking!G" + str(row + 2), "USER_ENTERED",
                  [[cur_id]], creds)


if __name__ == '__main__':
    main()
