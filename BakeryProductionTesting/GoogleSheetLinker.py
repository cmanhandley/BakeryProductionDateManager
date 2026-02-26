import pandas as pd
import gspread
"""
this is the linker between google sheets and simulated bakery production.
Interacts with credentials.json to access google sheets
"""
class GoogleSheetLinker:
    def __init__(self, worksheet_name="Sheet1"):
        self.worksheet_name = worksheet_name
        try:
            self.gc = gspread.service_account(filename="credentials.json")
            self.sheet = self.gc.open("BakeryProduction")
            self.ws = self.sheet.worksheet(self.worksheet_name)
            #updates gooogle sheet with product, quantity, and sell by date
            #worksheet.update("A1:A2", [["Product"], [2]])
            print("Google Sheets link established successfully.")

        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Error: The spreadsheet 'BakeryProduction' was not found.")
        except gspread.exceptions.WorksheetNotFound:
            print(f"Error: The worksheet '{worksheet_name}' was not found in the spreadsheet.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def pull(self):
        try:
            records = self.ws.get_all_records()
            df = pd.DataFrame(records)
            return df
        
        except Exception as e:
            print(f"Error pulling data: {e}")
            return None
        
    def push(self, products):
        try:
            values = [["Product", "Quantity", "Sell by date"]]
            for product in products:
                values.append([product.getProduct(), product.getQuantity(), product.getSellByDate()])
            self.ws.update("A1", values)
            print("Sheet updated successfully.")

        except Exception as e:
            print(f"Error pushing data: {e}")

        