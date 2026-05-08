# boekhoud.py

> Dubbel boekhouden voor ZZP en klein MKB — lokaal, offline, volledig toetsenbordgedreven.

```
┌───────────────────────────────────────────────────────────────────────────┐
│ Dagboek:     [ VER1                     ]   Saldo:   0.00                 │
│ Boekstuknr:  2026-0042                                                    │
│ Datum:       15-04-2026                                                   │
│ Omschrijving: Factuur april diensten                                      │
├────────┬─────────────────────────────────────────┬──────────┬─────────────┤
│ Rek.nr │ Omschrijving                            │ Relatie  │      Bedrag │
├────────┼─────────────────────────────────────────┼──────────┼─────────────┤
│  1300  │ Factuur april diensten                  │ 1001     │      121.00 │
│  8000  │ Factuur april diensten                  │          │     -100.00 │
│  1500  │ BTW Voorheffing                         │          │      -21.00 │
└────────┴─────────────────────────────────────────┴──────────┴─────────────┘
 F2=Zoek  Shift+F2=Nieuw  F5=Factuur  F9=Volgende  F10=Vorige  Esc=Terug
```

---

## Wat is boekhoud.py?

boekhoud.py is boekhoudssoftware voor de ZZP'er of het kleine MKB die:

- Geen abonnement wil betalen voor software die ze dagelijks nodig hebben
- Hun financiële data **niet** in een Amerikaanse cloud wil hebben
- Snel wil werken — invoer via toetsenbord, geen muis nodig
- Houdt van eenvoud en overzicht zonder onnodige complexiteit

Geïnspireerd op klassieke DOS-boekhoudpakketten uit de jaren '80 en '90.
Gebouwd met moderne Python, maar met dezelfde filosofie: **snel, stil, toetsenbordgedreven**.

---

## Kenmerken

- **Volledig lokaal** — draait zonder internet, geen cloud, geen accounts
- **Privacy by design** — geen telemetrie, geen analytics, geen externe verbindingen
- **Optionele AES-256 encryptie** — database versleuteld met Argon2id, KeePassXC-model
- **Dubbel boekhouden** — grootboek, dagboeken, journaalposten, balans, W&V
- **PDF facturen** — gegenereerd via ReportLab, volledig lokaal
- **Excel export** — via openpyxl
- **Toetsenbord eerst** — alle functies bereikbaar zonder muis
- **NL + EN** — taal wisselen zonder herstart, ES gepland
- **Cross-platform** — Windows, macOS, Linux

---

## Boekhoudmodel

Gebaseerd op klassieke DOS-boekhoudfilosofie. Kernprincipes:

- **Geen debiteur/crediteur splitsing** — alleen relaties, saldo bepaalt de rol
- **Geen blokkades** — de boekhouder beslist zelf, software waarschuwt maar blokkeert nooit
- **BTW als expliciete boekingsregel** — geen automatische berekening op de achtergrond
- **Positief/negatief bedrag** — geen D/C keuze bij invoer

---

## Stack

| Laag | Technologie |
|---|---|
| Taal | Python 3.11+ |
| TUI | Textual (Textualize) |
| Database | SQLite / SQLCipher (AES-256) |
| Key derivation | Argon2id (argon2-cffi) |
| PDF | ReportLab |
| Excel | openpyxl |
| Packaging | PyInstaller |

---

## Installatie

*Fase 1 is in ontwikkeling. Releases volgen via [dospy.nl](https://dospy.nl).*

```bash
# Vanuit broncode (ontwikkelaars)
pip install -r requirements.txt
python main.py
```

---

## Roadmap

| Fase | Inhoud |
|---|---|
| **Fase 1** *(huidig)* | Grootboek, dagboeken, relaties, boekingscherm, balans/W&V, PDF-factuur, NL + EN, optionele AES-256 |
| Fase 2 | Multi-administratie, PDF-export rapporten, Spaans (ES), factuursjablonen |
| Fase 3 | Bankimport CSV/MT940, BTW-aangifte overzicht |
| Fase 4 | Vergelijkingsperiodes, uitgebreide rapportage |

---

## Bijdragen

Bijdragen zijn welkom. Lees `CONTRIBUTING.md` voordat je een pull request opent.

Heb je een bug gevonden of een idee? Open een issue.

---

## Licentie

GPL-3.0 — zie `LICENSE`

---

## Over dospy

boekhoud.py is een project van [tweekwadraat](https://github.com/tweekwadraat) —
een initiatief voor lokale, privacyvriendelijke software met een DOS-gevoel.

Website: [dospy.nl](https://dospy.nl)