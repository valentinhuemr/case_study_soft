from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB("database.json")
reservation_table = db.table("reservations")

class Reservation:
    def __init__(self, user_id: str, device_id: str, start_date: str, end_date: str):
        self.user_id = user_id
        self.device_id = device_id
        self.start_date = start_date
        self.end_date = end_date

    def store_data(self):
        reservation_table.insert({
            "user_id": self.user_id,
            "device_id": self.device_id,
            "start_date": self.start_date,
            "end_date": self.end_date
        })

    @classmethod
    def find_all(cls):
        return [cls(**res) for res in reservation_table.all()]