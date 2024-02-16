import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

API_FILE_PATH = 'api_access/secret_key.json'

class Sheets:
    def __init__(self) -> None:
        
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(API_FILE_PATH, scopes=scopes)
        file = gspread.authorize(credentials)
        self.workbook = file.open('Financeiro')
        self.opened_sheets = {}

    def get_sheet_by_name(self, name: str) -> pd.DataFrame:
        if name not in self.opened_sheets.keys():
            print(f"Getting data for {name}...", end=" ")
            sheet = self.workbook.worksheet(name)
            df = pd.DataFrame(sheet.get_all_records())
            self.opened_sheets[name] = df

        print(f"Got data for {name}.")
        return self.opened_sheets[name]
    