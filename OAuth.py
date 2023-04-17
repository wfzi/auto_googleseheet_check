from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import OAuth_function

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1vfW_9OTYjo9OkY7f_nJWX-7CWrKfZUghNTA5bjney4I'
RANGE_NAME = 'B2:B4'

SPREADSHEET_DICT = {
    "test"              : "1vfW_9OTYjo9OkY7f_nJWX-7CWrKfZUghNTA5bjney4I",
    "tracking-form"     : "1zM-9tdsbCMwqEdGILtiHE6WPUMCkpEk5kdKcYBAICA4",
    "Tommi-Surya"       : "14MIJXZ0A5Aj8nuAWZrMe0s3qbGXa-HQiXdLrnnBezXM",
    "Shiyao-Wang"       : "1RNsQbjaIm8OVfYed2gUV--oUe2LCG4o9sZmKc4GpQYw",
    "Digvijay-Singh"    : "1rEG54WPhy-2OsyAUctWsW500JZEeA65RVLLpZPKFYKU"
}

MOCK_WEEKLY_REPORT_INFO = {
    "volunteer_info"    : ['Qilong Guo', 'qguo14@ucsc.edu ', (2022, 42, 1), '10-17-22', '10-15-22', '07-14-23'],
    "sheet_id"          : "1yXLOVg0fL0LRji8UQZpsHMbFah33sUymIw5GglwpAZc"
}

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
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
    print(type(creds))

    # Retrieve all volunteer information from the main tracking form
    volunteerInfo = OAuth_function.get_volunteer_info(SPREADSHEET_DICT['tracking-form'], creds)
    for info in volunteerInfo:
        print()
        print(info[0])
        print(OAuth_function.verify_weekly_report(info, info[6], creds))

    # print(OAuth_function.verify_weekly_report(MOCK_WEEKLY_REPORT_INFO['volunteer_info'], MOCK_WEEKLY_REPORT_INFO['sheet_id'], creds))


if __name__ == '__main__':
    main()