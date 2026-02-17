#!/usr/bin/env python3
"""
Trigger document creation workflow (simulates filled application form).

This script simulates the state after the application form has been filled out.
It creates documents and business data so that documents can be generated.

Usage:
    python scripts/tests/trigger_document_creation.py
"""

import json
import requests
from pathlib import Path

# ============================================================
# CONFIGURATION - Edit these values as needed
# ============================================================

# Webhook URLs
WEBHOOK_URL_TEST = "https://n8n.srv1043111.hstgr.cloud/webhook-test/e85497e7-5204-42ae-acf0-445692523e1e"
WEBHOOK_URL_PROD = "https://n8n.srv1043111.hstgr.cloud/webhook/e85497e7-5204-42ae-acf0-445692523e1e"

# Set to True for production webhook, False for test webhook
USE_PRODUCTION_WEBHOOK = True

# Formular Selection (1, 2, 3, ...)
SELECTED_FORMULAR = 2

# Available Formulare
FORMULARE = {
    1: {"id": "Kp7FqM2ZsB9aXJfTgR4LwD", "name": "Begründungsschreiben"},
    2: {"id": "angebot", "name": "Angebot"},
    3: {"id": "YYY", "name": "Formular 3"},
}

# Test data values
VORNAME = "Dominique1"
NACHNAME = "Test Datensatz"
APPLICATION_FOLDER = "https://drive.google.com/drive/u/4/folders/1EDHnjVEdbhOJ4x_CETUhYNAMJpBW6fhw"

# Der application_folder ist in der Fördernetzdokumente die Zwischenablage. 

# ============================================================
# DO NOT EDIT BELOW THIS LINE
# ============================================================

SCRIPT_DIR = Path(__file__).parent
TEST_DATA_FILE = SCRIPT_DIR / 'test_data_ids.json'


def main():
    # Check if test_data_ids.json exists
    if not TEST_DATA_FILE.exists():
        print(f"Error: {TEST_DATA_FILE} not found.")
        print("Please run 'python scripts/tests/create_test_data.py' first.")
        return

    # Load the test data IDs
    with open(TEST_DATA_FILE, 'r') as f:
        test_data = json.load(f)

    document_record_id = test_data.get('document_id')
    employee_record_id = test_data.get('employee_student_id')

    if not document_record_id or not employee_record_id:
        print("Error: Missing document_id or employee_student_id in test_data_ids.json")
        return

    # Select webhook URL based on flag
    webhook_url = WEBHOOK_URL_PROD if USE_PRODUCTION_WEBHOOK else WEBHOOK_URL_TEST
    webhook_type = "PRODUCTION" if USE_PRODUCTION_WEBHOOK else "TEST"

    # Get selected formular
    formular = FORMULARE[SELECTED_FORMULAR]

    # Build the payload (wrapped in "data" for N8N access via $json.body.data.*)
    payload = {
        "data": {
            "formular_unique_id": formular["id"],
            "employee.first_name": VORNAME,
            "employee.last_name": NACHNAME,
            "document_name": formular["name"],
            "application_folder": APPLICATION_FOLDER,
            "document_record_id": document_record_id,
            "employees_record_id": employee_record_id
        }
    }

    print(f"Calling N8N webhook ({webhook_type})...")
    print(f"Formular: {SELECTED_FORMULAR} - {formular['name']}")
    print(f"URL: {webhook_url}")
    print(f"\nPayload (data):")
    for key, value in payload["data"].items():
        print(f"  {key}: {value or '(empty)'}")

    # Send the request
    print("\nSending POST request...")
    response = requests.post(webhook_url, json=payload)

    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.text}")


if __name__ == '__main__':
    main()
