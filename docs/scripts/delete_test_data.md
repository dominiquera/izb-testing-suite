# delete_test_data.py

Löscht die erstellten Testdaten aus Airtable.

## Kontext

Löscht nur die Records, deren IDs in `test_data_ids.json` gespeichert sind.
Wurde von `create_test_data.py` erstellt.

## Eingaben

### Environment Variables
| Variable | Beschreibung |
|----------|--------------|
| `AIRTABLE_TOKEN` | Airtable API Token |
| `AIRTABLE_BASE_ID` | Airtable Base ID |

### Datei
- `test_data_ids.json` - Enthält die zu löschenden Record-IDs

## Ausgaben

- Records werden aus Airtable gelöscht
- `test_data_ids.json` wird gelöscht

### Lösch-Reihenfolge
1. applications (abhängig von allem)
2. documents
3. employees_students
4. deals
5. businesses_clients

## Beispiel

```bash
python delete_test_data.py
```

## Alternative

Für umfangreicheres Löschen (inkl. verknüpfter Records):
→ `find_and_delete_test_data.py`
