#!/usr/bin/env python3
"""
Script to fetch leads from Close CRM by email address or lead ID.
"""

import argparse
import os
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()

CLOSE_API_KEY = os.getenv("CLOSE_API_KEY")
BASE_URL = "https://api.close.com/api/v1"


def get_lead_by_id(lead_id: str) -> Optional[dict]:
    """Fetch a single lead from Close CRM by its ID."""

    headers = {
        "Authorization": CLOSE_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(f"{BASE_URL}/lead/{lead_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def search_leads_by_email(email: str) -> list:
    """Search for leads in Close CRM that contain the given email address."""

    headers = {
        "Authorization": CLOSE_API_KEY,
        "Content-Type": "application/json"
    }

    # Use Close's search endpoint with email query
    search_url = f"{BASE_URL}/lead/"
    params = {
        "query": f'email:"{email}"',
        "_limit": 100
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []


def display_leads(leads: list, search_email: str):
    """Display lead information in a readable format."""

    if not leads:
        print(f"\nKeine Leads mit E-Mail '{search_email}' gefunden.")
        return

    print(f"\n{'='*60}")
    print(f"Gefundene Leads mit E-Mail: {search_email}")
    print(f"{'='*60}")

    for i, lead in enumerate(leads, 1):
        print(f"\n--- Lead {i} ---")
        print(f"ID:          {lead.get('id')}")
        print(f"Name:        {lead.get('display_name')}")
        print(f"Status:      {lead.get('status_label')}")
        print(f"URL:         https://app.close.com/lead/{lead.get('id')}")

        # Show contacts
        contacts = lead.get("contacts", [])
        if contacts:
            print(f"Kontakte:")
            for contact in contacts:
                name = contact.get("name", "N/A")
                emails = [e.get("email") for e in contact.get("emails", [])]
                phones = [p.get("phone") for p in contact.get("phones", [])]
                print(f"  - {name}")
                if emails:
                    print(f"    E-Mails: {', '.join(emails)}")
                if phones:
                    print(f"    Telefon: {', '.join(phones)}")

        # Show custom fields if present
        if lead.get("custom"):
            print(f"Custom Fields: {lead.get('custom')}")

    print(f"\n{'='*60}")
    print(f"Insgesamt {len(leads)} Lead(s) gefunden.")


def display_single_lead(lead: Optional[dict], lead_id: str):
    """Display a single lead's information."""

    if not lead:
        print(f"\nKein Lead mit ID '{lead_id}' gefunden.")
        return

    print(f"\n{'='*60}")
    print(f"Lead Details")
    print(f"{'='*60}")
    print(f"ID:          {lead.get('id')}")
    print(f"Name:        {lead.get('display_name')}")
    print(f"Status:      {lead.get('status_label')}")
    print(f"URL:         https://app.close.com/lead/{lead.get('id')}")

    # Show contacts
    contacts = lead.get("contacts", [])
    if contacts:
        print(f"Kontakte:")
        for contact in contacts:
            name = contact.get("name", "N/A")
            emails = [e.get("email") for e in contact.get("emails", [])]
            phones = [p.get("phone") for p in contact.get("phones", [])]
            print(f"  - {name}")
            if emails:
                print(f"    E-Mails: {', '.join(emails)}")
            if phones:
                print(f"    Telefon: {', '.join(phones)}")

    # Show custom fields if present
    if lead.get("custom"):
        print(f"Custom Fields: {lead.get('custom')}")

    print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch leads from Close CRM by email or lead ID."
    )
    parser.add_argument(
        "--email", "-e",
        help="Search leads by email address"
    )
    parser.add_argument(
        "--id", "-i",
        help="Get a specific lead by its ID (e.g., lead_bEXAJYCK...)"
    )

    args = parser.parse_args()

    if args.id:
        print(f"Hole Lead mit ID: {args.id}")
        lead = get_lead_by_id(args.id)
        display_single_lead(lead, args.id)
    elif args.email:
        print(f"Suche nach Leads mit E-Mail: {args.email}")
        leads = search_leads_by_email(args.email)
        display_leads(leads, args.email)
    else:
        parser.print_help()
        print("\nBeispiele:")
        print("  python get_close_leads.py --email dominique@landeseiten.de")
        print("  python get_close_leads.py --id lead_bEXAJYCKzFoH7uorF0c3LPwQ4x6X6SgTk6GpptKwz8q")
