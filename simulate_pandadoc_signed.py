#!/usr/bin/env python3
"""
Simulate PandaDoc signature - triggers "1.1 neuen QCG Auftrag starten".

This script simulates the webhook that is triggered when a customer signs
the PandaDoc contract. It calls the Make webhook to start folder creation.

Usage:
    python scripts/tests/simulate_pandadoc_signed.py
"""

import requests

# ============================================================
# CONFIGURATION - Edit these values as needed
# ============================================================

# Email address to send
EMAIL = "dominique@landeseiten.de"

# Google Drive File ID (from URL: https://drive.google.com/file/d/FILE_ID/view)
# Upload folder: https://drive.google.com/drive/u/4/folders/1EDHnjVEdbhOJ4x_CETUhYNAMJpBW6fhw
FILE_ID = "101gsYGcLz513_MQsmngDMFnrXknZey9z"
#https://drive.google.com/file/d/101gsYGcLz513_MQsmngDMFnrXknZey9z/view?usp=sharing

# Die File-ID ist die Datei Testdatei peg,
# die in der Zwischenablage liegt, die an den Webhook übergeben 
# werden muss, weil das eigentlich das Panda-Doc ist, was heruntergeladen werden soll.
# Die wird normalerweise von dem anderen Webhook eben, 
# sobald das PandaDoc unterschrieben ist, runtergeladen und in die Zwischenablage hochgeladen. 

# Webhook URL
WEBHOOK_URL = "https://hook.eu1.make.com/j7poahnr90vxqm1yqo1fknl5cnfftaxb"

# ============================================================
# DO NOT EDIT BELOW THIS LINE
# ============================================================


def main():
    payload = {
        "email": EMAIL,
        "file_id": FILE_ID
    }

    print(f"Calling Make webhook...")
    print(f"URL: {WEBHOOK_URL}")
    print(f"Email: {EMAIL}")
    print(f"File ID: {FILE_ID or '(empty)'}")

    print("\nSending POST request...")
    response = requests.post(WEBHOOK_URL, json=payload)

    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.text}")


if __name__ == '__main__':
    main()
