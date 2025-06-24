#!/bin/bash

# Stockholm Våldskarta - Automatisering Setup Script
# Detta script sätter upp automatisk uppdatering av våldskarta

set -e

echo "🚀 Stockholm Våldskarta - Automatisering Setup"
echo "=============================================="

# Kontrollera Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 krävs men är inte installerat"
    exit 1
fi

# Skapa virtual environment
echo "📦 Skapar Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Installera dependencies
echo "📥 Installerar Python-paket..."
pip install requests python-crontab

# Skapa nödvändiga mappar
echo "📁 Skapar mappar..."
mkdir -p backups
mkdir -p logs

# Kopiera befintlig data och HTML
echo "📋 Kopierar befintliga filer..."
if [ -f "../stockholm_violence_final_v3.json" ]; then
    cp ../stockholm_violence_final_v3.json stockholm_violence_data.json
    echo "✅ Kopierade befintlig dataset"
else
    echo "⚠️  Ingen befintlig dataset hittades"
fi

if [ -f "../stockholm-violence-map-SEO-OPTIMIZED/index.html" ]; then
    cp ../stockholm-violence-map-SEO-OPTIMIZED/index.html index.html
    echo "✅ Kopierade SEO-optimerad HTML"
else
    echo "⚠️  Ingen HTML-fil hittades"
fi

# Gör script körbart
chmod +x auto_update.py
chmod +x setup_cron.py

echo ""
echo "✅ Setup slutfört!"
echo ""
echo "📋 Nästa steg:"
echo "1. Redigera config.json med dina Netlify-uppgifter"
echo "2. Kör: python3 setup_cron.py för att sätta upp automatisk schemaläggning"
echo "3. Testa: python3 auto_update.py för att köra en manuell uppdatering"
echo ""
echo "🔧 Konfiguration:"
echo "- Redigera config.json för att ange Netlify Site ID och Access Token"
echo "- Ändra schedule i config.json för att justera uppdateringsfrekvens"
echo "- Kontrollera logs/ mappen för automatiseringsloggar"
echo ""

