from tinydb import TinyDB, Query
import os
from serializer import serializer
from datetime import datetime



class Device:
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    def __init__(self, device_name: str, managed_by_user_id: str, **kwargs):
        self.id = kwargs.get('id')  # ID wird entweder aus der Datenbank oder beim Instanziieren gesetzt
        if not self.id:  # Falls keine ID vorhanden, automatisch generieren
            self.id = len(self.db_connector) + 1
        self.device_name = device_name
        self.managed_by_user_id = managed_by_user_id
        self.is_active = kwargs.get('is_active', True)
        self.end_of_life = kwargs.get('end_of_life', None)
        self.first_maintenance = kwargs.get('first_maintenance', None)
        self.next_maintenance = kwargs.get('next_maintenance', None)
        self.__maintenance_interval = kwargs.get('maintenance_interval', None)
        self.__maintenance_cost = kwargs.get('maintenance_cost', 0.0)
        self.__last_update = kwargs.get('last_update', datetime.now().isoformat())
        self.__creation_date = kwargs.get('creation_date', datetime.now().isoformat())

    def store_data(self):
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        data = {
            "id": self.id,
            "device_name": self.device_name,
            "managed_by_user_id": self.managed_by_user_id,
            "is_active": self.is_active,
            "end_of_life": self.end_of_life,
            "first_maintenance": self.first_maintenance,
            "next_maintenance": self.next_maintenance,
            "maintenance_interval": self.__maintenance_interval,
            "maintenance_cost": self.__maintenance_cost,
            "last_update": datetime.now().isoformat(),
            "creation_date": self.__creation_date
        }
        if result:
            self.db_connector.update(data, DeviceQuery.device_name == self.device_name)
        else:
            self.db_connector.insert(data)

    @classmethod
    def find_all(cls):
        devices = []
        for device in cls.db_connector.all():
            devices.append(cls(**device))
        return devices
    def delete(self):
            """Löscht das aktuelle Gerät aus der Datenbank."""
            DeviceQuery = Query()
            self.db_connector.remove(DeviceQuery.device_name == self.device_name)