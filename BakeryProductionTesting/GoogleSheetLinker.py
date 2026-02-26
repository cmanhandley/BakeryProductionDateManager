import pandas as pd
import gspread

class GoogleSheetLinker:
    def __init__(self, worksheet_name="Sheet1"):
        self.worksheet_name = worksheet_name
        try:
            self.gc = gspread.service_account(filename="credentials.json")
            self.sheet = self.gc.open("BakeryProduction")
            self.ws = self.sheet.worksheet(self.worksheet_name)
            print("Google Sheets link established successfully.")
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Error: The spreadsheet 'BakeryProduction' was not found.")
        except gspread.exceptions.WorksheetNotFound:
            print(f"Error: The worksheet '{worksheet_name}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def pull(self):
        try:
            records = self.ws.get_all_records()
            return pd.DataFrame(records)
        except Exception as e:
            print(f"Error pulling data: {e}")
            return None

    def push_fifo(self, inventory_objects):
        try:
            values = [["Product", "ShelfLife", "QueueJSON", "PullToday"]]
            for inv in inventory_objects:
                values.append([
                    inv.name,
                    inv.shelf_life,
                    inv.to_json(),
                    inv.pulled_today
                ])
            self.ws.update("A1", values)
            print("FIFO sheet updated successfully.")
        except Exception as e:
            print(f"Error pushing FIFO data: {e}")
