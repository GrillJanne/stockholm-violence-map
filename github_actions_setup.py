#!/usr/bin/env python3
"""
GitHub Actions Workflow Generator för Stockholm Våldskarta
Skapar automatisering via GitHub Actions istället för cron
"""

import json
import os
from pathlib import Path

def create_github_workflow():
    """Skapar GitHub Actions workflow"""
    
    workflow_content = """name: Stockholm Våldskarta Auto Update

on:
  schedule:
    # Kör var 6:e timme
    - cron: '0 */6 * * *'
  workflow_dispatch: # Tillåt manuell körning

jobs:
  update-data:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests
        
    - name: Run data update
      env:
        NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
        NETLIFY_ACCESS_TOKEN: ${{ secrets.NETLIFY_ACCESS_TOKEN }}
      run: |
        python auto_update.py
        
    - name: Commit updated data
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add stockholm_violence_data.json
        git diff --staged --quiet || git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M:%S')"
        
    - name: Push changes
      uses: ad-m/github-push-action@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        branch: main
"""

    # Skapa .github/workflows mapp
    workflow_dir = Path('.github/workflows')
    workflow_dir.mkdir(parents=True, exist_ok=True)
    
    # Skriv workflow-fil
    workflow_file = workflow_dir / 'auto-update.yml'
    with open(workflow_file, 'w') as f:
        f.write(workflow_content)
    
    print(f"✅ GitHub Actions workflow skapad: {workflow_file}")
    return workflow_file

def create_github_auto_update():
    """Skapar GitHub Actions-kompatibel auto_update.py"""
    
    github_auto_update = """#!/usr/bin/env python3
\"\"\"
Stockholm Våldskarta - GitHub Actions Auto Update
Förenklad version för GitHub Actions
\"\"\"

import requests
import json
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any

class PoliceDataFetcher:
    def __init__(self):
        self.base_url = "https://polisen.se/api/events"
        self.stockholm_regions = [
            "Stockholm", "Stockholms län", "Huddinge", "Järfälla", 
            "Nacka", "Solna", "Sundbyberg", "Södertälje", "Täby"
        ]
        
    def fetch_events(self, days_back: int = 7) -> List[Dict[str, Any]]:
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            params = {
                'DateTime': f"{start_date.strftime('%Y-%m-%d')},{end_date.strftime('%Y-%m-%d')}",
                'locationname': ','.join(self.stockholm_regions)
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            events = response.json()
            return self.filter_violence_events(events)
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
    
    def filter_violence_events(self, events: List[Dict]) -> List[Dict]:
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

def deploy_to_netlify(site_id: str, access_token: str, data_content: str, html_content: str) -> bool:
    \"\"\"Deployer till Netlify via API\"\"\"
    try:
        files = {
            'stockholm_violence_data.json': data_content,
            'index.html': html_content
        }
        
        deployment_data = {'files': files}
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"https://api.netlify.com/api/v1/sites/{site_id}/deploys",
            headers=headers,
            json=deployment_data,
            timeout=60
        )
        
        if response.status_code == 200:
            print("✅ Netlify deployment successful!")
            return True
        else:
            print(f"❌ Netlify deployment failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Netlify deployment error: {e}")
        return False

def main():
    print("🚀 Stockholm Våldskarta - Auto Update (GitHub Actions)")
    
    # Hämta nya händelser
    fetcher = PoliceDataFetcher()
    new_events = fetcher.fetch_events(7)
    
    if not new_events:
        print("ℹ️  No new events found")
        return
    
    print(f"📥 Found {len(new_events)} new events")
    
    # Ladda befintlig data
    try:
        with open('stockholm_violence_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except:
        existing_data = {'events': []}
    
    # Lägg till nya händelser (förenklad version)
    existing_events = existing_data.get('events', [])
    
    # Enkel duplikathantering baserat på datum och typ
    existing_signatures = set()
    for event in existing_events:
        signature = f"{event.get('datetime', '')}_{event.get('type', '')}"
        existing_signatures.add(signature)
    
    new_events_added = 0
    for event in new_events:
        signature = f"{event.get('datetime', '')}_{event.get('type', '')}"
        if signature not in existing_signatures:
            # Förenklad formatering
            formatted_event = {
                'datetime': event.get('datetime', ''),
                'type': event.get('type', ''),
                'summary': event.get('summary', ''),
                'location_name': event.get('location', {}).get('name', ''),
                'latitude': 59.3293,  # Stockholm centrum som fallback
                'longitude': 18.0686,
                'location_confidence': 0.5,
                'correction_method': 'github_automation',
                'url': event.get('url', ''),
                'added_by_automation': True,
                'added_timestamp': datetime.now().isoformat()
            }
            existing_events.append(formatted_event)
            new_events_added += 1
    
    if new_events_added == 0:
        print("ℹ️  No new unique events to add")
        return
    
    # Uppdatera metadata
    updated_data = {
        'metadata': {
            'last_updated': datetime.now().isoformat(),
            'total_events': len(existing_events),
            'new_events_added': new_events_added,
            'data_source': 'polisen.se',
            'automation_version': 'github-actions-1.0'
        },
        'events': existing_events
    }
    
    # Spara uppdaterad data
    with open('stockholm_violence_data.json', 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Added {new_events_added} new events")
    print(f"📊 Total events: {len(existing_events)}")
    
    # Deployer till Netlify om konfigurerat
    site_id = os.environ.get('NETLIFY_SITE_ID')
    access_token = os.environ.get('NETLIFY_ACCESS_TOKEN')
    
    if site_id and access_token:
        print("🚀 Deploying to Netlify...")
        
        # Läs HTML-fil
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
        except:
            print("❌ Could not read index.html")
            return
        
        # Läs uppdaterad data
        with open('stockholm_violence_data.json', 'r', encoding='utf-8') as f:
            data_content = f.read()
        
        deploy_to_netlify(site_id, access_token, data_content, html_content)
    else:
        print("ℹ️  Netlify credentials not configured, skipping deployment")

if __name__ == "__main__":
    main()
"""

    with open('auto_update.py', 'w') as f:
        f.write(github_auto_update)
    
    print("✅ GitHub Actions auto_update.py skapad")

def create_readme():
    """Skapar README för GitHub repository"""
    
    readme_content = """# Stockholm Våldskarta - Automatisering

Automatisk uppdatering av Stockholm Våldskarta med data från polisen.se.

## 🚀 GitHub Actions Setup

### 1. Repository Setup
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/stockholm-violence-map.git
git push -u origin main
```

### 2. Konfigurera Secrets
Gå till GitHub repository → Settings → Secrets and variables → Actions

Lägg till följande secrets:
- `NETLIFY_SITE_ID`: Ditt Netlify Site ID
- `NETLIFY_ACCESS_TOKEN`: Ditt Netlify Access Token

### 3. Aktivera Actions
- GitHub Actions aktiveras automatiskt när workflow-filen finns
- Första körningen sker enligt schema eller manuellt via Actions-fliken

## 📋 Funktioner

- ✅ Automatisk hämtning av nya våldshändelser från polisen.se
- ✅ Duplikathantering för att undvika dubbletter
- ✅ Automatisk deployment till Netlify
- ✅ Git-versionshantering av uppdateringar
- ✅ Körning var 6:e timme

## 🔧 Manuell körning

```bash
python auto_update.py
```

## 📊 Monitoring

- Kontrollera Actions-fliken i GitHub för körningshistorik
- Loggar visas i varje workflow-körning
- Automatiska commits visar när data uppdaterats

## 🛠️ Anpassning

Redigera `.github/workflows/auto-update.yml` för att:
- Ändra schema (cron expression)
- Lägga till fler steg
- Konfigurera notifikationer

## 📈 Status

Senaste uppdatering visas i commit-historiken och på webbplatsen.
"""

    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ README.md skapad")

def main():
    print("🚀 GitHub Actions Setup för Stockholm Våldskarta")
    print("===============================================")
    
    # Skapa alla nödvändiga filer
    create_github_workflow()
    create_github_auto_update()
    create_readme()
    
    print("\n✅ GitHub Actions setup slutfört!")
    print("\n📋 Nästa steg:")
    print("1. Skapa GitHub repository")
    print("2. Lägg till Netlify secrets i GitHub")
    print("3. Pusha filerna till GitHub")
    print("4. Automatiseringen startar enligt schema")
    print("\n🔗 Mer info finns i README.md")

if __name__ == "__main__":
    main()

