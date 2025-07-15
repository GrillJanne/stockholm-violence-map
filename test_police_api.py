#!/usr/bin/env python3
"""
Testar polisen.se API direkt för att se vad som händer
"""

import requests
import json
from datetime import datetime, timedelta

def test_api_basic():
    """Test 1: Grundläggande API-anrop"""
    print("🧪 TEST 1: Grundläggande API-anrop")
    print("=" * 50)
    
    url = "https://polisen.se/api/events"
    
    try:
        response = requests.get(url, timeout=30 )
        print(f"📡 Status: {response.status_code}")
        print(f"📏 Response längd: {len(response.text)} tecken")
        
        if response.status_code == 200:
            events = response.json()
            print(f"📥 Antal händelser: {len(events)}")
            
            if events:
                print(f"\n📋 FÖRSTA HÄNDELSEN:")
                first_event = events[0]
                print(f"   Typ: {first_event.get('type', 'N/A')}")
                print(f"   Datum: {first_event.get('datetime', 'N/A')}")
                print(f"   Plats: {first_event.get('location', {}).get('name', 'N/A')}")
        else:
            print(f"❌ Fel: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_api_with_stockholm():
    """Test 2: Med Stockholm som locationname"""
    print("\n🧪 TEST 2: Med Stockholm som locationname")
    print("=" * 50)
    
    url = "https://polisen.se/api/events"
    params = {'locationname': 'Stockholm'}
    
    try:
        response = requests.get(url, params=params, timeout=30 )
        print(f"📡 Status: {response.status_code}")
        print(f"🔗 URL: {response.url}")
        
        if response.status_code == 200:
            events = response.json()
            print(f"📥 Antal händelser: {len(events)}")
            
            if events:
                print(f"\n📋 FÖRSTA 3 HÄNDELSER:")
                for i, event in enumerate(events[:3]):
                    print(f"   {i+1}. {event.get('type', 'N/A')} - {event.get('location', {}).get('name', 'N/A')}")
        else:
            print(f"❌ Fel: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_api_with_dates():
    """Test 3: Med datum-parametrar"""
    print("\n🧪 TEST 3: Med datum-parametrar")
    print("=" * 50)
    
    url = "https://polisen.se/api/events"
    
    # Testa olika datum-format
    end_date = datetime.now( )
    start_date = end_date - timedelta(days=7)
    
    # Format 1: YYYY-MM-DD,YYYY-MM-DD
    params1 = {
        'DateTime': f"{start_date.strftime('%Y-%m-%d')},{end_date.strftime('%Y-%m-%d')}",
        'locationname': 'Stockholm'
    }
    
    print(f"📅 Datum format 1: {params1['DateTime']}")
    
    try:
        response = requests.get(url, params=params1, timeout=30)
        print(f"📡 Status: {response.status_code}")
        print(f"🔗 URL: {response.url}")
        
        if response.status_code == 200:
            events = response.json()
            print(f"📥 Antal händelser: {len(events)}")
        else:
            print(f"❌ Fel: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_api_without_dates():
    """Test 4: Utan datum (senaste händelser)"""
    print("\n🧪 TEST 4: Utan datum-parametrar")
    print("=" * 50)
    
    url = "https://polisen.se/api/events"
    params = {'locationname': 'Stockholm'}
    
    try:
        response = requests.get(url, params=params, timeout=30 )
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            events = response.json()
            print(f"📥 Antal händelser: {len(events)}")
            
            if events:
                print(f"\n📋 SENASTE 5 HÄNDELSER:")
                for i, event in enumerate(events[:5]):
                    print(f"   {i+1}. {event.get('datetime', 'N/A')} - {event.get('type', 'N/A')}")
                    print(f"      Plats: {event.get('location', {}).get('name', 'N/A')}")
        else:
            print(f"❌ Fel: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_different_locations():
    """Test 5: Olika location-parametrar"""
    print("\n🧪 TEST 5: Olika location-parametrar")
    print("=" * 50)
    
    url = "https://polisen.se/api/events"
    
    locations = ['Stockholm', 'Stockholms län', 'Stockholm stad']
    
    for location in locations:
        print(f"\n🔍 Testar location: '{location}'" )
        params = {'locationname': location}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                events = response.json()
                print(f"   📥 Antal händelser: {len(events)}")
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    test_api_basic()
    test_api_with_stockholm()
    test_api_with_dates()
    test_api_without_dates()
    test_different_locations()
