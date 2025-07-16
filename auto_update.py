#!/usr/bin/env python3
"""
Stockholm Våldskarta - Automatisk Datauppdatering
Hämtar ny data från polisen.se och uppdaterar JSON-filen automatiskt
"""

import requests
import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PoliceDataFetcher:
    """Hämtar data från polisen.se API"""
    
    def __init__(self):
        self.base_url = "https://polisen.se/api/events"
        
    def fetch_events(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Hämtar händelser från polisen.se"""
        try:
            # Enkla parametrar - bara Stockholm, inget datum
            params = {
                'locationname': 'Stockholm'
            }
            
            logging.info(f"🔍 Hämtar händelser från polisen.se")
            logging.info(f"📍 Locationname: Stockholm")
            
            response = requests.get(self.base_url, params=params, timeout=30)
            logging.info(f"📡 API Response: {response.status_code}")
            
            if response.status_code != 200:
                logging.error(f"API fel: {response.status_code} - {response.text}")
                return []
            
            events = response.json()
            logging.info(f"📥 Hämtade {len(events)} händelser från polisen.se")
            
            # Filtrera på våldsdåd
            violence_events = self.filter_violence_events(events)
            logging.info(f"🚨 Filtrerade till {len(violence_events)} våldshändelser")
            
            # Filtrera på senaste dagarna
            recent_events = self.filter_recent_events(violence_events, days_back)
            logging.info(f"📅 Filtrerade till {len(recent_events)} händelser från senaste {days_back} dagarna")
            
            return recent_events
            
        except Exception as e:
            logging.error(f"❌ Fel vid hämtning av data: {e}")
            return []
    
    def filter_violence_events(self, events: List[Dict]) -> List[Dict]:
        """Filtrera ut våldshändelser"""
        violence_keywords = [
            'misshandel', 'rån', 'våldtäkt', 'mord', 'dråp', 'skottlossning',
            'explosion', 'sprängning', 'sexualbrott', 'våld', 'hot'
        ]
        
        filtered_events = []
        for event in events:
            event_type = event.get('type', '').lower()
            summary = event.get('summary', '').lower()
            
            if any(keyword in event_type or keyword in summary for keyword in violence_keywords):
                filtered_events.append(event)
        
        return filtered_events
    
    def filter_recent_events(self, events: List[Dict], days_back: int) -> List[Dict]:
        """Filtrera händelser till de senaste X dagarna"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            recent_events = []
            
            for event in events:
                event_datetime_str = event.get('datetime', '')
                if event_datetime_str:
                    try:
                        # Polisen.se format: 2024-01-15 14:30:00 +01:00
                        # Ta bort timezone för parsing
                        clean_datetime = event_datetime_str.split(' +')[0]
                        event_datetime = datetime.strptime(clean_datetime, '%Y-%m-%d %H:%M:%S')
                        
                        if event_datetime >= cutoff_date:
                            recent_events.append(event)
                            
                    except ValueError:
                        # Om datum-parsing misslyckas, inkludera händelsen ändå
                        recent_events.append(event)
                else:
                    # Om inget datum finns, inkludera händelsen
                    recent_events.append(event)
            
            return recent_events
            
        except Exception as e:
            logging.error(f"❌ Fel vid filtrering av datum: {e}")
            return events

class LocationEnhancer:
    """Förbättrar koordinater för händelser"""
    
    def enhance_location(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Förbättrar koordinater för en händelse"""
        try:
            # Om koordinater redan finns och är rimliga
            if event.get('location', {}).get('gps'):
                gps_str = event['location']['gps']
                if ',' in gps_str:
                    try:
                        lat, lon = gps_str.split(',')
                        lat, lon = float(lat.strip()), float(lon.strip())
                        
                        # Kontrollera att koordinaterna är i Stockholm-området
                        if 58.5 <= lat <= 60.5 and 17.0 <= lon <= 19.0:
                            event['latitude'] = lat
                            event['longitude'] = lon
                            event['location_confidence'] = 0.8
                            event['correction_method'] = 'original_gps'
                            return event
                    except (ValueError, IndexError):
                        pass
            
            # Fallback till Stockholm centrum
            event['latitude'] = 59.3293
            event['longitude'] = 18.0686
            event['location_confidence'] = 0.3
            event['correction_method'] = 'fallback_stockholm'
            
            return event
            
        except Exception as e:
            logging.warning(f"⚠️ Kunde inte förbättra koordinater: {e}")
            event['latitude'] = 59.3293
            event['longitude'] = 18.0686
            event['location_confidence'] = 0.3
            event['correction_method'] = 'error_fallback'
            return event

class DataProcessor:
    """Bearbetar och formaterar data"""
    
    def __init__(self):
        self.location_enhancer = LocationEnhancer()
    
    def process_events(self, new_events: List[Dict], existing_data: Dict) -> Dict:
        """Bearbetar nya händelser och slår ihop med befintlig data"""
        try:
            existing_events = existing_data.get('events', [])
            
            # Skapa set av befintliga händelse-ID:n
            existing_ids = {self.generate_event_id(event) for event in existing_events}
            
            logging.info(f"📊 Befintliga händelser: {len(existing_events)}")
            logging.info(f"🔍 Kontrollerar {len(new_events)} nya händelser")
            
            # Bearbeta nya händelser
            processed_new_events = []
            for event in new_events:
                event_id = self.generate_event_id(event)
                
                # Skippa om händelsen redan finns
                if event_id in existing_ids:
                    logging.debug(f"🔄 Hoppar över duplikat: {event_id}")
                    continue
                
                # Förbättra koordinater
                enhanced_event = self.location_enhancer.enhance_location(event)
                
                # Formatera händelse
                formatted_event = self.format_event(enhanced_event)
                processed_new_events.append(formatted_event)
                
                logging.info(f"➕ Ny händelse: {event.get('type', 'N/A')} - {event.get('location', {}).get('name', 'N/A')}")
            
            # Slå ihop med befintlig data
            all_events = existing_events + processed_new_events
            
            # Sortera efter datum (nyast först)
            all_events.sort(key=lambda x: x.get('datetime', ''), reverse=True)
            
            # Skapa uppdaterad dataset
            updated_data = {
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'total_events': len(all_events),
                    'new_events_added': len(processed_new_events),
                    'data_source': 'polisen.se',
                    'automation_version': '2.0',
                    'github_actions': True
                },
                'events': all_events
            }
            
            logging.info(f"✅ Bearbetade {len(processed_new_events)} nya händelser")
            logging.info(f"📊 Total dataset innehåller nu {len(all_events)} händelser")
            
            return updated_data
            
        except Exception as e:
            logging.error(f"❌ Fel vid bearbetning av data: {e}")
            return existing_data
    
    def generate_event_id(self, event: Dict) -> str:
        """Genererar unikt ID för en händelse"""
        # Använd datum, typ och plats för att skapa unikt ID
        date_str = event.get('datetime', '')
        event_type = event.get('type', '')
        location = event.get('location', {}).get('name', '')
        
        id_string = f"{date_str}_{event_type}_{location}"
        return hashlib.md5(id_string.encode()).hexdigest()[:12]
    
    def format_event(self, event: Dict) -> Dict:
        """Formaterar en händelse till vårt dataformat"""
        return {
            'id': self.generate_event_id(event),
            'datetime': event.get('datetime', ''),
            'type': event.get('type', ''),
            'summary': event.get('summary', ''),
            'location_name': event.get('location', {}).get('name', ''),
            'latitude': event.get('latitude'),
            'longitude': event.get('longitude'),
            'location_confidence': event.get('location_confidence', 0.5),
            'correction_method': event.get('correction_method', 'unknown'),
            'kommun': self.extract_kommun(event.get('location', {}).get('name', '')),
            'url': event.get('url', ''),
            'added_by_automation': True,
            'added_timestamp': datetime.now().isoformat()
        }
    
    def extract_kommun(self, location_name: str) -> str:
        """Extraherar kommun från platsnamn"""
        stockholm_kommuner = [
            'Stockholm', 'Huddinge', 'Järfälla', 'Nacka', 'Solna',
            'Sundbyberg', 'Södertälje', 'Täby', 'Upplands Väsby',
            'Vallentuna', 'Vaxholm', 'Österåker', 'Botkyrka',
            'Danderyd', 'Ekerö', 'Haninge', 'Lidingö', 'Norrtälje',
            'Nykvarn', 'Nynäshamn', 'Salem', 'Sigtuna', 'Sollentuna',
            'Tyresö', 'Värmdö'
        ]
        
        for kommun in stockholm_kommuner:
            if kommun.lower() in location_name.lower():
                return kommun
        
        return 'Stockholm'  # Default

def main():
    """Huvudfunktion för automatisk uppdatering"""
    try:
        logging.info("🚀 Stockholm Våldskarta - Auto Update startar")
        logging.info("=" * 60)
        
        # Initiera komponenter
        data_fetcher = PoliceDataFetcher()
        data_processor = DataProcessor()
        
        # Hämta nya händelser
        new_events = data_fetcher.fetch_events(days_back=31)  # 14 dagar för att få fler händelser
        
        if not new_events:
            logging.info("ℹ️ Inga nya våldshändelser hittades")
            return
        
        # Ladda befintlig data
        try:
            with open('stockholm_violence_data.json', 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            logging.info("📂 Laddade befintlig data")
        except FileNotFoundError:
            logging.info("📂 Ingen befintlig data hittades, skapar ny dataset")
            existing_data = {'events': []}
        except Exception as e:
            logging.error(f"❌ Fel vid laddning av befintlig data: {e}")
            existing_data = {'events': []}
        
        # Bearbeta och uppdatera data
        updated_data = data_processor.process_events(new_events, existing_data)
        
        # Kontrollera om nya händelser lades till
        new_events_added = updated_data.get('metadata', {}).get('new_events_added', 0)
        
        if new_events_added == 0:
            logging.info("ℹ️ Inga nya unika händelser att lägga till")
            return
        
        # Spara uppdaterad data
        with open('stockholm_violence_data.json', 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"✅ Sparade uppdaterad data med {new_events_added} nya händelser")
        logging.info(f"📊 Totalt antal händelser: {updated_data.get('metadata', {}).get('total_events', 0)}")
        logging.info("🎉 Automatisk uppdatering slutförd framgångsrikt!")
        
    except Exception as e:
        logging.error(f"❌ Kritiskt fel i huvudfunktionen: {e}")
        raise

if __name__ == '__main__':
    main()

