from tinydb import TinyDB, Query
<<<<<<< HEAD
import os
from datetime import datetime

class Reservation:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('reservations')

    def __init__(self, device_id: int, user_id: str, date: str, **kwargs):
        self.id = kwargs.get('id', len(self.db_connector) + 1)
        self.device_id = device_id
        self.user_id = user_id
        self.date = date

    def store_data(self):
        ReservationQuery = Query()
        existing = self.db_connector.search((ReservationQuery.device_id == self.device_id) & (ReservationQuery.date == self.date))
        
        if existing:
            return False  # Reservierung existiert bereits
        
        data = {
            "id": self.id,
            "device_id": self.device_id,
            "user_id": self.user_id,
            "date": self.date,
        }
        self.db_connector.insert(data)
        return True

    @classmethod
    def find_all(cls):
        return [cls(**reservation) for reservation in cls.db_connector.all()]

    @classmethod
    def find_by_device(cls, device_id):
        ReservationQuery = Query()
        return [cls(**res) for res in cls.db_connector.search(ReservationQuery.device_id == device_id)]

    def delete(self):
        ReservationQuery = Query()
        self.db_connector.remove((ReservationQuery.device_id == self.device_id) & (ReservationQuery.date == self.date))
=======
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
>>>>>>> 739d89ce6c5ec20e053d9aaf5a36c5a67dbbeb50
