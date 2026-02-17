# find_and_delete_test_data.py

Findet und löscht Testdaten inkl. aller verknüpften Records.

## Kontext

Sucht in der Applications-Tabelle nach "Test" im Namen und findet
automatisch alle verknüpften Records (documents, employees, deals, businesses).

## Eingaben

### Environment Variables
| Variable | Beschreibung |
|----------|--------------|
| `AIRTABLE_TOKEN` | Airtable API Token |
| `AIRTABLE_BASE_ID` | Airtable Base ID |

### CLI Parameter
| Parameter | Beschreibung |
|-----------|--------------|
| `--delete` | Führt die Löschung durch |

## Ausgaben

### Ohne --delete
- Listet alle gefundenen Testdaten auf
- Zeigt verknüpfte Records pro Tabelle

### Mit --delete
- Löscht alle gefundenen Records
- In korrekter Reihenfolge (abhängige zuerst)

## Beispiel

```bash
# Nur anzeigen
python find_and_delete_test_data.py

# Löschen
python find_and_delete_test_data.py --delete
```
