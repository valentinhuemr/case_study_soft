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
    
    # Geräte anlegen
    st.subheader("Gerät anlegen")
    device_name = st.text_input("Gerätename eingeben", key="add_device")

    # Lade alle vorhandenen Nutzer aus der Datenbank
    all_users = User.find_all()
    user_options = {user.name: user.id for user in all_users}  # Mapping: Nutzername -> Nutzer-ID

    if user_options:
        managed_by = st.selectbox("Verantwortlicher Nutzer auswählen", options=list(user_options.keys()), key="add_user")
    else:
        st.warning("Es sind keine Nutzer in der Nutzerverwaltung vorhanden. Bitte legen Sie erst Nutzer an.")
        managed_by = None

    if st.button("Gerät speichern"):
        if device_name and managed_by:
            # Neues Gerät erstellen und speichern
            user_id = user_options[managed_by]
            device = Device(device_name, user_id)
            device.store_data()
            st.success(f"Gerät '{device_name}' wurde gespeichert und '{managed_by}' ist der Verantwortliche.")
            
            # Gerät zur Liste im session_state hinzufügen
            st.session_state.devices.append(device_name)
        else:
            st.error("Bitte sowohl einen Gerätenamen als auch einen Nutzer auswählen.")

    # Gerät umbenennen
    st.subheader("Gerät ändern")
    if st.session_state.devices:
        selected_device = st.selectbox("Gerät auswählen", st.session_state.devices, key="edit_device")
        new_name = st.text_input("Neuen Namen eingeben", value=selected_device, key="new_device_name")
        
        if st.button("Änderungen speichern"):
            if new_name:
                # Lade das alte Gerät aus der Datenbank
                device = Device.find_by_attribute("device_name", selected_device)
                if device:
                    # Altes Gerät löschen
                    device.delete()
    
                    # Neues Gerät mit geändertem Namen erstellen
                    new_device = Device(new_name, device.managed_by_user_id)
                    new_device.store_data()
                    st.success(f"Gerät '{selected_device}' wurde in '{new_name}' umbenannt.")
                    
                    # Aktualisiere die Dropdown-Liste
                    st.session_state.devices = [d if d != selected_device else new_name for d in st.session_state.devices]
                else:
                    st.error(f"Gerät '{selected_device}' konnte nicht gefunden werden.")
            else:
                st.error("Bitte einen neuen Namen eingeben.")
                
        st.info("Tipp: Seite neu laden, um Änderungen zu sehen!")
    else:
        st.warning("Es sind keine Geräte vorhanden.")
    
# Nutzer-Verwaltung
if tabs == "Nutzerverwaltung":
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
    else:
        st.info("Keine Nutzer gefunden.")

    # Nutzer löschen
    st.subheader("Nutzer löschen")
    delete_user_email = st.text_input("E-Mail-Adresse des zu löschenden Nutzers", key="delete_user_email")
    if st.button("Nutzer löschen"):
        user = User.find_by_attribute("id", delete_user_email)
        if user:
            user.delete()
            st.success(f"Nutzer '{user.name}' wurde erfolgreich gelöscht.")
        else:
            st.error(f"Kein Nutzer mit der E-Mail-Adresse '{delete_user_email}' gefunden.")

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
