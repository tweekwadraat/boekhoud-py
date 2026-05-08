# Bijdragen aan boekhoud.py

Fijn dat je wil bijdragen. Dit document legt uit hoe dat werkt.

---

## Filosofie eerst

boekhoud.py is gebouwd op een bewuste filosofie: lokaal, privacyvriendelijk, toetsenbordgedreven, geen onnodige complexiteit. Lees de README voordat je begint. Een bijdrage die tegen deze principes ingaat wordt niet geaccepteerd, hoe technisch goed ook.

Concreet betekent dat:
- Geen externe verbindingen, geen telemetrie, geen cloud-afhankelijkheden
- Geen features die de interface drukker maken zonder duidelijke noodzaak
- Geen afhankelijkheden toevoegen die niet strikt noodzakelijk zijn

---

## Hoe bijdragen

### Bug melden
Open een issue met:
- Wat je deed
- Wat je verwachtte
- Wat er gebeurde
- Platform (Windows / macOS / Linux) en Python-versie

### Idee of feature request
Open een issue met een duidelijke omschrijving. Leg uit waarom het past bij de filosofie. Discussie is welkom voordat er code geschreven wordt — zo voorkom je werk voor niets.

### Code bijdragen
1. Fork de repository
2. Maak een branch aan: `git checkout -b mijn-aanpassing`
3. Schrijf leesbare, gedocumenteerde code — dit is een portfoliostuk
4. Test je wijziging handmatig
5. Open een pull request met een heldere beschrijving van wat je hebt gedaan en waarom

---

## Stijlafspraken

- Python 3.11+
- Geen ORM — directe SQL queries via `queries.py`
- Alle UI-teksten via de i18n JSON bestanden (`nl.json`, `en.json`) — nooit hardcoded
- Monospace, DOS-gevoel — nieuwe UI-elementen sluiten aan op de bestaande stijl
- Geen externe API-calls, ooit, nergens

---

## Licentie

Door bij te dragen ga je akkoord dat jouw bijdrage valt onder de GPL-3.0 licentie van dit project.

---

*Vragen? Open een issue of mail naar info@dospy.nl*