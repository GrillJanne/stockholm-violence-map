# GitHub Automatisering för Nybörjare - Stockholm Våldskarta

## 🎯 **Vad är GitHub och varför använda det?**

**GitHub** är en molntjänst för kodlagring och samarbete. För din våldskarta betyder det:
- ✅ **Gratis hosting** av din kod
- ✅ **Automatisk körning** av script i molnet
- ✅ **Versionshantering** - alla ändringar sparas
- ✅ **Backup** - din kod är säker i molnet
- ✅ **GitHub Actions** - gratis automatisering

## 📋 **Vad du behöver:**

### **Innan du börjar:**
1. **GitHub-konto** (gratis på github.com)
2. **Git installerat** på din dator
3. **Netlify Site ID och Access Token** (från din befintliga sida)
4. **Automatiseringsfilerna** (från ZIP-paketet)

---

## 🚀 **STEG-FÖR-STEG GUIDE**

### **STEG 1: Skapa GitHub-konto (om du inte har ett)**

1. **Gå till:** https://github.com
2. **Klicka:** "Sign up"
3. **Fyll i:**
   - Username (t.ex. "dittnamn-stockholm-karta")
   - Email
   - Lösenord
4. **Verifiera** email
5. **Välj:** Free plan (gratis)

### **STEG 2: Installera Git på din dator**

#### **Windows:**
1. **Ladda ner:** https://git-scm.com/download/win
2. **Installera** med standardinställningar
3. **Öppna:** "Git Bash" (sökfunktionen i Windows)

#### **Mac:**
1. **Öppna Terminal** (Cmd+Space, skriv "Terminal")
2. **Kör:** `git --version`
3. **Om Git saknas:** Följ instruktionerna för att installera

#### **Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install git

# CentOS/RHEL
sudo yum install git
```

### **STEG 3: Konfigurera Git (första gången)**

**Öppna terminal/Git Bash och kör:**
```bash
# Sätt ditt namn (visas i commits)
git config --global user.name "Ditt Namn"

# Sätt din email (samma som GitHub)
git config --global user.email "din-email@example.com"

# Kontrollera att det fungerade
git config --list
```

### **STEG 4: Skapa nytt GitHub Repository**

1. **Logga in** på GitHub
2. **Klicka** den gröna "New" knappen (eller gå till https://github.com/new)
3. **Fyll i:**
   - **Repository name:** `stockholm-violence-map`
   - **Description:** `Automatiserad våldskarta för Stockholm med data från polisen.se`
   - **Välj:** Public (för gratis GitHub Actions)
   - **KRYSSA I:** "Add a README file"
4. **Klicka:** "Create repository"

### **STEG 5: Klona repository till din dator**

1. **På GitHub-sidan:** Klicka den gröna "Code" knappen
2. **Kopiera URL:en** (börjar med https://github.com/...)
3. **I terminal/Git Bash:**

```bash
# Gå till en mapp där du vill ha projektet (t.ex. Desktop)
cd Desktop

# Klona repository (ersätt URL med din egen)
git clone https://github.com/DITT-USERNAME/stockholm-violence-map.git

# Gå in i mappen
cd stockholm-violence-map

# Kontrollera att du är i rätt mapp
ls -la
```

### **STEG 6: Lägg till automatiseringsfilerna**

1. **Extrahera** `stockholm-violence-AUTOMATION-COMPLETE.zip`
2. **Kopiera alla filer** från `stockholm-violence-automation/` mappen
3. **Klistra in** i din `stockholm-violence-map/` mapp

**Eller via terminal:**
```bash
# Om ZIP-filen är på Desktop
cd ~/Desktop/stockholm-violence-map

# Kopiera filer från extraherad mapp
cp -r ../stockholm-violence-automation/* .

# Kontrollera att filerna finns
ls -la
```

**Du ska nu ha dessa filer:**
- `auto_update.py`
- `config.json`
- `index.html`
- `stockholm_violence_data.json`
- `README.md`
- `setup.sh`
- `setup_cron.py`
- `github_actions_setup.py`

### **STEG 7: Skapa GitHub Actions Workflow**

**Kör setup-scriptet:**
```bash
# Gör scriptet körbart
chmod +x github_actions_setup.py

# Kör GitHub Actions setup
python3 github_actions_setup.py
```

**Detta skapar:**
- `.github/workflows/auto-update.yml` - Automatiseringsinstruktioner
- Uppdaterad `auto_update.py` - Förenklad för GitHub Actions
- Uppdaterad `README.md` - Med GitHub-instruktioner

### **STEG 8: Pusha filerna till GitHub**

```bash
# Lägg till alla filer
git add .

# Skapa en commit (sparningspunkt)
git commit -m "Lägg till automatisering för våldskarta"

# Skicka till GitHub
git push origin main
```

**Om du får fel här:**
```bash
# Första gången kan du behöva sätta upstream
git push -u origin main
```

### **STEG 9: Konfigurera Netlify Secrets**

#### **9.1: Hitta ditt Netlify Site ID**
1. **Logga in** på Netlify (netlify.com)
2. **Klicka** på din webbplats (08-violence.netlify.app)
3. **Gå till:** Site settings → General → Site details
4. **Kopiera:** Site ID (t.ex. `abc123def-456g-789h-012i-345jklmnopqr`)

#### **9.2: Skapa Netlify Access Token**
1. **I Netlify:** Klicka din profil (övre högra hörnet)
2. **Välj:** User settings
3. **Gå till:** Applications
4. **Klicka:** "New access token"
5. **Beskrivning:** "Stockholm Våldskarta Automation"
6. **Klicka:** "Generate token"
7. **KOPIERA TOKEN OMEDELBART** (visas bara en gång!)

#### **9.3: Lägg till Secrets i GitHub**
1. **Gå till** ditt GitHub repository
2. **Klicka:** Settings (högst upp på repository-sidan)
3. **I vänster meny:** Secrets and variables → Actions
4. **Klicka:** "New repository secret"

**Lägg till första secret:**
- **Name:** `NETLIFY_SITE_ID`
- **Secret:** Klistra in ditt Site ID
- **Klicka:** "Add secret"

**Lägg till andra secret:**
- **Name:** `NETLIFY_ACCESS_TOKEN`
- **Secret:** Klistra in din Access Token
- **Klicka:** "Add secret"

### **STEG 10: Aktivera och testa automatiseringen**

#### **10.1: Kontrollera att GitHub Actions är aktivt**
1. **I ditt repository:** Klicka "Actions" (högst upp)
2. **Du ska se:** "Stockholm Våldskarta Auto Update" workflow
3. **Om det finns en gul varning:** Klicka "I understand my workflows, go ahead and enable them"

#### **10.2: Testa manuell körning**
1. **Klicka** på "Stockholm Våldskarta Auto Update"
2. **Klicka** "Run workflow" (höger sida)
3. **Klicka** den gröna "Run workflow" knappen
4. **Vänta** 2-5 minuter
5. **Kontrollera** att det blir grönt (✅) - betyder framgång

#### **10.3: Kontrollera resultatet**
1. **Om testet lyckades:** Gå till din Netlify-sida
2. **Kontrollera** att data uppdaterats
3. **I GitHub:** Kolla om det skapats en ny commit med "Auto-update: [datum]"

---

## 🔧 **Hur automatiseringen fungerar**

### **Schema:**
- **Automatisk körning:** Var 6:e timme (00:00, 06:00, 12:00, 18:00 UTC)
- **Manuell körning:** När som helst via GitHub Actions

### **Vad som händer vid varje körning:**
1. **GitHub startar** en virtuell dator i molnet
2. **Laddar ner** din kod
3. **Installerar** Python och dependencies
4. **Kör** `auto_update.py` som:
   - Hämtar nya händelser från polisen.se
   - Filtrerar på våldsdåd
   - Uppdaterar din JSON-fil
   - Deployer till Netlify
5. **Sparar** uppdaterad data tillbaka till GitHub
6. **Stänger av** den virtuella datorn

### **Kostnad:**
- **GitHub Actions:** Gratis för publika repositories (2000 minuter/månad)
- **Din automatisering:** Använder ~5 minuter per körning
- **Total kostnad:** 0 kr/månad

---

## 📊 **Monitoring och underhåll**

### **Kontrollera att automatiseringen fungerar:**

#### **Daglig kontroll (30 sekunder):**
1. **Gå till:** GitHub repository → Actions
2. **Kontrollera:** Senaste körningen är grön (✅)
3. **Om röd (❌):** Klicka för att se felmeddelande

#### **Veckovis kontroll (2 minuter):**
1. **Kontrollera** din Netlify-sida för nya händelser
2. **Jämför** med polisen.se för att se att data stämmer
3. **Kolla** GitHub commits för automatiska uppdateringar

### **Vanliga problem och lösningar:**

#### **Problem 1: Röd (❌) i GitHub Actions**
**Lösning:**
1. Klicka på den röda körningen
2. Läs felmeddelandet
3. Vanligaste fel:
   - **Netlify credentials:** Kontrollera Site ID och Access Token
   - **API timeout:** Polisen.se API är temporärt otillgängligt (försök igen senare)

#### **Problem 2: Inga nya händelser läggs till**
**Lösning:**
1. Kontrollera att polisen.se API fungerar
2. Kolla om det faktiskt finns nya händelser
3. Verifiera att filtreringen fungerar korrekt

#### **Problem 3: Deployment till Netlify misslyckas**
**Lösning:**
1. Kontrollera Netlify Access Token (kan ha gått ut)
2. Verifiera Site ID
3. Kontrollera att Netlify-kontot är aktivt

---

## 🎯 **Fördelar med GitHub Actions**

### **Jämfört med egen server:**
- ✅ **Ingen server att underhålla**
- ✅ **Automatiska uppdateringar** av miljön
- ✅ **Gratis hosting** och körning
- ✅ **Inbyggd monitoring** och loggar
- ✅ **Skalbar** - hanterar hög belastning automatiskt

### **Säkerhet:**
- ✅ **Secrets är krypterade** och säkra
- ✅ **Isolerad miljö** för varje körning
- ✅ **Audit logs** - alla ändringar spåras
- ✅ **Backup** - all kod är säkrad i molnet

---

## 📚 **Användbara GitHub-kommandon**

### **Grundläggande Git-kommandon:**
```bash
# Se status på filer
git status

# Lägg till alla ändringar
git add .

# Skapa commit
git commit -m "Beskrivning av ändring"

# Skicka till GitHub
git push

# Hämta senaste ändringar från GitHub
git pull

# Se commit-historik
git log --oneline
```

### **Om du gör ändringar lokalt:**
```bash
# Efter att du ändrat filer
git add .
git commit -m "Uppdaterade konfiguration"
git push
```

---

## 🎉 **Slutresultat**

**Efter denna setup har du:**
- ✅ **Automatiserad våldskarta** som uppdateras var 6:e timme
- ✅ **Gratis hosting** och körning via GitHub
- ✅ **Automatisk deployment** till Netlify
- ✅ **Versionshantering** av all kod
- ✅ **Monitoring** via GitHub Actions
- ✅ **Backup** av all data i molnet

**Din våldskarta kommer nu att:**
- 🔄 **Hämta ny data** från polisen.se automatiskt
- 📊 **Uppdatera webbplatsen** utan din inblandning
- 📈 **Förbättra SEO** med färsk data
- 🔒 **Säkra data** med automatisk versionshantering

**Sätt upp en gång - fungerar för alltid!** ✨

---

## 📞 **Hjälp och support**

### **Om något går fel:**
1. **Kontrollera** GitHub Actions loggar för felmeddelanden
2. **Testa** manuell körning först
3. **Verifiera** Netlify-konfiguration
4. **Kolla** att alla secrets är korrekt inställda

### **Vanliga nybörjarfel:**
- **Glömt pusha kod:** `git push` efter ändringar
- **Fel secrets:** Kontrollera stavning och värden
- **Fel repository-typ:** Måste vara Public för gratis Actions

**Med denna guide ska du kunna sätta upp automatiseringen även som GitHub-nybörjare!** 🚀

