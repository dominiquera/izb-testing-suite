#!/usr/bin/env python3
"""
Make Queue Webhook Rerun - Sendet JSON-Payload an eine Webhook-URL.
"""

import json
import requests

WEBHOOK_URL = "HIER_DEINE_WEBHOOK_URL_EINFUEGEN"
PAYLOAD_FILE = "webhook_payload.json"


def send_webhook():
    with open(PAYLOAD_FILE, "r") as f:
        payload = json.load(f)

    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")


if __name__ == "__main__":
    send_webhook()
