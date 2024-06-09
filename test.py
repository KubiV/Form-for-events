import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Připojení k Google Sheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Otevření listu
sheet = client.open('Název_listu').sheet1  # Změň 'Název_listu' na skutečný název tvého listu

# Získání všech hodnot v listu
all_values = sheet.get_all_values()

# Najdi poslední plný řádek
last_row_index = None
for i in range(len(all_values) - 1, -1, -1):
    if all(all_values[i]):
        last_row_index = i + 1
        break

# Údaj, který chceš přidat
data_to_add = "Nový údaj"

# Přidání údaje do nového sloupce na konec posledního plného řádku
sheet.update_cell(last_row_index, sheet.col_count + 1, data_to_add)
