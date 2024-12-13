import json
import os

class Database:
    def __init__(self, database_file="users_db.json"):
        self.database_file = database_file
        self.data = self._load_database()

    def _load_database(self):
        if not os.path.exists(self.database_file):
            return {}
        with open(self.database_file, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        return data

    def _save_database(self):
        with open(self.database_file, "w") as f:
            json.dump(self.data, f, indent=4)

    def authenticate(self, username, password):
        if username in self.data and self.data[username]["password"] == password:
            return True
        return False

    def create_account(self, username, password, personal_info):
        self.data[username] = {
            "password": password,
            "personal_info": personal_info,
            "messages": []
        }
        self._save_database()

    def get_user_data(self, username):
        return self.data.get(username, {})

    def update_user_messages(self, username, messages):
        if username in self.data:
            self.data[username]["messages"] = messages
            self._save_database()

    def user_exists(self, username):
        return username in self.data
