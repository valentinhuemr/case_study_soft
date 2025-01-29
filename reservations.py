from tinydb import TinyDB, Query
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
