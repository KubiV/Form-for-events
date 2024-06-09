import gspread
from google.oauth2.service_account import Credentials
from setup import id, registration_list

credentials_file = 'credentials.json'
sheet_id = id
registation_sheet = registration_list

# Připojení k Google Sheets
SCOPES = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file(credentials_file, scopes=SCOPES)
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/"+ sheet_id +"/edit")
sheet = spreadsheet.worksheet(registation_sheet)

# Získání všech hodnot v listu
all_values = sheet.get_all_values()

def add_value_to_last_row(value):
    last_filled_row = len(all_values)
    next_column = len(all_values[0]) + 1 
    sheet.update_cell(last_filled_row, next_column, value)

# Příklad použití
value_to_add = 'nová hodnota'
add_value_to_last_row(value_to_add)
