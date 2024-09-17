import streamlit as st
from streamlit_calendar import calendar
import json
from datetime import datetime, timedelta
from get_ical import fetch_ical, fix_timezone, modif_vevent, re_vevent
import re

st.set_page_config(layout="wide")

def load_masters_config(file_path: str):
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        if 'constant_events' not in config:
            config['constant_events'] = []
        return config
    except FileNotFoundError:
        st.error(f"Le fichier de configuration {file_path} n'a pas été trouvé.")
        return {"masters": [], "constant_events": []}
    except json.JSONDecodeError:
        st.error(f"Le fichier {file_path} n'est pas un JSON valide.")
        return {"masters": [], "constant_events": []}

def fetch_courses(code: str, start: str, end: str, year: int, fiche_etalon: str):
    try:
        ical = fetch_ical(code, start, end, year, fiche_etalon)
        ical_fixed = fix_timezone(ical, code)
        
        if ical_fixed is None:
            st.warning(f"Impossible de corriger le fuseau horaire pour le code {code}")
            return []
        
        tous_les_cours = []
        for match_event in re_vevent.finditer(ical_fixed):
            event = modif_vevent(match_event, 0, code)
            summary_match = re.search(r"SUMMARY:(.+)", event)
            dtstart_match = re.search(r"DTSTART;TZID=Europe/Paris:(\d{8}T\d{6})", event)
            dtend_match = re.search(r"DTEND;TZID=Europe/Paris:(\d{8}T\d{6})", event)
            location_match = re.search(r"LOCATION:(.+)", event)
            
            if summary_match and dtstart_match and dtend_match:
                start_time = datetime.strptime(dtstart_match.group(1), "%Y%m%dT%H%M%S")
                end_time = datetime.strptime(dtend_match.group(1), "%Y%m%dT%H%M%S")
                cours_info = {
                    "title": summary_match.group(1),
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "extendedProps": {
                        "location": location_match.group(1) if location_match else "Non spécifié"
                    }
                }
                tous_les_cours.append(cours_info)
        
        return tous_les_cours
    except Exception as e:
        st.error(f"Erreur lors de la récupération des cours pour le code {code}: {str(e)}")
        return []

def filter_courses(all_courses, selected_courses):
    return [course for course in all_courses if any(selected in course['title'] for selected in selected_courses)]

def main():
    st.title("Calendrier interactif M2 LOGOS")

    config = load_masters_config('m2_logos.json')
    start_date = "2024-09-16"
    end_date = "2025-07-17"
    annee_academique = 5
    fiche_etalon = "58598,"

    all_courses = []
    for master in config['masters']:
        with st.spinner(f"Récupération des cours pour {master['name']}..."):
            master_courses = fetch_courses(master['code'], start_date, end_date, annee_academique, fiche_etalon)
            all_courses.extend(master_courses)

    if not all_courses:
        st.warning("Aucun cours n'a pu être récupéré. Le calendrier sera vide (rechargez la page dans 1h, c'est probablement une erreur venant d'ADE).")

    st.header("Sélection des cours")
    selected_courses = []
    for master in config['masters']:
        st.subheader(master['name'])
        for course in master['courses']:
            if st.checkbox(course, key=f"{master['name']}_{course}"):
                selected_courses.append(course)

    st.header("Philosophie, linguistique et événements constants")
    
    for i, event in enumerate(config['constant_events']):
        col1, col2 = st.columns([3, 1])
        with col1:
            if event['type'] == 'weekly':
                st.write(f"{event['summary']} - {event['day']} à {event['time']} ({event['duration']} min) - {event['room']}")
            elif event['type'] == 'one-time':
                st.write(f"{event['summary']} - {event['date']} à {event['time']} ({event['duration']} min) - {event['room']}")
        with col2:
            config['constant_events'][i]['enabled'] = st.checkbox("Activer", value=event['enabled'], key=f"event_{i}")
    
    with st.expander("Ajouter un nouvel événement constant"):
        with st.form("new_constant_event"):
            event_type = st.selectbox("Type d'événement", ['weekly', 'one-time'])
            event_summary = st.text_input("Nom de l'événement")
            if event_type == 'weekly':
                event_day = st.selectbox("Jour", ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'])
            else:
                event_date = st.date_input("Date de l'événement")
            event_time = st.time_input("Heure de début")
            event_duration = st.number_input("Durée (en minutes)", min_value=15, step=15)
            event_room = st.text_input("Salle")
            if st.form_submit_button("Ajouter l'événement constant"):
                new_event = {
                    'type': event_type,
                    'summary': event_summary,
                    'time': event_time.strftime('%H:%M'),
                    'duration': event_duration,
                    'room': event_room,
                    'enabled': True
                }
                if event_type == 'weekly':
                    new_event['day'] = event_day
                else:
                    new_event['date'] = event_date.strftime("%Y-%m-%d")
                config['constant_events'].append(new_event)
                st.success("Événement constant ajouté avec succès!")

    logos_calendar = filter_courses(all_courses, selected_courses)
    
    # Ajout des événements constants au calendrier
    for event in config['constant_events']:
        if event['enabled']:
            if event['type'] == 'weekly':
                # Créer un événement récurrent
                logos_calendar.append({
                    'title': event['summary'],
                    'daysOfWeek': [['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'].index(event['day']) + 1],
                    'startTime': event['time'],
                    'endTime': (datetime.strptime(event['time'], '%H:%M') + timedelta(minutes=event['duration'])).strftime('%H:%M'),
                    'extendedProps': {
                        'location': event['room']
                    }
                })
            elif event['type'] == 'one-time':
                # Créer un événement unique
                start_datetime = f"{event['date']}T{event['time']}"
                end_datetime = (datetime.fromisoformat(start_datetime) + timedelta(minutes=event['duration'])).isoformat()
                logos_calendar.append({
                    'title': event['summary'],
                    'start': start_datetime,
                    'end': end_datetime,
                    'extendedProps': {
                        'location': event['room']
                    }
                })

    # Configuration du calendrier
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "initialView": "timeGridWeek",
        "slotMinTime": "08:00:00",
        "slotMaxTime": "20:00:00",
        "allDaySlot": False,
        "height": 700,
        "locale": "fr",
        "firstDay": 1,  # Lundi comme premier jour de la semaine
        "events": logos_calendar
    }

    # Affichage du calendrier
    st.header("Calendrier LOGOS")
    calendar_state = calendar(events=logos_calendar, options=calendar_options)

    # Affichage des détails de l'événement sélectionné
    if calendar_state.get("eventsSet") is not None:
        selected_event = calendar_state.get("eventClick")
        if selected_event:
            st.write(f"Événement sélectionné: {selected_event['event']['title']}")
            st.write(f"Début: {selected_event['event']['start']}")
            st.write(f"Fin: {selected_event['event']['end']}")
            if 'location' in selected_event['event']['extendedProps']:
                st.write(f"Lieu: {selected_event['event']['extendedProps']['location']}")

if __name__ == "__main__":
    main()