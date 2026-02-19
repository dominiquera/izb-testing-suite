"""
Schaltet Kurse für einen Studenten frei via Make.com Webhook.

Verwendung:
    1. STUDENT_RECORD_ID im Script setzen und ausführen:
       python schalte_kurse_frei.py

    2. Oder ID als Parameter übergeben:
       python schalte_kurse_frei.py rec123ABC456
"""

import sys
import requests

# =============================================================================
# KONFIGURATION
# =============================================================================

MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/nh9qkxqofgmcfrah8ntk6ka676ur7480"

STUDENT_RECORD_ID = "reczDH8zu7N5O4y1M"  # Hier die Student-ID eintragen


# =============================================================================
# HAUPTFUNKTION
# =============================================================================

def schalte_kurse_frei(student_record_id: str) -> bool:
    """
    Sendet die Student-ID an den Make.com Webhook.

    Args:
        student_record_id: Die Airtable Record-ID des Studenten

    Returns:
        True bei Erfolg, False bei Fehler
    """
    print(f"Sende Anfrage für Student: {student_record_id}")

    payload = {
        "student_record_id": student_record_id
    }

    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=30)

        if response.ok:
            print(f"[OK] Kurse freigeschaltet (Status: {response.status_code})")
            if response.text:
                print(f"Antwort: {response.text}")
            return True
        else:
            print(f"[FEHLER] Status {response.status_code}: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("[FEHLER] Timeout - keine Antwort vom Server")
        return False
    except requests.exceptions.RequestException as e:
        print(f"[FEHLER] Verbindungsfehler: {e}")
        return False


if __name__ == "__main__":
    # Nimm ID aus Kommandozeile oder aus der Konfiguration
    if len(sys.argv) >= 2:
        student_id = sys.argv[1]
    else:
        student_id = STUDENT_RECORD_ID

    success = schalte_kurse_frei(student_id)
    sys.exit(0 if success else 1)
