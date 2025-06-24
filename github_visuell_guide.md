# GitHub Setup - Visuell Guide med Skärmdumpar

## 📸 **Visuell Guide för GitHub Nybörjare**

*Denna guide kompletterar den detaljerade textuella guiden med visuella referenser*

---

## 🎯 **STEG 1: Skapa GitHub-konto**

### **1.1: Gå till GitHub.com**
```
URL: https://github.com
```
**Vad du ser:**
- Stor "Sign up" knapp i övre högra hörnet
- "Sign in" länk bredvid för befintliga användare

### **1.2: Registreringsformulär**
**Fyll i:**
- **Username:** Välj något unikt (t.ex. "erik-stockholm-karta")
- **Email:** Din email-adress
- **Password:** Starkt lösenord

**Tips:** Username blir del av din URL (github.com/USERNAME)

### **1.3: Verifiering**
- GitHub skickar verifieringsemail
- Klicka länken i emailet
- Välj "Free" plan (0 kr/månad)

---

## 🎯 **STEG 2: Skapa nytt Repository**

### **2.1: Hitta "New" knappen**
**Efter inloggning ser du:**
- Grön "New" knapp (vänster sida)
- Eller gå direkt till: https://github.com/new

### **2.2: Repository-inställningar**
**Fyll i formuläret:**
```
Repository name: stockholm-violence-map
Description: Automatiserad våldskarta för Stockholm med data från polisen.se
```

**Viktiga inställningar:**
- ✅ **Public** (måste vara valt för gratis GitHub Actions)
- ✅ **Add a README file** (kryssa i denna)
- ❌ **Add .gitignore** (lämna tom)
- ❌ **Choose a license** (lämna tom)

### **2.3: Klicka "Create repository"**
**Du kommer nu till din nya repository-sida**

---

## 🎯 **STEG 3: Klona Repository**

### **3.1: Hitta "Code" knappen**
**På din repository-sida:**
- Grön "Code" knapp (höger sida)
- Klicka den för att se URL

### **3.2: Kopiera URL**
**I dropdown-menyn:**
- Välj "HTTPS" tab (standard)
- URL ser ut som: `https://github.com/USERNAME/stockholm-violence-map.git`
- Klicka kopiera-ikonen

### **3.3: Terminal-kommandon**
```bash
# Navigera till Desktop (eller valfri mapp)
cd Desktop

# Klona repository (ersätt URL med din egen)
git clone https://github.com/USERNAME/stockholm-violence-map.git

# Gå in i mappen
cd stockholm-violence-map
```

---

## 🎯 **STEG 4: Lägg till Secrets**

### **4.1: Gå till Settings**
**I ditt repository:**
- Klicka "Settings" tab (högst upp, längst till höger)
- **OBS:** Inte din profil-settings, utan repository-settings

### **4.2: Hitta Secrets**
**I vänster meny:**
- Scrolla ner till "Security" sektion
- Klicka "Secrets and variables"
- Klicka "Actions"

### **4.3: Lägg till första secret**
**Klicka "New repository secret"**
```
Name: NETLIFY_SITE_ID
Secret: [Ditt Site ID från Netlify]
```
**Klicka "Add secret"**

### **4.4: Lägg till andra secret**
**Klicka "New repository secret" igen**
```
Name: NETLIFY_ACCESS_TOKEN
Secret: [Din Access Token från Netlify]
```
**Klicka "Add secret"**

---

## 🎯 **STEG 5: Hitta Netlify-uppgifter**

### **5.1: Netlify Site ID**
**I Netlify dashboard:**
1. Klicka på din webbplats (08-violence.netlify.app)
2. Klicka "Site settings" (i huvudmenyn)
3. Under "General" → "Site details"
4. Kopiera "Site ID" (lång sträng med bokstäver och siffror)

### **5.2: Netlify Access Token**
**Skapa ny token:**
1. Klicka din avatar (övre högra hörnet i Netlify)
2. Välj "User settings"
3. Klicka "Applications" (vänster meny)
4. Under "Personal access tokens"
5. Klicka "New access token"
6. Beskrivning: "Stockholm Våldskarta Automation"
7. Klicka "Generate token"
8. **KOPIERA OMEDELBART** (visas bara en gång!)

---

## 🎯 **STEG 6: Aktivera GitHub Actions**

### **6.1: Gå till Actions**
**I ditt repository:**
- Klicka "Actions" tab (högst upp)

### **6.2: Aktivera workflows**
**Om du ser en varning:**
- "Workflows aren't being run on this forked repository"
- Klicka "I understand my workflows, go ahead and enable them"

### **6.3: Hitta din workflow**
**Du ska se:**
- "Stockholm Våldskarta Auto Update" workflow
- Status: Grön cirkel = aktiv, Grå = inaktiv

---

## 🎯 **STEG 7: Testa automatiseringen**

### **7.1: Manuell körning**
**I Actions-sidan:**
1. Klicka på "Stockholm Våldskarta Auto Update"
2. Klicka "Run workflow" (höger sida)
3. Klicka den gröna "Run workflow" knappen

### **7.2: Övervaka körning**
**Du ser nu:**
- Gul cirkel = Körs
- Grön bock = Lyckades
- Röd X = Misslyckades

### **7.3: Kontrollera loggar**
**Klicka på körningen för att se:**
- Detaljerade loggar
- Felmeddelanden (om något gick fel)
- Tidsåtgång för varje steg

---

## 🔧 **Vanliga UI-element att känna igen**

### **GitHub Repository-sida:**
```
[Code] [Issues] [Pull requests] [Actions] [Projects] [Wiki] [Security] [Insights] [Settings]
```

### **Actions-sida:**
```
[All workflows] [Stockholm Våldskarta Auto Update]
                [Run workflow ▼]
```

### **Settings → Secrets:**
```
Repository secrets:
✅ NETLIFY_SITE_ID
✅ NETLIFY_ACCESS_TOKEN
[New repository secret]
```

---

## 📊 **Status-indikatorer**

### **GitHub Actions Status:**
- 🟢 **Grön bock:** Lyckad körning
- 🟡 **Gul cirkel:** Pågående körning  
- 🔴 **Röd X:** Misslyckad körning
- ⚪ **Grå cirkel:** Inaktiv/väntande

### **Repository Status:**
- **Public:** Synlig för alla (krävs för gratis Actions)
- **Private:** Endast du kan se (kostar pengar för Actions)

---

## 🎯 **Snabbkontroll - Är allt rätt?**

### **✅ Checklista:**
- [ ] GitHub-konto skapat
- [ ] Repository skapat (Public)
- [ ] Git installerat på datorn
- [ ] Repository klonat lokalt
- [ ] Automatiseringsfiler tillagda
- [ ] Filer pushade till GitHub
- [ ] NETLIFY_SITE_ID secret tillagd
- [ ] NETLIFY_ACCESS_TOKEN secret tillagd
- [ ] GitHub Actions aktiverat
- [ ] Första testkörning genomförd

### **🔍 Verifiering:**
1. **GitHub Actions:** Grön bock på senaste körning
2. **Netlify:** Webbplatsen uppdaterad med ny data
3. **Repository:** Automatiska commits syns i historiken

---

## 📱 **GitHub Mobile App**

**För monitoring på språng:**
- Ladda ner "GitHub" app
- Logga in med samma konto
- Få notifikationer när Actions körs
- Kontrollera status var som helst

---

## 🎉 **Du är klar!**

**Om alla steg är genomförda har du:**
- ✅ **Automatiserad våldskarta** som uppdateras var 6:e timme
- ✅ **GitHub Actions** som kör gratis i molnet
- ✅ **Automatisk deployment** till Netlify
- ✅ **Monitoring** via GitHub interface
- ✅ **Backup** av all kod i molnet

**Grattis! Du har nu en professionell automatiserad lösning!** 🚀

---

## 📞 **Hjälp vid problem**

### **Om något ser annorlunda ut:**
- GitHub uppdaterar sitt interface regelbundet
- Grundfunktionerna är samma
- Sök efter liknande knappar/menyer

### **Vanliga misstag:**
- **Fel repository-typ:** Måste vara Public
- **Glömt secrets:** Båda måste finnas
- **Fel URL:** Kontrollera att du klonat rätt repository

**Följ denna visuella guide tillsammans med den detaljerade textguiden för bästa resultat!** 📖✨

