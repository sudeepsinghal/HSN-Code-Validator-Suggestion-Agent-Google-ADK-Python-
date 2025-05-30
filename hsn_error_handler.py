import logging
import pandas as pd

logging.basicConfig(
    filename='hsn_agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class HSNErrorHandler:
    @staticmethod
    def validate_hsn_input(code):
        if not code:
            raise ValueError("Input cannot be empty.")
        if not isinstance(code, str):
            raise TypeError("HSN code must be a string.")
        if not code.isdigit():
            raise ValueError("HSN code must be numeric.")
        if len(code) not in [2, 4, 6, 8]:
            raise ValueError("HSN code must be 2, 4, 6, or 8 digits long.")

    @staticmethod
    def handle_data_access(df, code):
        try:
            result = df[df['HSNCode'] == code]
            if result.empty:
                return None
            description = result.iloc[0]['Description']
            if pd.isna(description) or not description.strip():
                return "Description missing"
            return description
        except Exception as e:
            logging.error(f"Data access error for code {code}: {str(e)}")
            return "Data access error"

    @staticmethod
    def validate_description_input(description):
        if not description or not isinstance(description, str):
            raise ValueError("Description must be a non-empty string.")
        if len(description.strip()) < 3:
            raise ValueError("Description too short for meaningful suggestions.")

    @staticmethod
    def handle_suggestion_response(results, threshold=0.3):
        if results is None or len(results) == 0:
            return "No suggestions found."
        if isinstance(results, str): # In case an error message was returned
            return results
        # Filter results based on threshold if needed, or just return as is
        # For now, it returns the DataFrame directly if it's not a string error
        return results

    @staticmethod
    def log_warning(message):
        logging.warning(message)

    @staticmethod
    def log_info(message):
        logging.info(message)

    @staticmethod
    def safe_load_excel(file_path):
        try:
            df = pd.read_excel(file_path)
            return df
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logging.error(f"Failed to load Excel file: {e}")
            raise