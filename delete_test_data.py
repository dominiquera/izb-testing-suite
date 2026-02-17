#!/usr/bin/env python3
"""
Delete test data from Airtable that was created by create_test_data.py.

Usage:
    python scripts/tests/delete_test_data.py

This script reads the record IDs from test_data_ids.json and deletes
only those specific records. It will NOT delete any other data.
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory (2 levels up from this script)
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


def delete_record(table_name, record_id):
    """Delete a record from the specified Airtable table."""
    url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_name}/{record_id}'

    response = requests.delete(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error deleting record {record_id} from {table_name}: {response.status_code}")
        print(response.text)
        return False

    return True


def main():
    # Check if test_data_ids.json exists
    if not TEST_DATA_FILE.exists():
        print(f"No {TEST_DATA_FILE} found.")
        print("Either no test data was created, or it was already deleted.")
        return

    # Load the IDs
    with open(TEST_DATA_FILE, 'r') as f:
        test_data = json.load(f)

    print("Deleting test data from Airtable...")
    print(f"Created at: {test_data.get('created_at', 'unknown')}")

    # 1. Delete Application first (because it links to everything)
    print("\n1. Deleting Application...")
    application_id = test_data.get('application_id')
    if application_id:
        if delete_record('applications', application_id):
            print(f"   Deleted: {application_id}")
        else:
            print(f"   Failed to delete: {application_id}")

    # 2. Delete Document (because it's linked to Employee/Student)
    print("\n2. Deleting Document...")
    document_id = test_data.get('document_id')
    if document_id:
        if delete_record('documents', document_id):
            print(f"   Deleted: {document_id}")
        else:
            print(f"   Failed to delete: {document_id}")

    # 3. Delete Employee/Student (because it's linked to Deal and Business Client)
    print("\n3. Deleting Employee/Student...")
    employee_id = test_data.get('employee_student_id')
    if employee_id:
        if delete_record('employees_students', employee_id):
            print(f"   Deleted: {employee_id}")
        else:
            print(f"   Failed to delete: {employee_id}")

    # 4. Delete Deal (because it's linked to Business Client)
    print("\n4. Deleting Deal...")
    deal_id = test_data.get('deal_id')
    if deal_id:
        if delete_record('deals', deal_id):
            print(f"   Deleted: {deal_id}")
        else:
            print(f"   Failed to delete: {deal_id}")

    # 5. Delete Business Client
    print("\n5. Deleting Business Client...")
    business_id = test_data.get('business_client_id')
    if business_id:
        if delete_record('businesses_clients', business_id):
            print(f"   Deleted: {business_id}")
        else:
            print(f"   Failed to delete: {business_id}")

    # 6. Remove the JSON file
    TEST_DATA_FILE.unlink()

    print("\n" + "="*50)
    print("Test data cleanup complete!")
    print("="*50)


if __name__ == '__main__':
    main()
