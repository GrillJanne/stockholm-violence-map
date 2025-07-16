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

# --- PoliceDataFetcher ---
class PoliceDataFetcher:
    ...

# --- LocationEnhancer ---
class LocationEnhancer:
    ...

# --- DataProcessor ---
class DataProcessor:
    """Bearbetar och formaterar data"""

    def __init__(self):
        self.location_enhancer = LocationEnhancer()

    def process_events(self, new_events: List[Dict], existing_data: Dict) -> Dict:
        try:
            existing_events = existing_data.get('events', [])
            existing_ids = {self.generate_event_id(event) for event in existing_events}
            processed_new_events = []

            for event in new_events:
                event_id = self.generate_event_id(event)
                if event_id in existing_ids:
                    continue
                enhanced_event = self.location_enhancer.enhance_location(event)
                formatted_event = self.format_event(enhanced_event)
                processed_new_events.append(formatted_event)

            all_events = existing_events + processed_new_events
            all_events.sort(key=lambda x: x.get('datetime', ''), reverse=True)

            return {
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'total_events': len(all_events),
                    'new_events_added': len(processed_new_events),
                    'data_source': 'polisen.se',
                    'automation_version': '1.0'
                },
                'events': all_events
            }

        except Exception as e:
            logging.error(f"Fel vid bearbetning av data: {e}")
            return existing_data

    def generate_event_id(self, event: Dict) -> str:
        date_str = event.get('datetime', '')
        event_type = event.get('type', '')
        location = event.get('location', {}).get('name', '')
        id_string = f"{date_str}_{event_type}_{location}"
        return hashlib.md5(id_string.encode()).hexdigest()[:12]

    def format_event(self, event: Dict) -> Dict:
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
        kommuner = [
            'Stockholm', 'Huddinge', 'Järfälla', 'Nacka', 'Solna', 'Sundbyberg',
            'Södertälje', 'Täby', 'Upplands Väsby', 'Vallentuna', 'Vaxholm',
            'Österåker', 'Botkyrka', 'Danderyd', 'Ekerö', 'Haninge', 'Lidingö',
            'Norrtälje', 'Nykvarn', 'Nynäshamn', 'Salem', 'Sigtuna', 'Sollentuna',
            'Tyresö', 'Värmdö'
        ]
        for kommun in kommuner:
            if kommun.lower() in location_name.lower():
                return kommun
        return 'Stockholm'

# --- Huvudfunktion ---
def main():
    from pathlib import Path
    class AutomationOrchestrator:
        def __init__(self):
            self.config = {
                'data_file': 'data.json',
                'days_back': 7
            }
            self.data_fetcher = PoliceDataFetcher()
            self.data_processor = DataProcessor()

        def load_existing_data(self) -> Dict:
            path = Path(self.config['data_file'])
            if path.exists():
                with path.open('r', encoding='utf-8') as f:
                    return json.load(f)
            return {'events': []}

        def save_data(self, data: Dict):
            with open(self.config['data_file'], 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        def run(self):
            new_events = self.data_fetcher.fetch_events(self.config['days_back'])
            if not new_events:
                logging.info("Inga nya händelser hittades")
                return
            existing_data = self.load_existing_data()
            updated_data = self.data_processor.process_events(new_events, existing_data)
            self.save_data(updated_data)

    orchestrator = AutomationOrchestrator()
    orchestrator.run()

if __name__ == '__main__':
    main()
