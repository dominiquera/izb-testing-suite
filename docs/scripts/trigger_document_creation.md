# trigger_document_creation.py

Triggert die Dokumentenerstellung via N8N Webhook.

## Kontext

Simuliert den Zustand nach dem Ausfüllen des Applikationsformulars.
Legt Dokumente und Business-Daten an.

## Eingaben

### Konfiguration (im Script)
| Parameter | Werte | Beschreibung |
|-----------|-------|--------------|
| `USE_PRODUCTION_WEBHOOK` | True/False | Prod oder Test Webhook |
| `SELECTED_FORMULAR` | 1-8 | Welches Formular |

## Ausgaben

- N8N Webhook wird aufgerufen
- Dokumente werden in Airtable angelegt
- Business-Daten werden verarbeitet

## API-Aufruf

```
POST https://n8n.../webhook/...
Content-Type: application/json

{
  "record_id": "...",
  "formular": "..."
}
```

## Beispiel

```bash
python trigger_document_creation.py
```

## Nächster Schritt
→ `simulate_pandadoc_signed.py`
