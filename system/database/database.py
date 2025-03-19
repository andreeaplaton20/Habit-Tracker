import json

class DataBase:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.database = self.initialize_database()

    def initialize_database(self):
        """Initializes the database from the provided file path"""
        with open(self.file_path, "r") as file:
            database = json.load(file)
        return database

    def save_database_state(self, file_path=None):
        """Saves the current database state in the mentioned file_path
        
        Args:
            file_path: If given a file path it will save the database there, otherwise in the class file_path.
        """
        if file_path is None:
            file_path = self.file_path
        with open(file_path, "w") as file:
            json.dump(self.database, file, indent=4)