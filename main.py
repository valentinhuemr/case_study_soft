import streamlit as st
from devices import Device
from users import User
from serializer import serializer

# Hauptüberschrift
st.title("Geräteverwaltungssoftware für Hochschulen")

# Initialisieren der Geräte im session_state, falls sie noch nicht existieren
if "devices" not in st.session_state:
    st.session_state.devices = [d.device_name for d in Device.find_all()]

# Navigation für die Module
tabs = st.sidebar.radio("Navigation", [
    "Geräteverwaltung",
    "Nutzerverwaltung",
    "Reservierungssystem",
    "Wartungs-Management"
])

# Geräte-Verwaltung
if tabs == "Geräteverwaltung":
    st.header("Geräteverwaltung")

    # Gerät anlegen
    st.subheader("Gerät anlegen")
    device_name = st.text_input("Gerätename eingeben")
    managed_by = st.selectbox("Verantwortlicher Nutzer auswählen", [f"{user.name} ({user.id})" for user in User.find_all()])
    end_of_life = st.date_input("End of Life eingeben (optional)")
    maintenance_interval = st.number_input("Wartungsintervall in Tagen (optional)", min_value=1, step=1)
    maintenance_cost = st.number_input("Wartungskosten pro Wartung (optional)", min_value=0.0, step=0.1)
    first_maintenance = st.date_input("Erste Wartung (optional)")

    if st.button("Gerät speichern"):
        if device_name and managed_by:
            user_id = managed_by.split("(")[-1][:-1]  # E-Mail extrahieren
            device = Device(
                device_name=device_name,
                managed_by_user_id=user_id,
                end_of_life=end_of_life.isoformat() if end_of_life else None,
                maintenance_interval=maintenance_interval,
                maintenance_cost=maintenance_cost,
                first_maintenance=first_maintenance.isoformat() if first_maintenance else None
            )
            device.store_data()
            st.success(f"Gerät '{device_name}' wurde gespeichert.")
        else:
            st.error("Bitte sowohl einen Gerätenamen als auch einen Nutzer angeben.")

    # Geräte anzeigen
    st.subheader("Geräte")
    devices = Device.find_all()  # Lade alle Geräte aus der Datenbank
    if devices:
        # Dropdown-Menü mit Gerätenamen und IDs
        selected_device = st.selectbox("Wähle ein Gerät aus", [f"{device.device_name} (ID: {device.id})" for device in devices])
        # Gerät auswählen
        selected_device_obj = next((device for device in devices if f"{device.device_name} (ID: {device.id})" == selected_device), None)
        if selected_device_obj:
            # Zeige alle Daten des Geräts an
            st.write("Details zum Gerät:")
            st.write(f"**Gerätename:** {selected_device_obj.device_name}")
            st.write(f"**Geräte-ID:** {selected_device_obj.id}")
            st.write(f"**Verantwortlicher Nutzer:** {selected_device_obj.managed_by_user_id}")
            st.write(f"**Aktiv:** {'Ja' if selected_device_obj.is_active else 'Nein'}")
            st.write(f"**End of Life:** {selected_device_obj.end_of_life if selected_device_obj.end_of_life else 'Keine Angabe'}")
            st.write(f"**Erste Wartung:** {selected_device_obj.first_maintenance if selected_device_obj.first_maintenance else 'Keine Angabe'}")
            st.write(f"**Nächste Wartung:** {selected_device_obj.next_maintenance if selected_device_obj.next_maintenance else 'Keine Angabe'}")
            st.write(f"**Wartungsintervall:** {selected_device_obj.__dict__.get('_Device__maintenance_interval', 'Keine Angabe')} Tage")
            st.write(f"**Wartungskosten:** {selected_device_obj.__dict__.get('_Device__maintenance_cost', 'Keine Angabe')} EUR")
            st.write(f"**Erstellungsdatum:** {selected_device_obj.__dict__.get('_Device__creation_date', 'Keine Angabe')}")
            st.write(f"**Letzte Änderung:** {selected_device_obj.__dict__.get('_Device__last_update', 'Keine Angabe')}")
            
            # Lösch-Button hinzufügen
            if st.button("Gerät löschen"):
                selected_device_obj.delete()
                st.success(f"Gerät '{selected_device_obj.device_name}' wurde erfolgreich gelöscht.")
                # Seite neu laden, um die Änderungen anzuzeigen
                st.experimental_rerun()
    else:
        st.info("Keine Geräte vorhanden.")

# Nutzer-Verwaltung
elif tabs == "Nutzerverwaltung":
    st.header("Nutzerverwaltung")

    # Nutzer anlegen
    st.subheader("Nutzer anlegen")
    user_email = st.text_input("E-Mail-Adresse des Nutzers eingeben", key="add_user_email")
    user_name = st.text_input("Name des Nutzers eingeben", key="add_user_name")
    if st.button("Nutzer speichern"):
        if user_email and user_name:
            # Neuen Nutzer erstellen und speichern
            user = User(user_email, user_name)
            user.store_data()
            st.success(f"Nutzer '{user_name}' ({user_email}) wurde erfolgreich gespeichert.")
        else:
            st.error("Bitte sowohl eine E-Mail-Adresse als auch einen Namen angeben.")

    # Alle Nutzer anzeigen
    st.subheader("Alle Nutzer anzeigen")
    all_users = User.find_all()

    if all_users:
        # Nutzer in ein Dropdown-Menü einfügen
        selected_user = st.selectbox(
            "Wähle einen Nutzer aus", 
            options=[f"{user.name} ({user.id})" for user in all_users]
        )
        st.write(f"Ausgewählter Nutzer: {selected_user}")

        # Lösch-Button für den ausgewählten Nutzer
        if st.button("Ausgewählten Nutzer löschen"):
            user_id = selected_user.split("(")[-1][:-1]  # Extrahiere die ID (E-Mail-Adresse)
            user_to_delete = User.find_by_attribute("id", user_id)
            if user_to_delete:
                user_to_delete.delete()
                st.success(f"Nutzer '{user_to_delete.name}' wurde erfolgreich gelöscht.")
                st.experimental_rerun()
            else:
                st.error("Der ausgewählte Nutzer konnte nicht gefunden werden.")
    else:
        st.info("Keine Nutzer gefunden.")

# Reservierungssystem
elif tabs == "Reservierungssystem":
    st.header("Reservierungssystem")
    st.subheader("Reservierungen anzeigen")
    reservations = [
        {"Gerät": "Laser-Cutter", "Datum": "2025-01-10", "Nutzer": "Max Mustermann"},
        {"Gerät": "3D-Drucker", "Datum": "2025-01-11", "Nutzer": "Anna Müller"}
    ]
    for res in reservations:
        st.write(f"Gerät: {res['Gerät']}, Datum: {res['Datum']}, Nutzer: {res['Nutzer']}")

    st.subheader("Reservierung eintragen")
    selected_device = st.selectbox("Gerät auswählen", ["Laser-Cutter", "3D-Drucker", "Fräsmaschine"])
    reservation_date = st.date_input("Datum auswählen")
    reservation_user = st.text_input("Nutzername eingeben")
    if st.button("Reservierung speichern"):
        st.write(f"Reservierung für '{selected_device}' am '{reservation_date}' für Nutzer '{reservation_user}' wurde gespeichert.")

# Wartungs-Management
elif tabs == "Wartungs-Management":
    st.header("Wartungs-Management")
    st.subheader("Wartungen anzeigen")
    maintenances = [
        {"Gerät": "Laser-Cutter", "Datum": "2025-01-05", "Kosten": "100 EUR"},
        {"Gerät": "3D-Drucker", "Datum": "2025-01-08", "Kosten": "150 EUR"}
    ]
    for main in maintenances:
        st.write(f"Gerät: {main['Gerät']}, Datum: {main['Datum']}, Kosten: {main['Kosten']}")

    st.subheader("Wartungskosten anzeigen")
    selected_device = st.selectbox("Gerät auswählen", ["Laser-Cutter", "3D-Drucker", "Fräsmaschine"], key="maintenance")
    maintenance_cost = st.number_input("Wartungskosten eingeben (EUR)", min_value=0)
    if st.button("Kosten speichern"):
        st.write(f"Wartungskosten für '{selected_device}' wurden auf {maintenance_cost} EUR gesetzt.")
