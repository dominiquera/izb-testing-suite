# make_queue_webhook_rerun.py

Sendet JSON-Payload an eine Webhook-URL.

## Eingaben

### Konfiguration (im Script)
| Parameter | Beschreibung |
|-----------|--------------|
| `WEBHOOK_URL` | Ziel-URL für den Webhook |
| `PAYLOAD_FILE` | Pfad zur JSON-Datei |

### Datei
- `webhook_payload.json` - JSON-Payload zum Senden

## Ausgaben

- HTTP Response Status
- Response Body

## Beispiel

1. JSON in `webhook_payload.json` einfügen:
```json
{
  "key": "value"
}
```

2. Skript ausführen:
```bash
python make_queue_webhook_rerun.py
```
