from reservations import Reservation
from devices_inheritance import Device
from users_inheritance import User

class ReservationService:
    def __init__(self):
        self.reservations = self.find_all_reservations()

    def find_all_reservations(self) -> list[Reservation]:
        return Reservation.find_all()

    def find_reservations_by_device(self, device_id: str) -> list[Reservation]:
        return [res for res in self.reservations if res.device_id == device_id]

    def find_reservations_by_user(self, user_id: str) -> list[Reservation]:
        return [res for res in self.reservations if res.user_id == user_id]

    def check_reservation_conflict(self, device_id: str, start_date: str, end_date: str) -> bool:
        for res in self.find_reservations_by_device(device_id):
            if (start_date <= res.end_date and end_date >= res.start_date):
                return True
        return False

    def create_reservation(self, user_id: str, device_id: str, start_date: str, end_date: str) -> bool:
        if not User.find_by_attribute("id", user_id):
            raise ValueError("Nutzer existiert nicht.")
        if not Device.find_by_attribute("id", device_id):
            raise ValueError("Gerät existiert nicht.")
        if self.check_reservation_conflict(device_id, start_date, end_date):
            raise ValueError("Reservierungskonflikt: Zeitraum überschneidet sich mit einer bestehenden Reservierung.")
        
        reservation = Reservation(user_id=user_id, device_id=device_id, start_date=start_date, end_date=end_date)
        reservation.store_data()
        self.reservations.append(reservation)
        return True