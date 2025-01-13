import os
from datetime import datetime
from tinydb import TinyDB, Query
from serializer import serializer
from users import User  # Nutzerklasse importieren


class Device():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    def __init__(self, device_name: str, managed_by_user_id: str, **kwargs):
        self.id = kwargs.get('id', None)  # ID für das Gerät
        self.device_name = device_name
        self.managed_by_user_id = managed_by_user_id  # Nutzer-ID (z. B. E-Mail)
        self.is_active = kwargs.get('is_active', True)
        self.end_of_life = kwargs.get('end_of_life', None)
        self.first_maintenance = kwargs.get('first_maintenance', None)
        self.next_maintenance = kwargs.get('next_maintenance', None)
        self.__maintenance_interval = kwargs.get('maintenance_interval', None)
        self.__maintenance_cost = kwargs.get('maintenance_cost', 0.0)
        self.__last_update = kwargs.get('last_update', datetime.now().isoformat())
        self.__creation_date = kwargs.get('creation_date', datetime.now().isoformat())

    def __str__(self):
        return f"Device {self.device_name} (managed by: {self.managed_by_user_id})"

    def __repr__(self):
        return self.__str__()

    def store_data(self):
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)
        data = {
            "id": self.id or len(self.db_connector.all()) + 1,  # Automatische ID, falls keine vorhanden
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

    def delete(self):
        DeviceQuery = Query()
        self.db_connector.remove(DeviceQuery.device_name == self.device_name)

    def update_maintenance(self, interval: int, cost: float):
        self.__maintenance_interval = interval
        self.__maintenance_cost = cost
        self.store_data()

    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1):
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery[by_attribute] == attribute_value)
        if result:
            devices = [cls(**device) for device in result[:num_to_return]]
            return devices if num_to_return > 1 else devices[0]
        return None

    @classmethod
    def find_all(cls):
        devices = []
        for device in cls.db_connector.all():
            devices.append(cls(**device))
        return devices

    def link_to_user(self, user_id: str):
        user = User.find_by_attribute("id", user_id)
        if user:
            self.managed_by_user_id = user_id
            self.store_data()
        else:
            raise ValueError(f"User with ID '{user_id}' not found.")
