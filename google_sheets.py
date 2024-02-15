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

    def get_sheet_by_name(self, name: str) -> pd.DataFrame:
        sheet_credit = self.workbook.worksheet(name)
        df = pd.DataFrame(sheet_credit.get_all_records())
        return df