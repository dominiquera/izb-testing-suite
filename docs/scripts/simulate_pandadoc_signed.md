# simulate_pandadoc_signed.py

Simuliert, dass der PandaDoc-Vertrag unterschrieben wurde.

## Kontext

Ruft den Make-Webhook "1.1 neuen QCG Auftrag starten" auf.
→ Ordner werden in Google Drive erstellt.

## Eingaben

### Konfiguration (im Script)
| Parameter | Beschreibung |
|-----------|--------------|
| `EMAIL` | E-Mail-Adresse |
| `FILE_ID` | Google Drive File ID der PDF |

### Vorbereitung
1. PDF in den Upload-Folder hochladen
2. File-ID aus der Google Drive URL kopieren
3. Im Script eintragen

## Ausgaben

- Make Webhook wird aufgerufen
- QCG Auftrag wird gestartet
- Ordner werden in Google Drive erstellt

## API-Aufruf

```
POST https://hook.eu2.make.com/...
Content-Type: application/json

{
  "email": "...",
  "file_id": "..."
}
```

## Beispiel

```bash
python simulate_pandadoc_signed.py
```

## Nächster Schritt
→ `delete_test_data.py` (Aufräumen)
