import pandas as pd
import gspread
"""
this is the linker between google sheets and simulated bakery production.
Interacts with credentials.json to access google sheets
"""

try:
    gc = gspread.service_account(filename="credentials.json")
    sheet = gc.open("BakeryProduction")
    worksheet_name = "Sheet1"
    worksheet = sheet.worksheet(worksheet_name)
    #updates gooogle sheet with product, quantity, and sell by date
    worksheet.update("A1:A2", [["Product"], [2]])
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)
    print("Data loaded successfully!")
    print(df.head())

except gspread.exceptions.SpreadsheetNotFound:
    print(f"Error: The spreadsheet 'BakeryProduction' was not found.")
except gspread.exceptions.WorksheetNotFound:
    print(f"Error: The worksheet '{worksheet_name}' was not found in the spreadsheet.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")