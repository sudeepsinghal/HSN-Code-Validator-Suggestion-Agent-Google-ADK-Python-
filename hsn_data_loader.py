import pandas as pd
from hsn_error_handler import HSNErrorHandler

class HSNDataLoader:
    def __init__(self, file_path):
        self.df = HSNErrorHandler.safe_load_excel(file_path)
        self.df.columns = self.df.columns.str.strip()

        # This check confirms if the required columns exist AFTER stripping whitespace
        if 'HSNCode' not in self.df.columns or 'Description' not in self.df.columns:
            raise ValueError("Required columns 'HSNCode' and 'Description' are missing or misnamed in the Excel file. Please ensure exact spelling and casing.")

        self.df['HSNCode'] = self.df['HSNCode'].astype(str)
        self.df['Description'] = self.df['Description'].astype(str).str.lower()

    def get_dataframe(self):
        return self.df