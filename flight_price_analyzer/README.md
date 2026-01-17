# Flight Price Analyzer 🛫💰

Ein umfassender Flight Price Analyzer, der das World Wide Web nach den günstigsten Flügen durchsucht und 7 fortgeschrittene Strategien zur Preisoptimierung implementiert.

## 🎯 Hauptfunktionen

Der Analyzer implementiert die folgenden 7 Suchkriterien:

### 1. 📍 Hidden City Tickets & Alternative Routenführung
- **Hidden City Ticketing**: Findet Flüge, bei denen eine Zwischenlandung am eigentlichen Zielort günstiger ist
- **Nahegelegene Flughäfen**: Vergleicht Preise von alternativen Abflug- und Zielflughäfen
- **Multi-Leg Kombinationen**: Analysiert separate Buchungen, die günstiger als Durchgangstickets sein können
- **Detaillierte Analyse**: Zeigt Preisunterschiede und Risiken verschiedener Routing-Strategien

### 2. 🛡️ Anti-Price-Inflation Techniken
- **Tracking-Methoden Analyse**: Identifiziert, wie Airlines wiederholte Suchen erkennen (Cookies, Browser-Fingerprinting, IP-Tracking)
- **Preisinflations-Trigger**: Erklärt welche Verhaltensweisen Preiserhöhungen auslösen
- **Vermeidungsstrategie**: Schritt-für-Schritt Anleitung zur Vermeidung von künstlicher Preiserhöhung
- **Such-Protokoll**: Detaillierte Verhaltensregeln für jede Suche

### 3. 🌍 Geo-Pricing Simulation
- **Länderübergreifender Preisvergleich**: Simuliert Flugpreise in verschiedenen Ländern und Währungen
- **Günstigste Märkte**: Identifiziert, wo das Ticket am günstigsten gebucht werden kann
- **Geo-Pricing Erklärung**: Erklärt, warum Preise regional unterschiedlich sind
- **Legale Zugriffsmethoden**: Zeigt legale Wege auf, um von günstigeren Märkten zu buchen (VPN, lokale Reisebüros, etc.)

### 4. 📊 Historische Preisanalyse
- **Optimales Buchungsfenster**: Berechnet die ideale Zeit für die Buchung basierend auf historischen Daten
- **Wochentag-Analyse**: Zeigt die günstigsten Tage zum Buchen und Fliegen
- **Saisonale Muster**: Analysiert Preisschwankungen nach Jahreszeit
- **Fare Reset Zeiten**: Identifiziert, wann Airlines Preise zurücksetzen
- **Nachfragezyklen**: Erklärt, wie Nachfrage die Preisgestaltung beeinflusst

### 5. 📋 Tarifregeln & Ticketklassen-Analyse
- **Ticket-Klassen Breakdown**: Vergleich von Basic Economy, Standard Economy, Flex und Premium
- **Routing-Logik**: Erklärt Preisunterschiede zwischen Direkt-, Ein-Stopp- und Mehrfach-Stopp-Flügen
- **Preisbedingungen**: Analysiert Vorausbuchungsfristen, Mindestaufenthalt, etc.
- **Kostenreduzierungs-Tipps**: Praktische Hinweise zur Senkung der Gesamtkosten

### 6. 💰 Plattform-Vergleich
- **Multi-Plattform Analyse**: Vergleicht Preise zwischen Airlines, großen OTAs, regionalen Buchungsseiten
- **Gebührenanalyse**: Identifiziert Service-Gebühren, Aufschläge und versteckte Kosten
- **Versteckte Rabatte**: Findet Plattformen mit niedrigeren Basispreisen
- **Zuverlässigkeitsbewertung**: Bewertet Plattformen nach Preis-Leistungs-Verhältnis

### 7. 🔔 Fare Tracking Strategie
- **Preisüberwachung ohne Inflation**: Erstellt Strategien zur Preisbeobachtung ohne Preissteigerungen auszulösen
- **Such-Frequenz**: Optimale Häufigkeit für manuelle Suchen
- **Timing-Resets**: Empfohlene Wartezeiten zwischen Suchen
- **Alert-Setup**: Konfiguration von Preisalarmen
- **Verhaltensregeln**: Praktische Beispiele zur stabilen Preisüberwachung

## 📂 Projektstruktur

```
flight_price_analyzer/
├── main.py                # Einstiegspunkt
├── modules/               # Module für verschiedene Analysen
│   ├── __init__.py
│   ├── search.py          # Hidden city tickets, alternative Routen
│   ├── geo_pricing.py     # Geo-Pricing Simulation
│   ├── inflation.py       # Anti-Price-Inflation Techniken
│   ├── historical.py      # Historische Preisanalyse
│   ├── fare_tracking.py   # Preisüberwachungs-Strategie
│   ├── platform_compare.py # Plattform-Vergleich
│   └── utils.py           # Gemeinsame Hilfsfunktionen
├── requirements.txt       # Python-Abhängigkeiten
├── config.json           # Konfigurationsdatei
└── README.md             # Diese Datei
```

## 🚀 Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritt 1: Repository klonen

```bash
git clone <repository-url>
cd flight_price_analyzer
```

### Schritt 2: Virtuelle Umgebung erstellen (empfohlen)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Schritt 3: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## 💻 Verwendung

### Grundlegende Verwendung

```bash
python main.py FRA JFK 2024-06-15
```

**Parameter:**
- `FRA`: Abflughafen (IATA-Code)
- `JFK`: Zielflughafen (IATA-Code)
- `2024-06-15`: Abflugdatum (JJJJ-MM-TT)

### Mit Rückflug

```bash
python main.py FRA JFK 2024-06-15 --return-date 2024-06-22
```

### Mit Zielpreis

```bash
python main.py FRA JFK 2024-06-15 --target-price 450
```

### Ergebnisse exportieren

```bash
python main.py FRA JFK 2024-06-15 --export meine_analyse
```

Dies erstellt eine Datei `meine_analyse.json` mit allen Analyseergebnissen.

### Vollständiges Beispiel

```bash
python main.py FRA JFK 2024-06-15 \
  --return-date 2024-06-22 \
  --target-price 450 \
  --export flug_analyse_juni
```

## 📊 Ausgabe-Beispiel

```
================================================================================
FLIGHT PRICE ANALYSIS SUMMARY
================================================================================

Route: Frankfurt (FRA) → New York (JFK)
Departure: 2024-06-15
Return: 2024-06-22

--------------------------------------------------------------------------------
KEY RECOMMENDATIONS:
--------------------------------------------------------------------------------
1. 💰 CHEAPEST OPTION: multi_leg_split route at €420.50
2. 🌍 GEO-PRICING: Save €75.00 by booking from Poland
3. ✅ TIMING: You're in the optimal booking window - good time to book!
4. 🛡️  IMPORTANT: Use incognito mode, clear cookies, and limit searches
5. 💻 PLATFORM: Book via Google Flights for lowest total cost
6. 🔔 TRACKING: Set up Google Flights & Kayak price alerts

--------------------------------------------------------------------------------
PRICE SUMMARY:
--------------------------------------------------------------------------------
Direct Flight: €520.00
Cheapest Option: €420.50 (multi_leg_split)
Potential Savings: €99.50 (19.1%)
================================================================================
```

## ⚙️ Konfiguration

Die Datei `config.json` ermöglicht die Anpassung verschiedener Module:

```json
{
  "modules": {
    "search": {
      "enabled": true,
      "include_hidden_city": true,
      "include_nearby_airports": true,
      "max_alternatives": 10
    },
    "geo_pricing": {
      "enabled": true,
      "default_countries": ["DE", "PL", "TR", "IN", "GB", "US"],
      "show_vpn_recommendations": true
    },
    "inflation": {
      "enabled": true,
      "max_searches_per_day": 2,
      "require_incognito_mode": true
    }
    // ... weitere Konfigurationen
  }
}
```

## 🔍 Detaillierte Funktionsbeschreibungen

### Hidden City Ticketing

**Was ist das?**
Manchmal ist ein Ticket zu einer Stadt hinter Ihrem eigentlichen Ziel günstiger. Sie buchen den längeren Flug und steigen bei der Zwischenlandung aus.

**Beispiel:**
- Frankfurt → New York direkt: 800€
- Frankfurt → New York → Boston: 600€
- Sie buchen nach Boston, steigen aber in New York aus

**⚠️ WICHTIG:** Dies verstößt gegen die Geschäftsbedingungen der meisten Airlines. Nur zu Bildungszwecken!

### Geo-Pricing Simulation

**Warum sind Preise unterschiedlich?**
Airlines passen Preise basierend auf:
- Lokale Kaufkraft
- Wettbewerbssituation im Land
- Währungsschwankungen
- Point-of-Sale Regeln

**Beispiel:**
Derselbe Flug kann in Polen 20% günstiger sein als in der Schweiz.

### Anti-Price-Inflation

**Wie erkennen Airlines wiederholte Suchen?**
1. **Cookies**: Verfolgen Ihre Sitzungen
2. **Browser-Fingerprinting**: Einzigartige Browser-Signatur
3. **IP-Adresse**: Verfolgt Suchen vom selben Standort
4. **Suchmuster**: 3+ Suchen in 24 Stunden lösen Erhöhungen aus

**Schutzmaßnahmen:**
1. Immer Incognito-Modus verwenden
2. Cookies vor jeder Suche löschen
3. VPN verwenden (optional)
4. Maximal 1-2 Suchen pro Tag
5. Mindestens 24 Stunden zwischen Suchen warten

## 📈 Praktische Tipps

### Beste Buchungszeiten
- **Wochentag**: Dienstag 15-18 Uhr
- **Vorlaufzeit**: 21-90 Tage vor Abflug (abhängig von Route)
- **Flugzeit**: Dienstag/Mittwoch/Samstag fliegen (10-20% günstiger)

### Plattform-Empfehlungen
1. **Preisvergleich**: Google Flights oder Skyscanner
2. **Buchung**: Direkt bei der Airline (keine OTA-Gebühren)
3. **Preisalarme**: Google Flights + Kayak + Hopper App

### Kostenreduzierung
- Basic Economy wählen (falls kein Gepäck nötig)
- Alternative Flughäfen prüfen (kann 30%+ sparen)
- Separate Oneway-Tickets statt Hin- und Rückflug prüfen
- Eigenes Essen mitbringen
- Mittlere Sitze wählen (oft kostenlos)

## ⚠️ Wichtige Hinweise

### Rechtliche Aspekte

1. **Hidden City Ticketing**: Verstößt gegen die meisten Airline-AGBs
   - Kann zur Sperrung Ihres Vielfliegerkonto führen
   - Funktioniert nur mit Handgepäck
   - Nur für Bildungszwecke dokumentiert

2. **VPN-Nutzung**: Grauzone
   - Kann AGB verletzen
   - Buchung könnte storniert werden
   - Zahlungsadresse sollte übereinstimmen

3. **Separate Tickets**: Legal aber riskant
   - Kein Schutz bei verpassten Anschlüssen
   - Großzügige Pufferzeiten einplanen

### Ethische Überlegungen

Dieser Analyzer dient **ausschließlich zu Bildungszwecken** und zur Transparenz über Airline-Preisgestaltung. Nutzer sollten:
- Airline-AGBs respektieren
- Lokale Gesetze beachten
- Risiken selbst abwägen
- Informierte Entscheidungen treffen

## 🛠️ Entwicklung

### Module hinzufügen

Neue Analysemodule können im `modules/` Verzeichnis hinzugefügt werden:

```python
# modules/my_module.py
from .utils import FlightLogger

class MyAnalyzer:
    def __init__(self, logger=None):
        self.logger = logger or FlightLogger("MyModule")

    def analyze(self, origin, destination):
        # Ihre Analyse hier
        pass
```

### Tests ausführen

```bash
pytest tests/
```

## 📚 Datenquellen

**Hinweis:** Aktuelle Version verwendet Simulationsdaten. Für Produktionsnutzung sollten folgende APIs integriert werden:

- **Google Flights API** (QPX Express - eingestellt, Alternativen nutzen)
- **Skyscanner API**
- **Amadeus API**
- **Kiwi.com API**
- **Lufthansa Open API**

## 🤝 Beitragen

Beiträge sind willkommen! Bitte beachten Sie:

1. Fork des Repositories erstellen
2. Feature-Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Zum Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request öffnen

## 📝 Lizenz

Dieses Projekt dient ausschließlich zu Bildungszwecken. Die Nutzung erfolgt auf eigene Verantwortung.

## ⚡ FAQ

**Q: Funktioniert das wirklich?**
A: Die Prinzipien sind real und dokumentiert. Aktuelle Version nutzt Simulationen. Für echte Preise müssen Flight-APIs integriert werden.

**Q: Ist Hidden City Ticketing legal?**
A: Technisch legal, verstößt aber gegen Airline-AGBs. Kann zu Kontosperrungen führen.

**Q: Wie viel kann ich wirklich sparen?**
A: Typischerweise 10-30% durch optimale Timing und Plattformwahl. Bis zu 50% in extremen Fällen (Geo-Pricing, Hidden City).

**Q: Brauche ich wirklich einen VPN?**
A: Nicht zwingend. Incognito-Modus + Cookie-Löschung sind die wichtigsten Schritte. VPN hilft zusätzlich bei Geo-Pricing.

**Q: Welche Plattform ist am besten?**
A: Google Flights zum Vergleichen, dann direkt bei der Airline buchen (vermeidet OTA-Gebühren).

## 📞 Support

Bei Fragen oder Problemen:
1. GitHub Issues verwenden
2. Dokumentation prüfen
3. Community fragen

## 🎓 Weiterführende Ressourcen

- [Skyscanner Blog: Booking Tips](https://www.skyscanner.de/nachrichten/tipps/)
- [Google Flights Guide](https://www.google.com/travel/flights)
- [ITA Matrix Power User Guide](https://matrix.itasoftware.com/)
- [FlyerTalk Forums](https://www.flyertalk.com/)

---

**Entwickelt mit ❤️ für smarte Reisende**

*Hinweis: Dieses Tool ist zu Bildungszwecken erstellt. Nutzen Sie es verantwortungsvoll und respektieren Sie Airline-AGBs.*
