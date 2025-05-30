from hsn_error_handler import HSNErrorHandler

class HSNCodeValidator:
    def __init__(self, df):
        self.df = df
        self.valid_codes = set(df['HSNCode'])

    def validate_code(self, code):
        try:
            HSNErrorHandler.validate_hsn_input(code)
        except Exception as e:
            return False, str(e)

        if code not in self.valid_codes:
            return False, "HSN code not found in master dataset."

        description = HSNErrorHandler.handle_data_access(self.df, code)
        if description == "Description missing":
            return True, "HSN code is valid but description is missing."
        elif description == "Data access error":
            return False, "Error occurred during data lookup."
        return True, description

    def validate_hierarchy(self, code):
        try:
            HSNErrorHandler.validate_hsn_input(code)
        except Exception:
            return []

        hierarchy = [code[:i] for i in (2, 4, 6) if len(code) > i]
        return [c for c in hierarchy if c in self.valid_codes]