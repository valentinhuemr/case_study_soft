from tinydb import TinyDB, Query

# Datenbank initialisieren
db = TinyDB("database.json")
user_table = db.table("users")

class User:
    def __init__(self, id, name) -> None:
        """Create a new user based on the given name and id"""
        self.name = name
        self.id = id

    def store_data(self) -> None:
        """Save the user to the database"""
        user_table.upsert({"id": self.id, "name": self.name}, Query().id == self.id)

    def delete(self) -> None:
        """Delete the user from the database"""
        user_table.remove(Query().id == self.id)

    def __str__(self):
        return f"User {self.id} - {self.name}"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def find_all() -> list:
        """Find all users in the database"""
        return [User(user["id"], user["name"]) for user in user_table.all()]

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str) -> 'User':
        """Find a user by a specific attribute"""
        user_data = user_table.get(Query()[by_attribute] == attribute_value)
        if user_data:
            return cls(user_data["id"], user_data["name"])
        return None