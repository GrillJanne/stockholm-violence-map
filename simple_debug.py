#!/usr/bin/env python3
"""
Enkel debug för att se vad som händer
"""

import requests
import json
from datetime import datetime, timedelta

def check_police_api():
    """Kontrollera vad vi får från polisen.se"""
    print("🔍 TESTAR POLISEN.SE API")
    print("=" * 40)
    
    try:
        # Samma API-anrop som din auto_update.py borde göra
        base_url = "https://polisen.se/api/events"
        end_date = datetime.now( )
        start_date = end_date - timedelta(days=7)
        
        params = {
            'DateTime': f"{start_date.strftime('%Y-%m-%d')},{end_date.strftime('%Y-%m-%d')}",
            'locationname': 'Stockholm'
        }
        
        print(f"📅 Söker händelser från: {start_date.strftime('%Y-%m-%d')} till {end_date.strftime('%Y-%m-%d')}")
        
        response = requests.get(base_url, params=params, timeout=30)
        print(f"📡 API Response: {response.status_code}")
        
        if response.status_code == 200:
            events = response.json()
            print(f"📥 Totalt antal händelser: {len(events)}")
            
            # Visa några exempel
            print("\n📋 FÖRSTA 5 HÄNDELSER:")
            for i, event in enumerate(events[:5]):
                print(f"  {i+1}. {event.get('type', 'N/A')} - {event.get('datetime', 'N/A')}")
                print(f"     Plats: {event.get('location', {}).get('name', 'N/A')}")
                print(f"     Sammanfattning: {event.get('summary', 'N/A')[:80]}...")
                print()
            
            # Filtrera våldshändelser
            violence_keywords = ['misshandel', 'rån', 'våldtäkt', 'mord', 'skottlossning', 'explosion']
            violence_count = 0
            
            print("🚨 VÅLDSHÄNDELSER:")
            for event in events:
                event_type = event.get('type', '').lower()
                summary = event.get('summary', '').lower()
                
                if any(keyword in event_type or keyword in summary for keyword in violence_keywords):
                    violence_count += 1
                    if violence_count <= 5:  # Visa bara första 5
                        print(f"  🚨 {event.get('type', 'N/A')} - {event.get('datetime', 'N/A')}")
                        print(f"     Plats: {event.get('location', {}).get('name', 'N/A')}")
            
            print(f"\n📊 TOTALT VÅLDSHÄNDELSER: {violence_count}")
            
        else:
            print(f"❌ API-fel: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Fel: {e}")

def check_existing_data():
    """Kontrollera befintlig JSON-fil"""
    print("\n🔍 KONTROLLERAR BEFINTLIG JSON")
    print("=" * 40)
    
    try:
        with open('stockholm_violence_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        events = data.get('events', [])
        metadata = data.get('metadata', {})
        
        print(f"📊 Antal händelser i fil: {len(events)}")
        print(f"📅 Senast uppdaterad: {metadata.get('last_updated', 'N/A')}")
        print(f"➕ Nya händelser senast: {metadata.get('new_events_added', 'N/A')}")
        
        # Visa senaste händelser
        if events:
            print("\n📋 SENASTE 3 HÄNDELSER I FILEN:")
            # Sortera efter datum
            try:
                sorted_events = sorted(events, key=lambda x: x.get('datetime', ''), reverse=True)
                for i, event in enumerate(sorted_events[:3]):
                    print(f"  {i+1}. {event.get('type', 'N/A')} - {event.get('datetime', 'N/A')}")
                    print(f"     Plats: {event.get('location_name', 'N/A')}")
                    print(f"     Automation: {event.get('added_by_automation', 'N/A')}")
            except:
                print("  (Kunde inte sortera händelser)")
        
    except Exception as e:
        print(f"❌ Fel vid läsning av JSON: {e}")

if __name__ == "__main__":
    check_police_api()
    check_existing_data()
