import json
import streamlit as st
from datetime import datetime
from tinydb import TinyDB, Query
from devices import Device
from reservations import Reservation

class Maintenance:
    db_connector = TinyDB("maintenance_db.json").table("maintenances")

    def __init__(self, device_id, date, cost):
        self.device_id = device_id
        self.date = date
        self.cost = cost

    def store_data(self):
        """Speichert die Wartungsdaten in der JSON-Datenbank."""
        self.db_connector.insert({
            "device_id": self.device_id,
            "date": self.date,
            "cost": self.cost
        })

    @staticmethod
    def find_all():
        """Lädt alle gespeicherten Wartungsdaten aus der JSON-Datenbank."""
        return [Maintenance(d["device_id"], d["date"], d["cost"]) for d in Maintenance.db_connector.all()]

    @staticmethod
    def find_by_device(device_id):
        """Findet alle Wartungen für ein bestimmtes Gerät."""
        return [m for m in Maintenance.find_all() if m.device_id == device_id]
    
    @staticmethod
    def delete_maintenance(device_id, date):
        """Löscht eine bestimmte Wartung basierend auf Gerät-ID und Datum."""
        Maintenance.db_connector.remove(Query().device_id == device_id and Query().date == date)

    def __repr__(self):
        return f"Maintenance(device_id={self.device_id}, date={self.date}, cost={self.cost})"

# Streamlit UI-Erweiterung
st.title("Wartungsmanagement")

# Dropdown zur Geräteauswahl
devices = Device.find_all()
selected_device = st.selectbox("Gerät auswählen", [f"{d.device_name} (ID: {d.id})" for d in devices])

# Kalender zur Anzeige von Wartungen und Reservierungen
if selected_device:
    device_id = int(selected_device.split("(ID: ")[-1].strip(")"))
    maintenances = Maintenance.find_by_device(device_id)
    reservations = Reservation.find_by_device(device_id)
    
    st.subheader("Geplante Wartungen")
    for maintenance in maintenances:
        st.write(f"Datum: {maintenance.date}, Kosten: {maintenance.cost} EUR")
    
    st.subheader("Geplante Reservierungen")
    for reservation in reservations:
        st.write(f"Datum: {reservation.date}, Nutzer-ID: {reservation.user_id}")

# Automatische Nutzung der Wartungsdaten aus der Geräteverwaltung
st.subheader("Neue Wartung planen")
selected_device_obj = next((d for d in devices if d.id == device_id), None)
if selected_device_obj and selected_device_obj.next_maintenance:
    st.write(f"Nächste geplante Wartung: {selected_device_obj.next_maintenance}")
    maintenance_date = selected_device_obj.next_maintenance
else:
    maintenance_date = st.date_input("Wartungsdatum auswählen")

maintenance_cost = st.number_input("Wartungskosten eingeben (EUR)", min_value=0)

if st.button("Wartung speichern"):
    new_maintenance = Maintenance(device_id, maintenance_date, maintenance_cost)
    new_maintenance.store_data()
    st.success(f"Wartung für {selected_device} am {maintenance_date} gespeichert.")
