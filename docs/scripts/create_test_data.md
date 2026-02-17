# create_test_data.py

Erstellt verknüpfte Testdaten in Airtable für Workflow-Tests.

## Eingaben

### Environment Variables
| Variable | Beschreibung |
|----------|--------------|
| `AIRTABLE_TOKEN` | Airtable API Token |
| `AIRTABLE_BASE_ID` | Airtable Base ID |

### Konfiguration (im Script)
| Parameter | Werte | Beschreibung |
|-----------|-------|--------------|
| `SELECTED_STATUS` | 1=pending, 2=done, 3=error | Document Status |
| `SELECTED_FORMULAR` | 1-8 | Formular-Typ |
| `EMPLOYEE_FIRST_NAME` | String | Vorname Mitarbeiter |
| `EMPLOYEE_LAST_NAME` | String | Nachname Mitarbeiter |
| `BUSINESS_NAME` | String | Firmenname |

## Ausgaben

### Airtable Records
Erstellt folgende verknüpfte Records:
1. `businesses_clients` - Firmendaten
2. `deals` - Deal-Eintrag
3. `employees_students` - Mitarbeiter
4. `documents` - Dokument mit Formular-Link
5. `applications` - Applikation

### Datei
- `test_data_ids.json` - Speichert alle erstellten Record-IDs

## Beispiel

```bash
python create_test_data.py
```

## Nächster Schritt
→ `fill_form.py` oder `trigger_document_creation.py`
