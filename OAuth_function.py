from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_values(spreadsheet_id: 'str', range_name: 'str', creds: 'Credentials') -> 'list[list[str]]':
    """
    Get the value from a google sheets by specific sheets id, range and credentials

    Parameters: spreadsheet_id: str
                The id of the spreadsheet.

                range_name: str
                Sheets name, colume and row name of the cells you want to retrieve. example: A1:C2

                creds: Credentials
                Credentials of google api
    
    Returns:    list[list[str]]
                The value of the cells you retrived
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


def get_sheet_id(name: 'str', creds: 'Credentials') -> 'str':
    """
    get the weekly report sheets id by name and credentials

    Parameters: name: str
                Name of the people whose weekly report sheets id we want to get.

                creds: Credentials
                Credentials of google api
    
    Returns:    str
                The weekly report sheets id
        """
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            q="'1w-41nhWBFJFjWGXTT4WOTfSbbN-GVbyx' in parents", fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        
        for item in items:
            cur_name = item['name'].split('-')[0]
            if cur_name == name:
                return item['id']
            
        return 'No files found.'
    except HttpError as err:
        print(err)

def update_values(spreadsheet_id: 'str', range_name: 'str', value_input_option: 'str', values: 'list[list[str]]', creds: 'Credentials'):
    """
    Write the content into google sheets

    Parameters: spreadsheet_id: str
                The id of the spreadsheet.

                range_name: str
                Sheets name, colume and row name of the cells you want to retrieve. example: A1:C2

                value_input_option: str
                How we want to input our value

                values: The values we want to write in

                creds: Credentials
                Credentials of google api
    
    Returns:    list[list[str]]
                The value of the cells you retrived
        """
    # pylint: disable=maybe-no-member
    try:

        service = build('sheets', 'v4', credentials=creds)
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
