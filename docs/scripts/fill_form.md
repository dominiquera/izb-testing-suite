# fill_form.py

Füllt das Datenerfassungsformular automatisch aus (Playwright).

## Kontext

Nach dem PandaDoc unterschrieben wird:
1. Make-Prozess startet → erstellt Business-Application in Airtable
2. Dieses Skript macht ein **UPDATE** auf die existierende Application

## Eingaben

### URL-Parameter
| Parameter | Beschreibung |
|-----------|--------------|
| `deal_id` | Deal-ID aus Airtable |
| `id` | Record-ID der Application |

### Konfiguration (im Script)
| Parameter | Beschreibung |
|-----------|--------------|
| `FORM_URL` | Komplette URL mit Parametern |
| `HEADLESS` | True/False - Browser sichtbar? |
| `TEST_DATA` | Dict mit allen Formulardaten |

### TEST_DATA Struktur
- Persönliche Daten (Geschlecht, Name, etc.)
- Unternehmensdaten (Firma, Branche, Adresse)
- Mitarbeiterzahlen
- Betriebsdaten (Betriebsnummer, eService)
- Bankdaten
- Mitarbeiter-Subformular (Array)

## Ausgaben

- Formular wird ausgefüllt und abgesendet
- Application in Airtable wird aktualisiert

## Voraussetzungen

```bash
pip install playwright
playwright install chromium
```

## Beispiel

```bash
python fill_form.py
```

## Nächster Schritt
→ `trigger_document_creation.py`
