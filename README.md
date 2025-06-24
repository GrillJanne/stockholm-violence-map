# Stockholm Våldskarta - Automatisering

## 🚀 **KOMPLETT AUTOMATISERINGSSYSTEM**

Automatisk hämtning av nya våldshändelser från polisen.se och deployment till Netlify.

## 📦 **Två Automatiseringsalternativ**

### **1. 🖥️ Server/VPS Automatisering (Cron)**
- Kör på din egen server eller VPS
- Använder cron för schemaläggning
- Fullständig kontroll över processen

### **2. ☁️ GitHub Actions Automatisering (Rekommenderat)**
- Kör i molnet via GitHub
- Gratis för publika repositories
- Enklare setup och underhåll

## 🔧 **Setup Instruktioner**

### **GitHub Actions Setup (Rekommenderat)**

#### **Steg 1: Skapa GitHub Repository**
```bash
# Skapa nytt repository på GitHub
# Klona eller skapa lokalt
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/stockholm-violence-map.git
git push -u origin main
```

#### **Steg 2: Konfigurera Netlify Secrets**
1. Gå till GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Lägg till följande secrets:
   - `NETLIFY_SITE_ID`: Ditt Netlify Site ID (hittas i Netlify dashboard)
   - `NETLIFY_ACCESS_TOKEN`: Skapa i Netlify → User settings → Applications → Personal access tokens

#### **Steg 3: Aktivera Automatisering**
```bash
# Kör GitHub Actions setup
python3 github_actions_setup.py

# Pusha till GitHub
git add .
git commit -m "Add GitHub Actions automation"
git push
```

### **Server/VPS Setup**

#### **Steg 1: Installation**
```bash
# Kör setup script
chmod +x setup.sh
./setup.sh
```

#### **Steg 2: Konfiguration**
```bash
# Redigera config.json med dina uppgifter
nano config.json

# Lägg till:
# - Netlify Site ID
# - Netlify Access Token
```

#### **Steg 3: Aktivera Cron**
```bash
# Sätt upp automatisk schemaläggning
python3 setup_cron.py
```

## ⚙️ **Funktioner**

### **🔄 Automatisk Datauppdatering**
- ✅ Hämtar nya händelser från polisen.se var 6:e timme
- ✅ Filtrerar på våldshändelser (misshandel, rån, skottlossning, etc.)
- ✅ Förbättrar koordinater med geocoding
- ✅ Duplikathantering för att undvika dubbletter
- ✅ Backup av all data

### **🚀 Automatisk Deployment**
- ✅ Deployer automatiskt till Netlify vid nya händelser
- ✅ Uppdaterar både data och HTML
- ✅ Väntar på deployment-bekräftelse
- ✅ Felhantering och retry-logik

### **📊 Kvalitetskontroll**
- ✅ Validerar datakvalitet innan deployment
- ✅ Kontrollerar koordinatnoggrannhet
- ✅ Loggar alla ändringar och fel
- ✅ Metadata om varje uppdatering

### **🔍 Monitoring & Logging**
- ✅ Detaljerade loggar för alla operationer
- ✅ E-postnotifikationer vid fel (konfigurerbart)
- ✅ Statistik över nya händelser
- ✅ Backup-system för datasäkerhet

## 📋 **Konfiguration**

### **config.json Exempel**
```json
{
  "data_file": "stockholm_violence_data.json",
  "html_file": "index.html",
  "backup_dir": "backups",
  "days_back": 7,
  "netlify": {
    "site_id": "YOUR_NETLIFY_SITE_ID",
    "access_token": "YOUR_NETLIFY_ACCESS_TOKEN"
  },
  "automation": {
    "enabled": true,
    "schedule": "0 */6 * * *",
    "max_events_per_run": 100
  }
}
```

### **Schemaläggning**
- **Standard:** Var 6:e timme (`0 */6 * * *`)
- **Anpassningsbar:** Ändra `schedule` i config.json
- **Manuell körning:** Alltid möjlig för testning

## 🎯 **Fördelar med Automatisering**

### **📈 Alltid Uppdaterad Data**
- Nya våldshändelser visas inom 6 timmar
- Ingen manuell intervention krävs
- Konsekvent datakvalitet

### **⚡ Snabb Deployment**
- Automatisk publicering till Netlify
- Inga manuella deployment-steg
- Backup vid fel

### **🔒 Säker & Pålitlig**
- Felhantering och retry-logik
- Backup av all data
- Detaljerad loggning

### **💰 Kostnadseffektiv**
- GitHub Actions gratis för publika repos
- Minimal serverresurs-användning
- Automatisk skalning

## 📊 **Förväntade Resultat**

### **Datauppdateringar**
- **Frekvens:** Var 6:e timme
- **Nya händelser:** 5-15 per dag i genomsnitt
- **Datakvalitet:** 75%+ koordinatnoggrannhet
- **Uppdateringstid:** 2-5 minuter per körning

### **Webbplats-prestanda**
- **Uppdateringsfrekvens:** Automatisk vid nya data
- **Deployment-tid:** 1-3 minuter
- **Tillgänglighet:** 99.9%+ (Netlify SLA)
- **SEO-påverkan:** Positiv (färsk data)

## 🛠️ **Underhåll & Monitoring**

### **Daglig Monitoring**
- Kontrollera loggar för fel
- Verifiera att nya händelser läggs till
- Övervaka Netlify deployment-status

### **Veckovis Underhåll**
- Granska datakvalitet
- Kontrollera backup-filer
- Uppdatera dependencies vid behov

### **Månadsvis Optimering**
- Analysera automatiseringsstatistik
- Justera schemaläggning vid behov
- Optimera koordinatförbättringar

## 🚨 **Felsökning**

### **Vanliga Problem**
1. **Netlify deployment misslyckas**
   - Kontrollera Site ID och Access Token
   - Verifiera att filer är korrekta

2. **Inga nya händelser hämtas**
   - Kontrollera polisen.se API-status
   - Verifiera nätverksanslutning

3. **Cron job körs inte**
   - Kontrollera crontab: `crontab -l`
   - Verifiera sökvägar i cron-kommando

### **Debug-kommandon**
```bash
# Testa manuell körning
python3 auto_update.py

# Kontrollera cron status
python3 setup_cron.py status

# Visa loggar
tail -f logs/automation.log
```

## 🎉 **Slutresultat**

**En helt automatiserad Stockholm Våldskarta som:**
- 🔄 **Uppdateras automatiskt** var 6:e timme
- 📊 **Håller data färsk** från polisen.se
- 🚀 **Deployer automatiskt** till Netlify
- 📈 **Förbättrar SEO** med färsk data
- 🔒 **Säkrar data** med backup-system
- 📝 **Loggar allt** för transparens

**Sätt upp en gång - fungerar för alltid!** ✨

