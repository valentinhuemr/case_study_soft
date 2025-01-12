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
    managed_by = st.text_input("Verantwortlicher Nutzer (E-Mail)", key="add_user")
    if st.button("Gerät speichern"):
        if device_name and managed_by:
            # Neues Gerät erstellen und speichern
            device = Device(device_name, managed_by)
            device.store_data()
            st.success(f"Gerät '{device_name}' wurde gespeichert.")
            
            # Gerät zur Liste im session_state hinzufügen
            st.session_state.devices.append(device_name)
        else:
            st.error("Bitte sowohl einen Gerätenamen als auch einen Nutzer angeben.")

    # Gerät umbenennen
    st.subheader("Gerät ändern")
    if st.session_state.devices:
        selected_device = st.selectbox("Gerät auswählen", st.session_state.devices, key="edit_device")
        new_name = st.text_input("Neuen Namen eingeben", value=selected_device, key="new_device_name")
        if st.button("Änderungen speichern"):
            if new_name:
                # Gerät aus der Datenbank laden und Namen ändern
                device = Device.find_by_attribute("device_name", selected_device)
                if device:
                    device.device_name = new_name  # Namen ändern
                    device.store_data()  # Änderungen speichern
                    st.success(f"Gerät '{selected_device}' wurde in '{new_name}' umbenannt.")
                    
                    # Gerät im session_state aktualisieren
                    st.session_state.devices = [d if d != selected_device else new_name for d in st.session_state.devices]
                else:
                    st.error(f"Gerät '{selected_device}' konnte nicht gefunden werden.")
            else:
                st.error("Bitte einen neuen Namen eingeben.")
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
        for user in all_users:
            st.write(user)
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