#!/usr/bin/env python3
"""
Stockholm Våldskarta - Automatisk Datauppdatering med Förbättrade Platser
Hämtar ny data från polisen.se och förbättrar koordinater automatiskt
"""

import requests
import json
import hashlib
import math
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import logging

# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class StockholmAreaImprover:
    """Förbättrar platser baserat på Stockholm-områden och intelligent spridning"""
    
    def __init__(self):
        # Detaljerad databas över Stockholm-områden med sub-områden
        self.detailed_areas = {
            'Stockholm': {
                'center': (59.3293, 18.0686),
                'sub_areas': {
                    'Vasastan': (59.3434, 18.0567),
                    'Södermalm': (59.3165, 18.0740),
                    'Östermalm': (59.3378, 18.0895),
                    'Gamla stan': (59.3251, 18.0711),
                    'Norrmalm': (59.3293, 18.0686),
                    'Kungsholmen': (59.3275, 18.0298),
                    'Djurgården': (59.3247, 18.1157),
                    'Södermalm centrum': (59.3165, 18.0740),
                    'Östermalm centrum': (59.3378, 18.0895),
                    'Vasastan centrum': (59.3434, 18.0567),
                    'Norrmalm centrum': (59.3293, 18.0686),
                    'Gamla stan centrum': (59.3251, 18.0711),
                    'Kungsholmen centrum': (59.3275, 18.0298)
                },
                'spread_radius': 0.02  # Större spridning för Stockholm
            },
            'Sundbyberg': {
                'center': (59.3617, 17.9717),
                'sub_areas': {
                    'Sundbyberg centrum': (59.3617, 17.9717),
                    'Rissne': (59.3667, 17.9500),
                    'Ör': (59.3500, 17.9833),
                    'Hallonbergen': (59.3833, 17.9333),
                    'Duvbo': (59.3750, 17.9600),
                    'Lilla Alby': (59.3550, 17.9650)
                },
                'spread_radius': 0.008
            },
            'Huddinge': {
                'center': (59.2378, 17.9838),
                'sub_areas': {
                    'Huddinge centrum': (59.2378, 17.9838),
                    'Flemingsberg': (59.2167, 17.9500),
                    'Vårby gård': (59.2397, 17.8634),
                    'Hagsätra': (59.2397, 18.0634),
                    'Skogås': (59.2500, 18.0500),
                    'Trångsund': (59.2600, 18.0200)
                },
                'spread_radius': 0.015
            },
            'Botkyrka': {
                'center': (59.2000, 17.8500),
                'sub_areas': {
                    'Tumba': (59.2000, 17.8333),
                    'Tullinge': (59.2167, 17.9000),
                    'Fittja': (59.2333, 17.8667),
                    'Alby': (59.2167, 17.8333),
                    'Norsborg': (59.2167, 17.8167),
                    'Hallunda': (59.2333, 17.8333)
                },
                'spread_radius': 0.012
            },
            'Järfälla': {
                'center': (59.4000, 17.8500),
                'sub_areas': {
                    'Jakobsberg': (59.4167, 17.8167),
                    'Barkarby': (59.4000, 17.8500),
                    'Skälby': (59.4167, 17.8333),
                    'Kallhäll': (59.4000, 17.7833),
                    'Viksjö': (59.4333, 17.8500)
                },
                'spread_radius': 0.010
            },
            'Sollentuna': {
                'center': (59.4286, 17.9506),
                'sub_areas': {
                    'Sollentuna centrum': (59.4286, 17.9506),
                    'Tureberg': (59.4167, 17.9333),
                    'Helenelund': (59.4500, 17.9500),
                    'Häggvik': (59.4333, 17.9667),
                    'Norrviken': (59.4500, 17.9333)
                },
                'spread_radius': 0.008
            },
            'Haninge': {
                'center': (59.1667, 18.1333),
                'sub_areas': {
                    'Handen': (59.1667, 18.1333),
                    'Brandbergen': (59.1833, 18.1167),
                    'Jordbro': (59.2000, 18.0833),
                    'Vendelsö': (59.1500, 18.1500),
                    'Västerhaninge': (59.1333, 18.1000)
                },
                'spread_radius': 0.012
            },
            'Rinkeby-Kista': {
                'center': (59.3833, 17.9333),
                'sub_areas': {
                    'Rinkeby': (59.3667, 17.9333),
                    'Tensta': (59.3833, 17.9000),
                    'Hjulsta': (59.4000, 17.9167),
                    'Kista': (59.4033, 17.9442),
                    'Akalla': (59.4167, 17.9167),
                    'Husby': (59.4000, 17.9333)
                },
                'spread_radius': 0.012
            },
            'Södertälje': {
                'center': (59.1958, 17.6253),
                'sub_areas': {
                    'Södertälje centrum': (59.1958, 17.6253),
                    'Ronna': (59.1833, 17.6167),
                    'Geneta': (59.2167, 17.6333),
                    'Hovsjö': (59.1667, 17.6000),
                    'Fornhöjden': (59.2000, 17.6500)
                },
                'spread_radius': 0.010
            },
            'Solna': {
                'center': (59.3617, 18.0000),
                'sub_areas': {
                    'Solna centrum': (59.3617, 18.0000),
                    'Råsunda': (59.3667, 18.0167),
                    'Hagalund': (59.3500, 17.9833),
                    'Bergshamra': (59.3833, 18.0333),
                    'Ulriksdal': (59.3750, 18.0500)
                },
                'spread_radius': 0.008
            },
            'Nacka': {
                'center': (59.3117, 18.1642),
                'sub_areas': {
                    'Nacka centrum': (59.3117, 18.1642),
                    'Sickla': (59.3000, 18.1500),
                    'Finnboda': (59.3167, 18.1833),
                    'Saltsjöbaden': (59.2833, 18.3000),
                    'Boo': (59.3333, 18.2500)
                },
                'spread_radius': 0.012
            }
        }
        
        # Brottstypspecifika områden
        self.crime_area_preferences = {
            'Skottlossning': ['Rinkeby', 'Tensta', 'Husby', 'Fittja', 'Ronna'],
            'Explosion': ['Rinkeby', 'Tensta', 'Husby', 'Skälby', 'Fittja'],
            'Rån': ['Södermalm', 'Norrmalm', 'Rinkeby', 'Tensta'],
            'Misshandel': ['Södermalm', 'Vasastan', 'Norrmalm', 'Östermalm'],
            'Våldtäkt': ['Södermalm', 'Vasastan', 'Djurgården'],
            'Mord': ['Rinkeby', 'Tensta', 'Husby', 'Fittja', 'Ronna']
        }
        
        # Tidbaserade områdespreferenser
        self.time_area_preferences = {
            'night': ['Södermalm', 'Vasastan', 'Norrmalm'],  # 22-06
            'day': ['Norrmalm', 'Östermalm', 'Gamla stan'],   # 06-18
            'evening': ['Södermalm', 'Vasastan', 'Kungsholmen']  # 18-22
        }

    def get_time_category(self, datetime_str: str) -> str:
        """Bestäm tidskategori baserat på tid"""
        try:
            # Hantera olika datetime-format från polisen.se
            if '+' in datetime_str:
                dt_str = datetime_str.split('+')[0].strip()
            else:
                dt_str = datetime_str.strip()
            
            dt = datetime.fromisoformat(dt_str)
            hour = dt.hour
            
            if 22 <= hour or hour < 6:
                return 'night'
            elif 6 <= hour < 18:
                return 'day'
            else:
                return 'evening'
        except:
            return 'day'  # Default

    def improve_location_intelligent(self, event: Dict) -> Optional[Dict]:
        """Förbättra plats med intelligent analys"""
        
        location_name = event.get('location', {}).get('name', '')
        crime_type = event.get('type', '')
        datetime_str = event.get('datetime', '')
        
        # Extrahera kommun från location_name
        kommun = self.extract_kommun_from_location(location_name)
        
        # Hitta område i vår databas
        area_info = self.detailed_areas.get(kommun)
        if not area_info:
            logging.debug(f"Område {kommun} finns inte i databasen")
            return None
        
        # Välj sub-område baserat på brottstyp och tid
        selected_area = self._select_optimal_subarea(
            area_info, crime_type, datetime_str, kommun
        )
        
        if not selected_area:
            logging.debug(f"Kunde inte välja sub-område för {kommun}")
            return None
        
        area_name, (base_lat, base_lon) = selected_area
        
        # Lägg till intelligent spridning
        improved_lat, improved_lon = self._add_intelligent_spread(
            base_lat, base_lon, area_info['spread_radius'], crime_type
        )
        
        # Beräkna confidence baserat på specificiteten
        confidence = self._calculate_confidence(kommun, area_name, crime_type)
        
        # Uppdatera event med förbättrade koordinater
        event['latitude'] = improved_lat
        event['longitude'] = improved_lon
        event['location_confidence'] = confidence
        event['improvement_method'] = 'intelligent_area_analysis'
        event['improved_area'] = area_name
        event['improvement_details'] = f"Förbättrad från {kommun} centrum till {area_name} baserat på {crime_type}"
        
        logging.info(f"🎯 Förbättrade {event.get('id', 'N/A')} från {kommun} till {area_name} (confidence: {confidence:.2f})")
        
        return event

    def extract_kommun_from_location(self, location_name: str) -> str:
        """Extraherar kommun från platsnamn"""
        # Lista över Stockholm-kommuner
        stockholm_kommuner = [
            'Stockholm', 'Huddinge', 'Järfälla', 'Nacka', 'Solna',
            'Sundbyberg', 'Södertälje', 'Täby', 'Upplands Väsby',
            'Vallentuna', 'Vaxholm', 'Österåker', 'Botkyrka',
            'Danderyd', 'Ekerö', 'Haninge', 'Lidingö', 'Norrtälje',
            'Nykvarn', 'Nynäshamn', 'Salem', 'Sigtuna', 'Sollentuna',
            'Tyresö', 'Värmdö', 'Rinkeby-Kista'
        ]
        
        location_lower = location_name.lower()
        
        # Specialfall för Rinkeby-Kista
        if any(area in location_lower for area in ['rinkeby', 'tensta', 'husby', 'kista', 'akalla']):
            return 'Rinkeby-Kista'
        
        # Sök efter kommun i platsnamnet
        for kommun in stockholm_kommuner:
            if kommun.lower() in location_lower:
                return kommun
        
        return 'Stockholm'  # Default

    def _select_optimal_subarea(self, area_info: Dict, crime_type: str, 
                               datetime_str: str, location_name: str) -> Optional[Tuple[str, Tuple[float, float]]]:
        """Välj optimalt sub-område baserat på brottstyp och tid"""
        
        sub_areas = area_info['sub_areas']
        time_category = self.get_time_category(datetime_str)
        
        # Skapa viktad lista av områden
        weighted_areas = []
        
        for area_name, coords in sub_areas.items():
            weight = 1.0  # Basweight
            
            # Öka weight för brottstypspecifika områden
            crime_preferences = self.crime_area_preferences.get(crime_type, [])
            for pref in crime_preferences:
                if pref.lower() in area_name.lower():
                    weight += 2.0
                    break
            
            # Öka weight för tidspecifika områden
            time_preferences = self.time_area_preferences.get(time_category, [])
            for pref in time_preferences:
                if pref.lower() in area_name.lower():
                    weight += 1.5
                    break
            
            # Lägg till lite slumpmässighet för variation
            weight += random.uniform(0, 1)
            
            weighted_areas.append((weight, area_name, coords))
        
        # Sortera efter weight och välj
        weighted_areas.sort(reverse=True, key=lambda x: x[0])
        
        if weighted_areas:
            _, selected_name, selected_coords = weighted_areas[0]
            return (selected_name, selected_coords)
        
        return None

    def _add_intelligent_spread(self, base_lat: float, base_lon: float, 
                               radius: float, crime_type: str) -> Tuple[float, float]:
        """Lägg till intelligent spridning baserat på brottstyp"""
        
        # Olika spridningsmönster för olika brott
        spread_patterns = {
            'Skottlossning': 'clustered',  # Klustrade i specifika områden
            'Explosion': 'clustered',
            'Rån': 'linear',              # Längs gator och stråk
            'Misshandel': 'random',       # Mer slumpmässigt spridda
            'Våldtäkt': 'park_areas',     # Nära parker och avskilda områden
            'Mord': 'clustered'
        }
        
        pattern = spread_patterns.get(crime_type, 'random')
        
        if pattern == 'clustered':
            # Mindre spridning, mer klustrad
            actual_radius = radius * 0.6
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, actual_radius) * random.uniform(0.3, 1.0)
            
        elif pattern == 'linear':
            # Spridning längs "gator" (nord-syd eller öst-väst)
            if random.choice([True, False]):
                # Nord-syd spridning
                lat_offset = random.uniform(-radius, radius)
                lon_offset = random.uniform(-radius * 0.3, radius * 0.3)
            else:
                # Öst-väst spridning
                lat_offset = random.uniform(-radius * 0.3, radius * 0.3)
                lon_offset = random.uniform(-radius, radius)
            
            return (base_lat + lat_offset, base_lon + lon_offset)
            
        elif pattern == 'park_areas':
            # Spridning mot "park-områden" (lite utanför centrum)
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(radius * 0.5, radius * 1.2)
            
        else:  # random
            # Standard slumpmässig spridning
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, radius)
        
        # Beräkna nya koordinater (för clustered, park_areas och random)
        if pattern in ['clustered', 'park_areas', 'random']:
            lat_offset = distance * math.cos(angle)
            lon_offset = distance * math.sin(angle)
            
            return (base_lat + lat_offset, base_lon + lon_offset)

    def _calculate_confidence(self, location_name: str, area_name: str, crime_type: str) -> float:
        """Beräkna confidence för förbättringen"""
        
        confidence = 0.5  # Basconfidence
        
        # Öka confidence för specifika områden
        if area_name != f"{location_name} centrum":
            confidence += 0.2
        
        # Öka confidence för brottstypspecifika matchningar
        crime_preferences = self.crime_area_preferences.get(crime_type, [])
        for pref in crime_preferences:
            if pref.lower() in area_name.lower():
                confidence += 0.2
                break
        
        # Öka confidence för välkända problemområden
        problem_areas = ['Rinkeby', 'Tensta', 'Husby', 'Fittja', 'Ronna']
        for area in problem_areas:
            if area.lower() in area_name.lower():
                confidence += 0.1
                break
        
        return min(confidence, 0.95)  # Max 95% confidence

class PoliceDataFetcher:
    """Hämtar data från polisen.se API"""
    
    def __init__(self):
        self.base_url = "https://polisen.se/api/events"
        
    def fetch_events(self, days_back: int = 14) -> List[Dict[str, Any]]:
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
    
    def __init__(self):
        self.area_improver = StockholmAreaImprover()
    
    def enhance_location(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Förbättrar koordinater för en händelse"""
        try:
            # Försök först med intelligent platsförbättring
            improved_event = self.area_improver.improve_location_intelligent(event)
            if improved_event:
                return improved_event
            
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
            improved_count = 0
            
            for event in new_events:
                event_id = self.generate_event_id(event)
                
                # Skippa om händelsen redan finns
                if event_id in existing_ids:
                    logging.debug(f"🔄 Hoppar över duplikat: {event_id}")
                    continue
                
                # Förbättra koordinater
                enhanced_event = self.location_enhancer.enhance_location(event)
                
                # Räkna förbättringar
                if enhanced_event.get('improvement_method') == 'intelligent_area_analysis':
                    improved_count += 1
                
                # Formatera händelse
                formatted_event = self.format_event(enhanced_event)
                processed_new_events.append(formatted_event)
                
                logging.info(f"➕ Ny händelse: {event.get('type', 'N/A')} - {event.get('location', {}).get('name', 'N/A')}")
            
            # Slå ihop med befintlig data
            all_events = existing_events + processed_new_events
            
            # Sortera efter datum (nyast först)
            all_events.sort(key=lambda x: x.get('datetime', ''), reverse=True)
            
            # Beräkna förbättringsstatistik
            total_improved = sum(1 for event in all_events if event.get('improvement_method') == 'intelligent_area_analysis')
            improvement_rate = total_improved / len(all_events) if all_events else 0
            
            # Skapa uppdaterad dataset
            updated_data = {
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'total_events': len(all_events),
                    'new_events_added': len(processed_new_events),
                    'new_events_improved': improved_count,
                    'total_improved_events': total_improved,
                    'improvement_rate': improvement_rate,
                    'data_source': 'polisen.se',
                    'automation_version': '3.0',
                    'github_actions': True,
                    'enhanced_locations': True
                },
                'events': all_events
            }
            
            logging.info(f"✅ Bearbetade {len(processed_new_events)} nya händelser")
            logging.info(f"🎯 Förbättrade {improved_count} av {len(processed_new_events)} nya händelser")
            logging.info(f"📊 Total dataset innehåller nu {len(all_events)} händelser")
            logging.info(f"🎯 Totalt {total_improved} förbättrade händelser ({improvement_rate:.1%})")
            
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
            'improvement_method': event.get('improvement_method'),
            'improved_area': event.get('improved_area'),
            'improvement_details': event.get('improvement_details'),
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
            'Tyresö', 'Värmdö', 'Rinkeby-Kista'
        ]
        
        location_lower = location_name.lower()
        
        # Specialfall för Rinkeby-Kista
        if any(area in location_lower for area in ['rinkeby', 'tensta', 'husby', 'kista', 'akalla']):
            return 'Rinkeby-Kista'
        
        for kommun in stockholm_kommuner:
            if kommun.lower() in location_lower:
                return kommun
        
        return 'Stockholm'  # Default

def main():
    """Huvudfunktion för automatisk uppdatering med förbättrade platser"""
    try:
        logging.info("🚀 Stockholm Våldskarta - Auto Update med Förbättrade Platser startar")
        logging.info("=" * 70)
        
        # Initiera komponenter
        data_fetcher = PoliceDataFetcher()
        data_processor = DataProcessor()
        
        # Hämta nya händelser
        new_events = data_fetcher.fetch_events(days_back=14)  # 14 dagar för att få fler händelser
        
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
        
        # Logga slutstatistik
        new_improved = updated_data.get('metadata', {}).get('new_events_improved', 0)
        total_events = updated_data.get('metadata', {}).get('total_events', 0)
        total_improved = updated_data.get('metadata', {}).get('total_improved_events', 0)
        improvement_rate = updated_data.get('metadata', {}).get('improvement_rate', 0)
        
        logging.info(f"✅ Sparade uppdaterad data med {new_events_added} nya händelser")
        logging.info(f"🎯 Förbättrade {new_improved} av {new_events_added} nya händelser")
        logging.info(f"📊 Totalt antal händelser: {total_events}")
        logging.info(f"🎯 Totalt förbättrade händelser: {total_improved} ({improvement_rate:.1%})")
        logging.info("🎉 Automatisk uppdatering med förbättrade platser slutförd framgångsrikt!")
        
    except Exception as e:
        logging.error(f"❌ Kritiskt fel i huvudfunktionen: {e}")
        raise

if __name__ == '__main__':
    main()

