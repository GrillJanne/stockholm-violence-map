#!/usr/bin/env python3
"""
Stockholm Våldskarta - Automatisk Datauppdatering
Hämtar ny data från polisen.se och uppdaterar Netlify-deployment automatiskt
"""

import requests
import json
import os
import time
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)

class PoliceDataFetcher:
    """Hämtar data från polisen.se API"""
    
    def __init__(self):
        self.base_url = "https://polisen.se/api/events"
        self.stockholm_regions = [
            "Stockholm", "Stockholms län", "Huddinge", "Järfälla", 
            "Nacka", "Solna", "Sundbyberg", "Södertälje", "Täby",
            "Upplands Väsby", "Vallentuna", "Vaxholm", "Österåker",
            "Botkyrka", "Danderyd", "Ekerö", "Haninge", "Lidingö",
            "Norrtälje", "Nykvarn", "Nynäshamn", "Salem", "Sigtuna",
            "Sollentuna", "Tyresö", "Värmdö"
        ]
        
    def fetch_events(self, days_back: int = 14) -> List[Dict[str, Any]]:
        """Hämtar händelser från de senaste X dagarna"""
        try:
            # Beräkna datum
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            params = {
                'DateTime': f"{start_date.strftime('%Y-%m-%d')},{end_date.strftime('%Y-%m-%d')}",
                'locationname': ','.join(self.stockholm_regions)
            }
            
            logging.info(f"Hämtar data från {start_date.date()} till {end_date.date()}")
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            events = response.json()
            logging.info(f"Hämtade {len(events)} händelser från polisen.se")
            
            # Filtrera på våldsdåd
            violence_events = self.filter_violence_events(events)
            logging.info(f"Filtrerade till {len(violence_events)} våldshändelser")
            
            return violence_events
            
        except Exception as e:
            logging.error(f"Fel vid hämtning av data: {e}")
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

class LocationEnhancer:
    """Förbättrar koordinater för händelser"""
    
    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        
    def enhance_location(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Förbättrar koordinater för en händelse"""
        try:
            # Om koordinater redan finns och är bra, behåll dem
            if event.get('location', {}).get('gps'):
                lat, lon = event['location']['gps'].split(',')
                if abs(float(lat) - 59.3293) < 1 and abs(float(lon) - 18.0686) < 1:
                    event['latitude'] = float(lat)
                    event['longitude'] = float(lon)
                    event['location_confidence'] = 0.8
                    event['correction_method'] = 'original_gps'
                    return event
            
            # Försök förbättra med platsnamn
            location_name = event.get('location', {}).get('name', '')
            if location_name:
                coords = self.geocode_location(location_name)
                if coords:
                    event['latitude'] = coords[0]
                    event['longitude'] = coords[1]
                    event['location_confidence'] = 0.75
                    event['correction_method'] = 'geocoded'
                    event['specific_location'] = location_name
                    return event
            
            # Fallback till Stockholm centrum
            event['latitude'] = 59.3293
            event['longitude'] = 18.0686
            event['location_confidence'] = 0.3
            event['correction_method'] = 'fallback_stockholm'
            
            return event
            
        except Exception as e:
            logging.warning(f"Kunde inte förbättra koordinater för händelse: {e}")
            event['latitude'] = 59.3293
            event['longitude'] = 18.0686
            event['location_confidence'] = 0.3
            event['correction_method'] = 'error_fallback'
            return event
    
    def geocode_location(self, location: str) -> tuple:
        """Geocodar en plats till koordinater"""
        try:
            params = {
                'q': f"{location}, Stockholm, Sweden",
                'format': 'json',
                'limit': 1,
                'countrycodes': 'se'
            }
            
            response = requests.get(self.nominatim_url, params=params, timeout=10)
            response.raise_for_status()
            
            results = response.json()
            if results:
                return float(results[0]['lat']), float(results[0]['lon'])
            
            return None
            
        except Exception as e:
            logging.warning(f"Geocoding misslyckades för {location}: {e}")
            return None

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
            
            # Bearbeta nya händelser
            processed_new_events = []
            for event in new_events:
                event_id = self.generate_event_id(event)
                
                # Skippa om händelsen redan finns
                if event_id in existing_ids:
                    continue
                
                # Förbättra koordinater
                enhanced_event = self.location_enhancer.enhance_location(event)
                
                # Formatera händelse
                formatted_event = self.format_event(enhanced_event)
                processed_new_events.append(formatted_event)
            
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
                    'automation_version': '1.0'
                },
                'events': all_events
            }
            
            logging.info(f"Bearbetade {len(processed_new_events)} nya händelser")
            logging.info(f"Total dataset innehåller nu {len(all_events)} händelser")
            
            return updated_data
            
        except Exception as e:
            logging.error(f"Fel vid bearbetning av data: {e}")
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
            'specific_location': event.get('specific_location', ''),
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

class NetlifyDeployer:
    """Hanterar deployment till Netlify"""
    
    def __init__(self, site_id: str, access_token: str):
        self.site_id = site_id
        self.access_token = access_token
        self.api_base = "https://api.netlify.com/api/v1"
        
    def deploy_update(self, data_file_path: str, html_file_path: str) -> bool:
        """Deployer uppdaterad data till Netlify"""
        try:
            # Läs filer
            with open(data_file_path, 'r', encoding='utf-8') as f:
                data_content = f.read()
            
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Skapa deployment
            files = {
                'stockholm_violence_data.json': data_content,
                'index.html': html_content
            }
            
            deployment_data = {
                'files': files
            }
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Skapa deployment
            response = requests.post(
                f"{self.api_base}/sites/{self.site_id}/deploys",
                headers=headers,
                json=deployment_data,
                timeout=60
            )
            
            if response.status_code == 200:
                deploy_id = response.json()['id']
                logging.info(f"Deployment skapad: {deploy_id}")
                
                # Vänta på att deployment ska bli klar
                return self.wait_for_deployment(deploy_id)
            else:
                logging.error(f"Deployment misslyckades: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Fel vid deployment: {e}")
            return False
    
    def wait_for_deployment(self, deploy_id: str, max_wait: int = 300) -> bool:
        """Väntar på att deployment ska bli klar"""
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(
                    f"{self.api_base}/deploys/{deploy_id}",
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    deploy_data = response.json()
                    state = deploy_data.get('state')
                    
                    if state == 'ready':
                        logging.info("Deployment klar!")
                        return True
                    elif state == 'error':
                        logging.error("Deployment misslyckades")
                        return False
                    else:
                        logging.info(f"Deployment status: {state}")
                        time.sleep(10)
                else:
                    logging.warning(f"Kunde inte kontrollera deployment status: {response.status_code}")
                    time.sleep(10)
                    
            except Exception as e:
                logging.warning(f"Fel vid kontroll av deployment: {e}")
                time.sleep(10)
        
        logging.error("Deployment timeout")
        return False

class AutomationOrchestrator:
    """Huvudklass som orkestrerar hela automatiseringsprocessen"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config = self.load_config(config_file)
        self.data_fetcher = PoliceDataFetcher()
        self.data_processor = DataProcessor()
        
        # Netlify deployer (om konfigurerat)
        if self.config.get('netlify'):
            self.deployer = NetlifyDeployer(
                self.config['netlify']['site_id'],
                self.config['netlify']['access_token']
            )
        else:
            self.deployer = None
    
    def load_config(self, config_file: str) -> Dict:
        """Laddar konfiguration"""
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Skapa default config
                default_config = {
                    'data_file': 'stockholm_violence_data.json',
                    'html_file': 'index.html',
                    'backup_dir': 'backups',
                    'days_back': 14,
                    'netlify': {
                        'site_id': 'YOUR_NETLIFY_SITE_ID',
                        'access_token': 'YOUR_NETLIFY_ACCESS_TOKEN'
                    }
                }
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                
                logging.info(f"Skapade default konfiguration: {config_file}")
                return default_config
                
        except Exception as e:
            logging.error(f"Fel vid laddning av konfiguration: {e}")
            return {}
    
    def run_update(self) -> bool:
        """Kör en komplett uppdatering"""
        try:
            logging.info("Startar automatisk uppdatering av Stockholm Våldskarta")
            
            # 1. Hämta ny data från polisen
            new_events = self.data_fetcher.fetch_events(self.config.get('days_back', 7))
            
            if not new_events:
                logging.info("Inga nya händelser hittades")
                return True
            
            # 2. Ladda befintlig data
            existing_data = self.load_existing_data()
            
            # 3. Bearbeta och slå ihop data
            updated_data = self.data_processor.process_events(new_events, existing_data)
            
            # 4. Spara uppdaterad data
            self.save_data(updated_data)
            
            # 5. Skapa backup
            self.create_backup(updated_data)
            
            # 6. Deployer till Netlify (om konfigurerat)
            if self.deployer and updated_data['metadata']['new_events_added'] > 0:
                logging.info("Deployer uppdateringar till Netlify...")
                success = self.deployer.deploy_update(
                    self.config['data_file'],
                    self.config['html_file']
                )
                
                if success:
                    logging.info("Deployment till Netlify lyckades!")
                else:
                    logging.error("Deployment till Netlify misslyckades")
                    return False
            
            logging.info("Automatisk uppdatering slutförd framgångsrikt")
            return True
            
        except Exception as e:
            logging.error(f"Fel vid automatisk uppdatering: {e}")
            return False
    
    def load_existing_data(self) -> Dict:
        """Laddar befintlig data"""
        try:
            data_file = self.config.get('data_file', 'stockholm_violence_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logging.info("Ingen befintlig data hittades, skapar ny dataset")
                return {'events': []}
                
        except Exception as e:
            logging.error(f"Fel vid laddning av befintlig data: {e}")
            return {'events': []}
    
    def save_data(self, data: Dict) -> None:
        """Sparar data till fil"""
        try:
            data_file = self.config.get('data_file', 'stockholm_violence_data.json')
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Data sparad till {data_file}")
            
        except Exception as e:
            logging.error(f"Fel vid sparning av data: {e}")
    
    def create_backup(self, data: Dict) -> None:
        """Skapar backup av data"""
        try:
            backup_dir = self.config.get('backup_dir', 'backups')
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(backup_dir, f'stockholm_violence_data_{timestamp}.json')
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Backup skapad: {backup_file}")
            
        except Exception as e:
            logging.warning(f"Kunde inte skapa backup: {e}")

def main():
    """Huvudfunktion"""
    orchestrator = AutomationOrchestrator()
    success = orchestrator.run_update()

    # I main() funktionen, lägg till:
print(f"🔍 Kontrollerar {len(new_events)} nya händelser mot {len(existing_signatures)} befintliga")

for event in new_events:
    signature = f"{event.get('datetime', '')}_{event.get('type', '')}_{event.get('location', {}).get('name', '')}"
    if signature not in existing_signatures:
        print(f"➕ Ny händelse: {signature}")
    else:
        print(f"🔄 Duplikat: {signature}")

    
    if success:
        logging.info("Automatisering slutförd framgångsrikt")
        exit(0)
    else:
        logging.error("Automatisering misslyckades")
        exit(1)

if __name__ == "__main__":
    main()

