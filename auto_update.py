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

    def fetch_events(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """Hämtar händelser från de senaste X dagarna"""
        try:
            params = {
                'locationname': 'Stockholm'
            }

            logging.info(f"🔍 API URL: {self.base_url}")
            logging.info(f"📍 Locationname: Stockholm (utan datum-filter)")

            response = requests.get(self.base_url, params=params, timeout=30)
            logging.info(f"📡 API Response: {response.status_code}")

            response.raise_for_status()

            events = response.json()
            logging.info(f"📥 Hämtade {len(events)} händelser från polisen.se")

            recent_events = self.filter_recent_events(events, days_back)
            logging.info(f"🗕️ Filtrerade till {len(recent_events)} händelser från senaste {days_back} dagarna")

            violence_events = self.filter_violence_events(recent_events)
            logging.info(f"🚨 Filtrerade till {len(violence_events)} våldshändelser")

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

    def filter_recent_events(self, events: List[Dict], days_back: int) -> List[Dict]:
        """Filtrera händelser till de senaste X dagarna"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            recent_events = []

            for event in events:
                event_datetime_str = event.get('datetime', '')
                if event_datetime_str:
                    try:
                        clean_datetime = event_datetime_str.split(' +')[0]
                        event_datetime = datetime.strptime(clean_datetime, '%Y-%m-%d %H:%M:%S')

                        if event_datetime >= cutoff_date:
                            recent_events.append(event)

                    except ValueError as e:
                        logging.warning(f"Kunde inte parsa datum {event_datetime_str}: {e}")
                        recent_events.append(event)

            return recent_events

        except Exception as e:
            logging.error(f"Fel vid filtrering av datum: {e}")
            return events
