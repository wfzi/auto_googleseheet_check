from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_values(spreadsheet_id: 'str', range_name: 'str', creds: 'Credentials') -> 'list[list[str]]':
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.

    Parameters: spreadsheet_id: str
                The id of the spreadsheet.

                range_name: str
                colume and row name of the cells you want to retrieve. example: A1:C2

                creds: Credentials
                credentials of google api
    
    Returns:    list[list[str]]
                the value of the cells you retrived
        """
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range_name).execute()
        values = result.get('values', [])
        
        return values
    except HttpError as err:
        print(err)
    