// Affiliate Marketing System för Stockholm Våldskarta
// Säkerhetsrelaterade produkter och tjänster

const affiliateProducts = {
    security: [
        {
            id: 'verisure-alarm',
            name: 'Verisure Hemlarm',
            description: 'Komplett hemlarmssystem med 24/7 övervakning',
            price: 'Från 299 kr/mån',
            image: '/images/verisure-alarm.jpg',
            affiliateUrl: 'https://www.verisure.se/?ref=stockholmvaldskarta',
            category: 'Hemlarm',
            rating: 4.5,
            commission: '15%'
        },
        {
            id: 'sector-alarm',
            name: 'Sector Alarm',
            description: 'Trådlöst larmsystem med app-styrning',
            price: 'Från 199 kr/mån',
            image: '/images/sector-alarm.jpg',
            affiliateUrl: 'https://www.sectoralarm.se/?ref=stockholmvaldskarta',
            category: 'Hemlarm',
            rating: 4.3,
            commission: '12%'
        },
        {
            id: 'yale-doorman',
            name: 'Yale Doorman',
            description: 'Smart dörrlås med kodlås och app-kontroll',
            price: '2,995 kr',
            image: '/images/yale-doorman.jpg',
            affiliateUrl: 'https://www.yale.se/?ref=stockholmvaldskarta',
            category: 'Smarta lås',
            rating: 4.4,
            commission: '8%'
        }
    ],
    
    insurance: [
        {
            id: 'if-hemforsakring',
            name: 'If Hemförsäkring',
            description: 'Omfattande hemförsäkring med inbrottsskydd',
            price: 'Från 150 kr/mån',
            image: '/images/if-insurance.jpg',
            affiliateUrl: 'https://www.if.se/?ref=stockholmvaldskarta',
            category: 'Försäkring',
            rating: 4.2,
            commission: '25 kr per lead'
        },
        {
            id: 'folksam-hemforsakring',
            name: 'Folksam Hemförsäkring',
            description: 'Trygg hemförsäkring med bra villkor',
            price: 'Från 180 kr/mån',
            image: '/images/folksam-insurance.jpg',
            affiliateUrl: 'https://www.folksam.se/?ref=stockholmvaldskarta',
            category: 'Försäkring',
            rating: 4.1,
            commission: '30 kr per lead'
        }
    ],
    
    safety: [
        {
            id: 'pepper-spray',
            name: 'Laglig Pepparspray',
            description: 'Godkänd pepparspray för självförsvar',
            price: '149 kr',
            image: '/images/pepper-spray.jpg',
            affiliateUrl: 'https://www.sakerhetsprodukter.se/?ref=stockholmvaldskarta',
            category: 'Självförsvar',
            rating: 4.0,
            commission: '10%'
        },
        {
            id: 'personal-alarm',
            name: 'Personlarm',
            description: 'Högt personlarm med LED-ljus',
            price: '99 kr',
            image: '/images/personal-alarm.jpg',
            affiliateUrl: 'https://www.sakerhetsprodukter.se/?ref=stockholmvaldskarta',
            category: 'Personlig säkerhet',
            rating: 4.2,
            commission: '15%'
        }
    ],
    
    legal: [
        {
            id: 'lawline-juridik',
            name: 'Lawline Juridisk Rådgivning',
            description: 'Juridisk hjälp vid brott och försäkringsärenden',
            price: 'Från 500 kr/konsultation',
            image: '/images/lawline.jpg',
            affiliateUrl: 'https://www.lawline.se/?ref=stockholmvaldskarta',
            category: 'Juridik',
            rating: 4.6,
            commission: '100 kr per lead'
        }
    ]
};

// Affiliate tracking och analytics
class AffiliateTracker {
    constructor() {
        this.trackingData = {
            clicks: {},
            conversions: {},
            revenue: 0
        };
    }
    
    trackClick(productId, category) {
        // Spåra klick på affiliate-länkar
        if (!this.trackingData.clicks[productId]) {
            this.trackingData.clicks[productId] = 0;
        }
        this.trackingData.clicks[productId]++;
        
        // Google Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'affiliate_click', {
                'event_category': 'monetization',
                'event_label': productId,
                'custom_parameters': {
                    'product_category': category,
                    'affiliate_partner': this.getPartnerFromProductId(productId)
                }
            });
        }
        
        // Spara i localStorage för senare analys
        this.saveTrackingData();
    }
    
    trackConversion(productId, value) {
        // Spåra konverteringar (om möjligt via postback URLs)
        if (!this.trackingData.conversions[productId]) {
            this.trackingData.conversions[productId] = 0;
        }
        this.trackingData.conversions[productId]++;
        this.trackingData.revenue += value;
        
        if (typeof gtag !== 'undefined') {
            gtag('event', 'affiliate_conversion', {
                'event_category': 'monetization',
                'event_label': productId,
                'value': value
            });
        }
        
        this.saveTrackingData();
    }
    
    getPartnerFromProductId(productId) {
        if (productId.includes('verisure')) return 'Verisure';
        if (productId.includes('sector')) return 'Sector Alarm';
        if (productId.includes('yale')) return 'Yale';
        if (productId.includes('if-')) return 'If Försäkring';
        if (productId.includes('folksam')) return 'Folksam';
        if (productId.includes('lawline')) return 'Lawline';
        return 'Other';
    }
    
    saveTrackingData() {
        localStorage.setItem('affiliateTracking', JSON.stringify(this.trackingData));
    }
    
    loadTrackingData() {
        const saved = localStorage.getItem('affiliateTracking');
        if (saved) {
            this.trackingData = JSON.parse(saved);
        }
    }
    
    getStats() {
        return {
            totalClicks: Object.values(this.trackingData.clicks).reduce((a, b) => a + b, 0),
            totalConversions: Object.values(this.trackingData.conversions).reduce((a, b) => a + b, 0),
            totalRevenue: this.trackingData.revenue,
            clicksByProduct: this.trackingData.clicks,
            conversionsByProduct: this.trackingData.conversions
        };
    }
}

// Skapa global affiliate tracker
const affiliateTracker = new AffiliateTracker();
affiliateTracker.loadTrackingData();

// Funktion för att rendera affiliate-produkter
function renderAffiliateProducts(containerId, category = null, limit = null) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    let products = [];
    
    if (category) {
        products = affiliateProducts[category] || [];
    } else {
        // Visa alla produkter
        Object.values(affiliateProducts).forEach(categoryProducts => {
            products = products.concat(categoryProducts);
        });
    }
    
    if (limit) {
        products = products.slice(0, limit);
    }
    
    const html = products.map(product => `
        <div class="affiliate-product">
            <div class="product-image">
                <img src="${product.image}" alt="${product.name}" onerror="this.src='/images/placeholder.jpg'">
            </div>
            <div class="product-info">
                <h4 class="product-name">${product.name}</h4>
                <p class="product-description">${product.description}</p>
                <div class="product-rating">
                    ${'★'.repeat(Math.floor(product.rating))}${'☆'.repeat(5 - Math.floor(product.rating))}
                    <span class="rating-number">${product.rating}</span>
                </div>
                <div class="product-price">${product.price}</div>
                <div class="product-category">${product.category}</div>
            </div>
            <div class="product-actions">
                <a href="${product.affiliateUrl}" 
                   class="affiliate-link" 
                   target="_blank" 
                   rel="noopener sponsored"
                   onclick="affiliateTracker.trackClick('${product.id}', '${product.category}')">
                    Läs mer & Köp
                </a>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// Funktion för att visa relevanta produkter baserat på våldskarta-data
function showRelevantProducts(crimeType, location) {
    let relevantProducts = [];
    
    // Logik för att visa relevanta produkter baserat på brottstyp
    switch (crimeType.toLowerCase()) {
        case 'rån':
        case 'misshandel':
            relevantProducts = [
                ...affiliateProducts.safety,
                ...affiliateProducts.insurance.slice(0, 1)
            ];
            break;
            
        case 'inbrott':
        case 'stöld':
            relevantProducts = [
                ...affiliateProducts.security,
                ...affiliateProducts.insurance
            ];
            break;
            
        case 'skottlossning':
        case 'explosion':
            relevantProducts = [
                ...affiliateProducts.security,
                ...affiliateProducts.safety,
                ...affiliateProducts.legal
            ];
            break;
            
        default:
            relevantProducts = [
                ...affiliateProducts.security.slice(0, 2),
                ...affiliateProducts.safety.slice(0, 1)
            ];
    }
    
    return relevantProducts.slice(0, 3); // Begränsa till 3 produkter
}

// Funktion för att visa säsongsmässiga eller trendbaserade produkter
function getSeasonalProducts() {
    const month = new Date().getMonth();
    
    // Vinter (dec-feb): Fokus på hemlarm (mer inbrott)
    if (month === 11 || month === 0 || month === 1) {
        return affiliateProducts.security;
    }
    
    // Sommar (jun-aug): Fokus på personlig säkerhet (mer utomhusaktivitet)
    if (month >= 5 && month <= 7) {
        return affiliateProducts.safety;
    }
    
    // Standard: Blandning
    return [
        ...affiliateProducts.security.slice(0, 2),
        ...affiliateProducts.safety.slice(0, 1),
        ...affiliateProducts.insurance.slice(0, 1)
    ];
}

// Export för användning i andra filer
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        affiliateProducts,
        affiliateTracker,
        renderAffiliateProducts,
        showRelevantProducts,
        getSeasonalProducts
    };
}

