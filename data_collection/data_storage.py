#data_storage.py

import os
import pandas as pd

class DataStorage:
    def __init__(self, storage_dir="data"):
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def save_data_to_csv(self, data, filename):
        """Save data to a CSV file."""
        file_path = os.path.join(self.storage_dir, filename)
        
        # Convert data to DataFrame and save as CSV
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data])  # Convert single dictionary to DataFrame

        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
        return file_path

    def load_data_from_csv(self, filename):
        """Load data from a CSV file."""
        file_path = os.path.join(self.storage_dir, filename)
        
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            return df.to_dict(orient="records")
        else:
            raise FileNotFoundError(f"{filename} does not exist")

