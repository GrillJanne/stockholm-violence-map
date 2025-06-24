#!/usr/bin/env python3
"""
Cron Setup Script för Stockholm Våldskarta Automatisering
Sätter upp automatisk schemaläggning av datauppdateringar
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def setup_cron():
    """Sätter upp cron job för automatisk uppdatering"""
    try:
        # Ladda konfiguration
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        schedule = config.get('automation', {}).get('schedule', '0 */6 * * *')
        
        # Få absolut sökväg till script
        script_dir = Path(__file__).parent.absolute()
        script_path = script_dir / 'auto_update.py'
        venv_python = script_dir / 'venv' / 'bin' / 'python'
        log_file = script_dir / 'logs' / 'automation.log'
        
        # Skapa logs-mapp om den inte finns
        (script_dir / 'logs').mkdir(exist_ok=True)
        
        # Cron kommando
        cron_command = f"cd {script_dir} && {venv_python} {script_path} >> {log_file} 2>&1"
        
        # Lägg till cron job
        cron_entry = f"{schedule} {cron_command}"
        
        print("🕐 Sätter upp automatisk schemaläggning...")
        print(f"📅 Schema: {schedule} (var 6:e timme)")
        print(f"📂 Script: {script_path}")
        print(f"📝 Loggar: {log_file}")
        
        # Kontrollera om cron job redan finns
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        existing_crontab = result.stdout if result.returncode == 0 else ""
        
        if 'auto_update.py' in existing_crontab:
            print("⚠️  Cron job finns redan. Vill du uppdatera det? (y/n): ", end="")
            if input().lower() != 'y':
                print("❌ Avbryter setup av cron job")
                return False
            
            # Ta bort befintligt job
            lines = existing_crontab.strip().split('\n')
            filtered_lines = [line for line in lines if 'auto_update.py' not in line]
            new_crontab = '\n'.join(filtered_lines)
        else:
            new_crontab = existing_crontab.strip()
        
        # Lägg till nytt job
        if new_crontab:
            new_crontab += '\n'
        new_crontab += cron_entry + '\n'
        
        # Installera ny crontab
        process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
        process.communicate(input=new_crontab)
        
        if process.returncode == 0:
            print("✅ Cron job installerat framgångsrikt!")
            print(f"🔄 Automatisk uppdatering körs enligt schema: {schedule}")
            return True
        else:
            print("❌ Fel vid installation av cron job")
            return False
            
    except Exception as e:
        print(f"❌ Fel vid setup av cron: {e}")
        return False

def show_cron_status():
    """Visar status för befintliga cron jobs"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        
        if result.returncode == 0:
            crontab_content = result.stdout
            
            if 'auto_update.py' in crontab_content:
                print("✅ Automatisering är aktiv!")
                print("\n📋 Befintliga cron jobs:")
                for line in crontab_content.strip().split('\n'):
                    if 'auto_update.py' in line:
                        print(f"   {line}")
            else:
                print("❌ Ingen automatisering är konfigurerad")
        else:
            print("❌ Kunde inte läsa crontab")
            
    except Exception as e:
        print(f"❌ Fel vid kontroll av cron status: {e}")

def remove_cron():
    """Tar bort automatisering"""
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        
        if result.returncode == 0:
            existing_crontab = result.stdout
            
            if 'auto_update.py' not in existing_crontab:
                print("❌ Ingen automatisering hittades att ta bort")
                return False
            
            # Ta bort automation jobs
            lines = existing_crontab.strip().split('\n')
            filtered_lines = [line for line in lines if 'auto_update.py' not in line]
            new_crontab = '\n'.join(filtered_lines) + '\n' if filtered_lines else ''
            
            # Installera uppdaterad crontab
            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=new_crontab)
            
            if process.returncode == 0:
                print("✅ Automatisering borttagen!")
                return True
            else:
                print("❌ Fel vid borttagning av automatisering")
                return False
        else:
            print("❌ Kunde inte läsa crontab")
            return False
            
    except Exception as e:
        print(f"❌ Fel vid borttagning av cron: {e}")
        return False

def main():
    """Huvudfunktion"""
    print("🕐 Stockholm Våldskarta - Cron Setup")
    print("====================================")
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'install':
            setup_cron()
        elif command == 'status':
            show_cron_status()
        elif command == 'remove':
            remove_cron()
        else:
            print(f"❌ Okänt kommando: {command}")
            print("Tillgängliga kommandon: install, status, remove")
    else:
        print("Välj en åtgärd:")
        print("1. Installera automatisering")
        print("2. Visa status")
        print("3. Ta bort automatisering")
        print("4. Avsluta")
        
        choice = input("\nVälj (1-4): ").strip()
        
        if choice == '1':
            setup_cron()
        elif choice == '2':
            show_cron_status()
        elif choice == '3':
            remove_cron()
        elif choice == '4':
            print("👋 Avslutar")
        else:
            print("❌ Ogiltigt val")

if __name__ == "__main__":
    main()

