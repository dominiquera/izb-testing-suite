#!/usr/bin/env python3
"""
Create test data in Airtable for N8N workflow testing.

Usage:
    python scripts/tests/create_test_data.py

This script creates records in Airtable and saves the IDs to a JSON file
so they can be deleted later with delete_test_data.py.
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# CONFIGURATION - Edit these values as needed
# ============================================================

# Document Status (1 = pending, 2 = done, 3 = error)
# Wenn ich hier "pending" benutze, dann wird das
# Dokument vom Queue Worker aufgegriffen.
SELECTED_STATUS = 1

# Available Statuses (must match Airtable select options exactly)
DOCUMENT_STATUSES = {
    1: "pending",
    2: "done",
    3: "error",
}

# Formular Selection (1-8)
SELECTED_FORMULAR = 6  # Default: Begründung

# Available Formulare (Record IDs aus der Formulare-Tabelle)
FORMULARE = {
    1: {"record_id": "rec1blf92rNJHMnMm", "name": "Erklärung zum Antrag auf Arbeitsentgeldzuschuss"},
    2: {"record_id": "rec8SMvfyw5kGtGqp", "name": "Antrag Traegerbescheinigung"},
    3: {"record_id": "recJ5N0vBuDFsyHuX", "name": "Erhebungsbogen"},
    4: {"record_id": "recTmUufcDgr8MAQo", "name": "Antrag auf Arbeitsentgeldzuschuss"},
    5: {"record_id": "recUJsXu6JY0W9L2v", "name": "Fragebogen"},
    6: {"record_id": "recZi1OrSB9AXNWBs", "name": "Begründung"},
    7: {"record_id": "reckptGU51LIAk3rt", "name": "Vollmacht Beschaeftigungsqualifizierung"},
    8: {"record_id": "recpJp8l27QGhRy7j", "name": "Liste der Teilnehmenden"},
}

# Employee/Student data
EMPLOYEE_FIRST_NAME = "Dominique1"
EMPLOYEE_LAST_NAME = "Test Datensatz"
EMPLOYEE_JOB_TITLE = "Senior Finanzbuchhalter"
EMPLOYEE_WORK_START_DATE = "2000-01-01"

# Business Client data
BUSINESS_NAME = "Test Business Name"
BUSINESS_BRANCHE = "Finanzbuchhaltung"

# Deal data
DEAL_NAME = "Test Deal Name"

# Educational Program (existing record ID)
EDUCATIONAL_PROGRAM_ID = "recBOt4ixxB7s1AGx"

# Application data
APPLICATION_NAME = "Test Application"
APPLICATION_STATUS = "to be generated"
ANTRAGS_ART = "Einzelantrag"
APPLICATION_FOLDER = "https://drive.google.com/drive/u/4/folders/1EDHnjVEdbhOJ4x_CETUhYNAMJpBW6fhw"

# ============================================================
# DO NOT EDIT BELOW THIS LINE
# ============================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
TEST_DATA_FILE = SCRIPT_DIR / 'test_data_ids.json'

# Load environment variables from .env.local in project root
load_dotenv(PROJECT_ROOT / '.env.local', override=True)

AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

HEADERS = {
    'Authorization': f'Bearer {AIRTABLE_TOKEN}',
    'Content-Type': 'application/json'
}


def create_record(table_name, fields):
    """Create a record in the specified Airtable table."""
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}'
    payload = {'fields': fields}

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print(f"Error creating record in {table_name}: {response.status_code}")
        print(response.text)
        return None

    return response.json()


def main():
    print("Creating test data in Airtable...")

    # Get selected status and formular
    document_status = DOCUMENT_STATUSES[SELECTED_STATUS]
    formular = FORMULARE[SELECTED_FORMULAR]
    print(f"Document Status: {SELECTED_STATUS} - {document_status}")
    print(f"Formular: {SELECTED_FORMULAR} - {formular['name']}")

    # 1. Create Business Client
    print("\n1. Creating Business Client...")
    business_client = create_record('businesses_clients', {
        'business_name': BUSINESS_NAME,
        'Unternehmensbranche': BUSINESS_BRANCHE
    })

    if not business_client:
        print("Failed to create Business Client. Aborting.")
        return

    business_client_id = business_client['id']
    print(f"   Created Business Client: {business_client_id}")

    # 2. Create Deal linked to Business Client
    print("\n2. Creating Deal...")
    deal = create_record('deals', {
        'deal_name': DEAL_NAME,
        'linked_business': [business_client_id]  # Linked record field expects array
    })

    if not deal:
        print("Failed to create Deal. You may need to manually delete the Business Client.")
        print(f"Business Client ID to delete: {business_client_id}")
        return

    deal_id = deal['id']
    print(f"   Created Deal: {deal_id}")

    # 3. Create Employee/Student linked to Business Client, Deal, and Educational Program
    print("\n3. Creating Employee/Student...")
    employee_student = create_record('employees_students', {
        'first_name': EMPLOYEE_FIRST_NAME,
        'last_name': EMPLOYEE_LAST_NAME,
        'Aktueller Job Titel': EMPLOYEE_JOB_TITLE,
        'work_start_date': EMPLOYEE_WORK_START_DATE,
        'link_to_business': [business_client_id],  # Linked record field expects array
        'link_to_deals': [deal_id],  # Linked record field expects array
        'link_to_educational_programs': [EDUCATIONAL_PROGRAM_ID]  # Existing educational program
    })

    if not employee_student:
        print("Failed to create Employee/Student. You may need to manually delete the other records.")
        print(f"Business Client ID to delete: {business_client_id}")
        print(f"Deal ID to delete: {deal_id}")
        return

    employee_student_id = employee_student['id']
    print(f"   Created Employee/Student: {employee_student_id}")

    # 4. Create Document linked to Employee/Student and Formular
    print("\n4. Creating Document...")
    document = create_record('documents', {
        'employees_students': [employee_student_id],  # Linked record field expects array
        'status': document_status,
        'Formulare 2': [formular['record_id']]  # Linked record field expects array
    })

    if not document:
        print("Failed to create Document. You may need to manually delete the other records.")
        print(f"Business Client ID to delete: {business_client_id}")
        print(f"Employee/Student ID to delete: {employee_student_id}")
        return

    document_id = document['id']
    print(f"   Created Document: {document_id}")

    # 5. Create Application linked to all records
    print("\n5. Creating Application...")
    application = create_record('applications', {
        'application_name': APPLICATION_NAME,
        'application_status': APPLICATION_STATUS,
        'Antrags-Art': ANTRAGS_ART,
        'documents': [document_id],
        'link_to_deals': [deal_id],
        'link_to_students': [employee_student_id],
        'businesses_clients': [business_client_id],
        'link_to_program': [EDUCATIONAL_PROGRAM_ID],
        'application_folder': APPLICATION_FOLDER
    })

    if not application:
        print("Failed to create Application. You may need to manually delete the other records.")
        print(f"Business Client ID to delete: {business_client_id}")
        print(f"Deal ID to delete: {deal_id}")
        print(f"Employee/Student ID to delete: {employee_student_id}")
        print(f"Document ID to delete: {document_id}")
        return

    application_id = application['id']
    print(f"   Created Application: {application_id}")

    # 6. Save IDs to JSON file
    test_data = {
        'business_client_id': business_client_id,
        'deal_id': deal_id,
        'employee_student_id': employee_student_id,
        'document_id': document_id,
        'application_id': application_id,
        'created_at': datetime.now().isoformat()
    }

    with open(TEST_DATA_FILE, 'w') as f:
        json.dump(test_data, f, indent=2)

    print("\n" + "="*50)
    print("Test data created successfully!")
    print("="*50)
    print(f"\nBusiness Client ID: {business_client_id}")
    print(f"Deal ID: {deal_id}")
    print(f"Employee/Student ID: {employee_student_id}")
    print(f"Document ID: {document_id}")
    print(f"Application ID: {application_id}")
    print(f"\nIDs saved to: {TEST_DATA_FILE}")
    print("\nNext steps:")
    print("1. Run your N8N webhook test")
    print("2. Verify the generated documents")
    print("3. Run 'python scripts/tests/delete_test_data.py' to clean up")


if __name__ == '__main__':
    main()
