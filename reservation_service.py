from reservations import Reservation
from devices_inheritance import Device
from users_inheritance import User


class ReservationService():

    def __init__(self) -> None:
        self.find_all_reservations()

    def find_all_reservations(cls) -> list[Reservation]:
        cls.reservations = Reservation.find_all()
        return cls.reservations

    def find_all_reservations_by_user_id(cls, user_id: str) -> list[Reservation]:
        return [reservation for reservation in cls.reservations if reservation.user_id == user_id]
    
    def find_all_reservations_by_device_id(cls, device_id: str) -> list[Reservation]:
        return [reservation for reservation in cls.reservations if reservation.device_id == device_id]    
    
    def find_all_reservations_by_user_id_and_device_id(cls, user_id: str, device_id: str) -> list[Reservation]:
        return [reservation for reservation in cls.reservations if reservation.device_id == device_id and reservation.user_id == user_id]

    def check_conflict(cls, device_id: str, start_date: str, end_date: str) -> bool:
        for reservation in cls.reservations:
            if reservation.device_id == device_id:
                if (start_date >= reservation.start_date and start_date <= reservation.end_date) or (end_date >= reservation.start_date and end_date <= reservation.end_date):
                    return True
        return False

    def user_exists(cls, user_id: str) -> bool:
        return User.find_by_attribute("id", user_id) is not None

    def device_exists(cls, device_id: str) -> bool:
        return Device.find_by_attribute("id", device_id) is not None
    
    def create_reservation(cls, user_id: str, device_id: str, start_date: str, end_date: str) -> bool:
        if not cls.user_exists(user_id):
            raise ValueError("User does not exist")
        
        if not cls.device_exists(device_id):
            raise ValueError("Device does not exist")
        
        if cls.check_conflict(device_id, start_date, end_date):
            raise ValueError("Reservation conflict detected")
        
        reservation = Reservation(user_id, device_id, start_date, end_date)
        reservation.store_data()
        cls.find_all_reservations()
        return True


if __name__ == "__main__":
    # Create a device
    reservation_service = ReservationService()
    print(reservation_service.find_all_reservations())
    #print(reservation_service.create_reservation("2", "Device2", "2021-01-01 00:00:00", "2021-01-02 00:00:00"))
    #print(reservation_service.create_reservation("one@mci.edu", "Device2", "2021-01-01 00:00:00", "2021-01-02 00:00:00"))
    print(reservation_service.create_reservation("one@mci.edu", "Device2", "2021-02-01 00:00:00", "2021-02-02 00:00:00"))
