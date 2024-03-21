import pandas as pd
from .MongoDBManager import MongoDBManager  # MongoDBManager 클래스를 임포트합니다.

class ExcelUploader:
    def __init__(self, file_name, document_name):
        self.file_name = file_name
        self.document_name = document_name

    def load_file(self):
        if self.file_name.endswith('.xlsx'):
            return pd.read_excel(self.file_name)
        elif self.file_name.endswith('.csv'):
            return pd.read_csv(self.file_name)
        else:
            raise ValueError("Unsupported file format")

    def compare(self, db_mgr, column_list):
        # Load the file
        df = self.load_file()

        # Get document structure from db
        success, db_structure = db_mgr.select_first_one(self.document_name)
        if not success:
            return False, f"DB error: {db_structure}"

        # Compare structures
        file_columns = set(df.columns)
        db_columns = set(db_structure[0].keys()) - {"_id"} if db_structure else set()

        if not file_columns.issubset(db_columns) or not db_columns.issubset(file_columns):
            diff = file_columns.symmetric_difference(db_columns)
            return False, f"Structure mismatch. Difference: {diff}"

        return True, "Structures match"

    def upload(self, db_mgr, column_list):
        # Load the file
        df = self.load_file()

        insert_count = 0
        update_count = 0
        errors = []

        for _, row in df.iterrows():
            document = row.to_dict()
            
            query = {col: document[col] for col in column_list if col in document}

            # Perform insert or update
            success, msg = db_mgr.update(self.document_name, query, document, upsert=True)
            if not success:
                errors.append(msg)
            else:
                if msg == "Inserted new document":
                    insert_count += 1
                else:
                    update_count += msg  # msg is the modified count in this case

        if errors:
            return False, errors
        else:
            return True, f"Insertions: {insert_count}, Updates: {update_count}"