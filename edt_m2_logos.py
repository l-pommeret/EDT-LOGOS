import streamlit as st
from streamlit_calendar import calendar
import json
from datetime import datetime, timedelta
import re
from get_ical import fetch_ical, fix_timezone, modif_vevent, re_vevent

st.set_page_config(layout="wide")

def load_masters_config(file_path: str):
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
        if 'constant_events' not in config:
            config['constant_events'] = []
        # Vérification de la structure des cours
        for master in config['masters']:
            if not all(isinstance(course, dict) and 'name' in course and 'displayName' in course and 'color' in course for course in master['courses']):
                raise ValueError("La structure des cours dans le fichier JSON est incorrecte.")
        return config
    except FileNotFoundError:
        st.error(f"Le fichier de configuration {file_path} n'a pas été trouvé.")
        return {"masters": [], "constant_events": []}
    except json.JSONDecodeError:
        st.error(f"Le fichier {file_path} n'est pas un JSON valide.")
        return {"masters": [], "constant_events": []}
    except ValueError as e:
        st.error(str(e))
        return {"masters": [], "constant_events": []}

def fetch_courses(code: str, start: str, end: str, year: int, fiche_etalon: str, json_courses):
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
                location = location_match.group(1) if location_match else "Non spécifié"
                summary = summary_match.group(1)
                
                json_course = next((course for course in json_courses if course['name'] in summary), None)
                
                if json_course:
                    cours_info = {
                        "title": f"{json_course['displayName']} - {location}",
                        "start": start_time.isoformat(),
                        "end": end_time.isoformat(),
                        "backgroundColor": json_course['color'],
                        "extendedProps": {
                            "location": location,
                            "original_summary": summary
                        }
                    }
                    tous_les_cours.append(cours_info)
        
        return tous_les_cours
    except Exception as e:
        st.error(f"Erreur lors de la récupération des cours pour le code {code}: {str(e)}")
        return []

def filter_courses(all_courses, selected_courses):
    return [course for course in all_courses if any(selected in course['extendedProps']['original_summary'] for selected in selected_courses)]

def create_constant_event(event, is_weekly):
    if is_weekly:
        return {
            'title': f"{event['summary']} - {event['room']}",
            'daysOfWeek': [['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'].index(event['day']) + 1],
            'startTime': event['time'],
            'endTime': (datetime.strptime(event['time'], '%H:%M') + timedelta(minutes=event['duration'])).strftime('%H:%M'),
            'backgroundColor': event.get('color', '#808080'),  # Gris par défaut si pas de couleur spécifiée
            'extendedProps': {
                'location': event['room']
            }
        }
    else:
        start_datetime = f"{event['date']}T{event['time']}"
        end_datetime = (datetime.fromisoformat(start_datetime) + timedelta(minutes=event['duration'])).isoformat()
        return {
            'title': f"{event['summary']} - {event['room']}",
            'start': start_datetime,
            'end': end_datetime,
            'backgroundColor': event.get('color', '#808080'),  # Gris par défaut si pas de couleur spécifiée
            'extendedProps': {
                'location': event['room']
            }
        }

def main():
    st.title("Calendrier interactif M2 LOGOS")

    config = load_masters_config('m2_logos.json')
    start_date = "2024-09-16"
    end_date = "2025-07-17"
    annee_academique = 5
    fiche_etalon = "58598,"

    all_courses = []
    json_courses = [course for master in config['masters'] for course in master['courses']]
    for master in config['masters']:
        with st.spinner(f"Récupération des cours pour {master['name']}..."):
            master_courses = fetch_courses(master['code'], start_date, end_date, annee_academique, fiche_etalon, json_courses)
            all_courses.extend(master_courses)

    if not all_courses:
        st.warning("Aucun cours n'a pu être récupéré. Le calendrier sera vide (rechargez la page dans 1h, c'est probablement une erreur venant d'ADE).")

    st.header("Mathématiques, logique, informatique")
    selected_courses = []
    grouped_courses = {}
    for master in config['masters']:
        for course in master['courses']:
            if course['groupId'] not in grouped_courses:
                grouped_courses[course['groupId']] = {
                    'displayName': course['displayName'],
                    'names': [course['name']]
                }
            else:
                grouped_courses[course['groupId']]['names'].append(course['name'])

    for group_id, group_info in grouped_courses.items():
        if st.checkbox(group_info['displayName'], key=f"group_{group_id}"):
            selected_courses.extend(group_info['names'])

    st.header("Philosophie, linguistique et événements constants")
    
    grouped_events = {}
    for event in config['constant_events']:
        if event['groupId'] not in grouped_events:
            grouped_events[event['groupId']] = {
                'summary': event['summary'],
                'events': [event]
            }
        else:
            grouped_events[event['groupId']]['events'].append(event)

    for group_id, group_info in grouped_events.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            if len(group_info['events']) > 1:
                st.write(f"{group_info['summary']} (plusieurs sessions)")
            else:
                event = group_info['events'][0]
                if event['type'] == 'weekly':
                    st.write(f"{event['summary']} - {event['day']} à {event['time']} ({event['duration']} min) - {event['room']}")
                elif event['type'] == 'one-time':
                    st.write(f"{event['summary']} - {event['date']} à {event['time']} ({event['duration']} min) - {event['room']}")
        with col2:
            enabled = st.checkbox("Activer", value=group_info['events'][0]['enabled'], key=f"event_{group_id}")
            for event in group_info['events']:
                event['enabled'] = enabled

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
            event_color = st.color_picker("Couleur de l'événement", '#808080')
            if st.form_submit_button("Ajouter l'événement constant"):
                new_event = {
                    'type': event_type,
                    'summary': event_summary,
                    'time': event_time.strftime('%H:%M'),
                    'duration': event_duration,
                    'room': event_room,
                    'enabled': True,
                    'color': event_color
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
            logos_calendar.append(create_constant_event(event, event['type'] == 'weekly'))

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
        "hiddenDays": [0, 6],  # Cache le dimanche (0) et le samedi (6)
        "weekends": False  # Désactive l'affichage des week-ends
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