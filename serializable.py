from abc import ABC, abstractmethod
from datetime import datetime
from tinydb import Query
from typing import Self

class Serializable(ABC):
    db_connector =  None

    def __init__(self, id, creation_date: datetime = None, last_update: datetime = None) -> None:
        self.id = id
        self.creation_date = creation_date if creation_date else datetime.now()
        self.last_update = last_update if last_update else datetime.now()

    @classmethod
    @abstractmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        pass

    def store_data(self):
        print("Storing data...")
        self.last_update == datetime.now()

        query = Query()
        # upsert: https://tinydb.readthedocs.io/en/latest/usage.html#upserting-data
        result = self.db_connector.upsert(self.__to_dict(), query.id == self.id)
        if result:
            print("Data updated.")
        else:
            print("Data inserted.")

    
    def delete(self):
        print("Deleting data...")
        query = Query()
        if self.db_connector.remove(query.id == self.id):
            print("Data deleted.")
        else:
            print("Data not found.")
    
    @classmethod
    def find_by_attribute(cls, by_attribute: str, attribute_value: str, num_to_return=1) -> Self | list[Self]:
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery[by_attribute] == attribute_value)

        if result:
            if num_to_return == -1:
                num_to_return = len(result)

            data = result[:num_to_return]
            device_results = [cls.instantiate_from_dict(d) for d in data]
            return device_results if num_to_return > 1 else device_results[0]
        else:
            return None

           
    @classmethod
    def find_all(cls) -> list[Self]:
        # Load all data from the database and create instances of the Device class
        devices = []
        for device_data in cls.db_connector.all():
            devices.append(cls.instantiate_from_dict(device_data))
        return devices

    # String representation of the class
    def __repr__(self):
        return self.__str__()
    
    @abstractmethod
    def __str__(self):
        pass
    
    #Do not modify this function unless you really know what you are doing!
    def __to_dict(self, *args):
        """
        This function converts an object recursively into a dict.
        It is not necessary to understand how this function works!
        For the sake of simplicity it doesn't handle class attributes and callable objects like (callback) functions as attributes well
        """

        #If no object is passed to the function convert the object itself
        if len(args) > 0:
            obj = args[0] #ignore all other objects but the first one
        else:
            obj = self

        if isinstance(obj, dict):
            #If the object is a dict try converting all its values into dicts also
            data = {}
            for (k, v) in obj.items():
                data[k] = self.__to_dict(v)
            return data
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            #If the object is iterable (lists, etc.) try converting all its values into dicts
            #Strings are also iterable, but theses should not be converted
            data = [self.__to_dict(v) for v in obj]
            return data
        elif hasattr(obj, "__dict__"):
            #If its an object that has a __dict__ attribute this can be used
            data = []
            for k, v in obj.__dict__.items():
                #Iterate through all items of the __dict__ and and try converting each value to a dict
                #The resulting key value pairs are stored as tuples in a list that is then converted to a final dict
                data.append((k, self.__to_dict(v)))
            return dict(data)
        else:
            return obj