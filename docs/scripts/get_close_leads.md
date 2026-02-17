# get_close_leads.py

Sucht Leads in Close CRM nach E-Mail-Adresse.

## Eingaben

### Environment Variables
| Variable | Beschreibung |
|----------|--------------|
| `CLOSE_API_KEY` | Close API Key (Basic Auth) |

### Konfiguration (im Script)
| Parameter | Beschreibung |
|-----------|--------------|
| `email_to_search` | E-Mail-Adresse zum Suchen |

## Ausgaben

- Liste aller Leads mit der E-Mail
- Pro Lead: ID, Name, Status, Kontakte, Custom Fields
- Link zum Lead in Close

## API-Aufruf

```
GET https://api.close.com/api/v1/lead/
?query=email:"..."
```

## Beispiel

```bash
python get_close_leads.py
```

Ausgabe:
```
--- Lead 1 ---
ID:          lead_xxx
Name:        Firma ABC
Status:      Datenbank
URL:         https://app.close.com/lead/lead_xxx
Kontakte:
  - Max Mustermann
    E-Mails: max@firma.de
```
