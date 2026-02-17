"""
Playwright-Skript zum automatischen Ausfüllen des Datenerfassungsformulars.

Voraussetzungen:
    pip install playwright
    playwright install chromium
"""

from playwright.sync_api import sync_playwright, Page
import time

# =============================================================================
# KONFIGURATION
# =============================================================================

FORM_URL = "https://form.foerdernetz-deutschland.de/t/jnYBFipUYnus?deal_id=recEpYxwJ4VmH4GPj&id=recTyvMP0tDrUfuLc"

HEADLESS = False  # True = headless, False = sichtbar

# =============================================================================
# TESTDATEN
# =============================================================================

TEST_DATA = {
    # Persönliche Daten
    "geschlecht": "Herr",               # "Herr", "Frau", "divers, keine Angaben"
    "vorname": "Max",
    "nachname": "Mustermann",
    "telefon": "1711234567",
    "email": "dominique@landeseiten.de",
    "geburtsdatum": "15.01.1985",       # TT.MM.JJJJ

    # Unternehmensdaten
    "firma": "Diminique Testkopf Shcwammkopf",
    "branche": "Automobilindustrie",
    "strasse": "Musterstraße",
    "hausnummer": "123",
    "plz": "10115",
    "ort": "Berlin",
    "bundesland": "Berlin",
    "rechtsform": "GmbH",

    # Mitarbeiterzahlen
    "mitarbeiter_unter_10h": "5",
    "mitarbeiter_10_20h": "10",
    "mitarbeiter_20_30h": "15",
    "mitarbeiter_ueber_30h": "20",

    # Betriebsdaten
    "betriebsnummer_vorhanden": "Nein",
    "betriebsnummer": "",  # Nicht benötigt wenn "Nein"
    "eservice_zugang": "Nein",
    "betriebsvereinbarung": "Nein",

    # Bankdaten
    "iban": "DE89370400440532013000",
    "bic": "COBADEFFXXX",
    "bank_name": "Commerzbank Berlin",

    "agb_akzeptiert": True,

    # Mitarbeiter-Subformular (mindestens 1 erforderlich)
    "mitarbeiter": [
        {
            "geschlecht": "Herr",
            "vorname": "Test",
            "nachname": "Schwammkopf",
            "geburtsname": "",
            "geburtsort": "München",
            "geburtsdatum": "10.05.1990",
            "nationalitaet": "Deutschland",
            "sozialversicherungsnr": "12 100590 M 003",
            "schwerbehinderung": "Nein",
            "strasse": "Test Weg",
            "hausnummer": "42",
            "plz": "80331",
            "ort": "München",
            "telefon": "1761234567",
            "email": "dominique@landeseiten.de",
            "beschaeftigung_beginn": "01.01.2020",
            "arbeitszeit_woche": "40",
            "arbeitstage": "Montag, Dienstag, Mittwoch, Donnerstag, Freitag",
            "arbeitszeit_1_von": "08:00",
            "arbeitszeit_1_bis": "12:00",
            "arbeitszeit_2_von": "13:00",
            "arbeitszeit_2_bis": "17:00",
            "gehaltsform": "Monatsgehalt",
            "arbeitsentgelt": "3500",
            "verguetung_ist": "ortsüblich",
            "kurzarbeitergeld": "Nein",
            "befristet": "Nein",
            "befristete_arbeitserlaubnis": "Nein",
            "jobtitel": "Softwareentwickler",
            "taetigkeitsbeschreibung": "Entwicklung von Automatisierungsskripten und Webanwendungen.",
            "mehr_als_4_jahre": "Nein",
            "ausbildung_vorhanden": "Nein",
            "kostenuebernahme_dritter": "Nein",
            "fortbestand_arbeitsverhaeltnis": "Ja",
            "freistellung_bescheinigt": "Ja",
            "bedarfsgemeinschaft": "Nein",
            "bildungsgutschein": "Nein",
            "eingliederungszuschuss": "Nein",
            "weiterbildung": "Arbeitswelt 5.0",
            "foerderung_start": "01.04.2026",
            "ausbildung": "Fachinformatiker",
            "familienstand": "ledig",
            "arbeitsvertrag_pfad": "TEST.pdf",
        }
    ]
}


# =============================================================================
# HILFSFUNKTIONEN
# =============================================================================

def fill_by_aria(page: Page, aria_label: str, value: str):
    """Füllt Input per aria-label."""
    if not value:
        return
    try:
        page.fill(f'input[aria-label="{aria_label}"]', value)
        print(f"  [OK] {aria_label}")
    except Exception as e:
        print(f"  [FEHLER] {aria_label}: {e}")


def fill_by_partial_aria(page: Page, partial: str, value: str):
    """Füllt Input per partiellem aria-label."""
    if not value:
        return
    try:
        page.fill(f'input[aria-label*="{partial}"]', value)
        print(f"  [OK] {partial}")
    except Exception as e:
        print(f"  [FEHLER] {partial}: {e}")


def click_radio(page: Page, option_text: str):
    """Klickt Radio-Option (für einfache Felder wie Geschlecht)."""
    try:
        page.locator(f'[role="radio"]:has-text("{option_text}"), label:has-text("{option_text}")').first.click()
        print(f"  [OK] Radio: {option_text}")
    except Exception:
        try:
            page.locator(f'div:text-is("{option_text}"), span:text-is("{option_text}")').first.click()
            print(f"  [OK] Radio: {option_text}")
        except Exception as e:
            print(f"  [FEHLER] Radio '{option_text}': {e}")


def click_radio_for_question(page: Page, question_text: str, answer: str):
    """Klickt Ja/Nein für eine spezifische Frage via radiogroup."""
    try:
        # Finde die radiogroup deren Label den Fragetext enthält
        radiogroups = page.locator('[role="radiogroup"]').all()
        for rg in radiogroups:
            # Hole das Label per JavaScript
            label_text = rg.evaluate('''el => {
                const labelId = el.getAttribute("aria-labelledby");
                if (labelId) {
                    const label = document.getElementById(labelId);
                    return label ? label.innerText : "";
                }
                return "";
            }''')

            if question_text.lower() in label_text.lower():
                # Gefunden! Klicke die richtige Option
                option = rg.locator(f'[role="radio"]:has-text("{answer}")').first
                option.click()
                print(f"  [OK] {question_text[:40]}... -> {answer}")
                return

        print(f"  [WARNUNG] Frage '{question_text[:40]}...' nicht gefunden")
    except Exception as e:
        print(f"  [FEHLER] {question_text[:40]}...: {e}")


def select_react_dropdown(page: Page, aria_label: str, option_text: str):
    """Wählt Option in React-Select Dropdown per JavaScript."""
    try:
        # Finde das Input und klicke es an
        input_selector = f'input[aria-label="{aria_label}"]'
        page.click(input_selector)

        # Tippe die Option und drücke Enter
        page.fill(input_selector, option_text)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        print(f"  [OK] Dropdown: {aria_label}")
    except Exception as e:
        print(f"  [FEHLER] Dropdown '{aria_label}': {e}")


def fill_mitarbeiter_subform(page: Page, mitarbeiter: dict):
    """Füllt das Mitarbeiter-Subformular im iframe aus."""
    iframe = page.frame_locator('iframe[title="Create record form"]')

    def fill_text(aria_label, key):
        value = mitarbeiter.get(key, "")
        if value:
            try:
                # Scroll element into view with timeout
                el = iframe.locator(f'[aria-label="{aria_label}"], [aria-label*="{aria_label}"]').first
                el.scroll_into_view_if_needed(timeout=5000)
                el.fill(value)
                print(f"    [OK] {aria_label}")
            except Exception as e:
                print(f"    [FEHLER] {aria_label}: {e}")

    def fill_date(aria_label, key):
        value = mitarbeiter.get(key, "")
        if value:
            try:
                parts = value.split(".")
                if len(parts) == 3:
                    us_date = f"{parts[1]}/{parts[0]}/{parts[2]}"
                    date_input = iframe.locator(f'input[aria-label*="{aria_label}"]').first
                    # Warte kürzer, falls das Feld noch nicht da ist
                    date_input.wait_for(state="visible", timeout=3000)
                    date_input.scroll_into_view_if_needed()
                    date_input.click()
                    page.keyboard.type(us_date)
                    page.keyboard.press("Escape")
                    print(f"    [OK] {aria_label}")
            except Exception as e:
                print(f"    [FEHLER] {aria_label}: {e}")

    def fill_dropdown(aria_label, key):
        """Füllt ein React-Select Dropdown im iframe robust aus (unterstützt Multi-Select)."""
        value = mitarbeiter.get(key, "")
        if value:
            try:
                # Finde das Input-Feld (React-Select nutzt oft ein verstecktes Input für die Suche)
                input_el = iframe.locator(f'input[aria-label*="{aria_label}"]').first
                input_el.scroll_into_view_if_needed()
                
                # Splitte den Wert für Multi-Select (z.B. "Montag, Dienstag")
                options = [o.strip() for o in value.split(",")]
                
                for opt in options:
                    # Klick, um Fokus zu setzen und Dropdown zu öffnen
                    input_el.click()
                    page.wait_for_timeout(500)
                    
                    # Tippe den Wert Buchstabe für Buchstabe
                    page.keyboard.type(opt, delay=50)
                    page.wait_for_timeout(500)
                    
                    # Mit Enter bestätigen
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(300)
                
                # Schließe das Dropdown (besonders wichtig bei Multi-Select)
                page.keyboard.press("Escape")
                print(f"    [OK] Dropdown: {aria_label}")
            except Exception as e:
                print(f"    [FEHLER] Dropdown {aria_label}: {e}")

    def click_radio(text):
        try:
            rb = iframe.locator(f'[role="radio"]:has-text("{text}")').first
            rb.scroll_into_view_if_needed()
            rb.click()
            print(f"    [OK] Radio: {text}")
        except Exception:
            pass

    def select_airtable_option(label_text, value):
        """Spezialisierte Logik für Felder mit '+ Hinzufügen' Button (Airtable-Anbindung)."""
        if not value:
            return
        try:
            # Finde den Button im Kontext des Labels
            print(f"    [INFO] Suche Airtable-Option: {value}")
            add_button = iframe.locator(f'div:has(> p:has-text("{label_text}")) >> button:has-text("Hinzufügen")').first
            if not add_button.count():
                # Fallback: Suche global nach dem nächsten Button nach dem Label
                add_button = iframe.locator(f'button:has-text("Hinzufügen")').first
            
            add_button.scroll_into_view_if_needed()
            add_button.click()
            
            # Warte auf das Suchfeld
            search_input = iframe.locator('input[placeholder*="Search"]').first
            search_input.wait_for(state="visible", timeout=5000)
            search_input.fill(value)
            page.wait_for_timeout(1000)
            
            # Klicke das Ergebnis (suche nach dem Textteil, um robust zu sein)
            print(f"    [INFO] Klicke Ergebnis für: {value}")
            result = iframe.locator(f'div:has-text("{value}")').last
            
            result.scroll_into_view_if_needed()
            result.click()
            print(f"    [OK] Airtable Selection: {label_text} -> {value}")
        except Exception as e:
            print(f"    [FEHLER] Airtable Selection {label_text}: {e}")
            # Optional: Fallback - Klicke das erste gefundene Element in der Liste
            try:
                iframe.locator('.sc-c43922eb-0').first.click()
                print(f"    [OK] Fallback: Erste verfügbare Option gewählt")
            except:
                pass

    def select_plus_date(label_text, key):
        """Spezialisierte Logik für Datumsfelder mit '+ Startdatum hinzufügen'."""
        value = mitarbeiter.get(key, "")
        if not value:
            return
        try:
            print(f"    [INFO] Suche Startdatum: {value}")
            add_button = iframe.locator('button:has-text("Startdatum hinzufügen")').first

            if add_button.count() > 0:
                add_button.scroll_into_view_if_needed()
                add_button.click()

            # Warte bis die Liste mit Daten geladen ist
            page.wait_for_timeout(2000)

            # Erstelle verschiedene Datums-Formate zum Suchen
            # Input: "01.03.2026" -> suche nach "1.3.", "01.03.", "1.3.2026", etc.
            parts = value.split(".")
            if len(parts) == 3:
                day = parts[0].lstrip("0") or "0"
                month = parts[1].lstrip("0") or "0"
                year = parts[2]

                # Verschiedene mögliche Formate
                date_formats = [
                    f"{day}.{month}.",           # "1.3."
                    f"{day}.{month}.{year}",     # "1.3.2026"
                    f"{parts[0]}.{parts[1]}.",   # "01.03."
                    value,                        # "01.03.2026"
                ]
            else:
                date_formats = [value]

            # Suche das Datum in der Liste und klicke darauf
            clicked = False
            for date_format in date_formats:
                print(f"    [INFO] Suche nach Format: {date_format}")
                result = iframe.locator(f'div:has-text("{date_format}")').last
                if result.count() > 0:
                    result.scroll_into_view_if_needed()
                    result.click()
                    print(f"    [OK] Startdatum: {date_format}")
                    clicked = True
                    break

            if not clicked:
                # Fallback: Klicke das erste Element in der Liste
                print(f"    [WARNUNG] Datum nicht gefunden, wähle erstes verfügbares")
                first_option = iframe.locator('[role="option"], [role="listitem"], .sc-c43922eb-0').first
                if first_option.count() > 0:
                    first_option.click()
                    print(f"    [OK] Erstes verfügbares Datum gewählt")

        except Exception as e:
            print(f"    [FEHLER] Startdatum: {e}")

    # Geschlecht & Familienstand
    click_radio(mitarbeiter.get("geschlecht", "Herr"))
    click_radio(mitarbeiter.get("familienstand", "ledig"))

    def upload_file(aria_label, key):
        """Lädt eine Datei im iframe hoch."""
        path = mitarbeiter.get(key, "")
        if path:
            try:
                # Suche nach dem Datei-Input. Airtable/React-Formulare nutzen oft ein verstecktes Input.
                # Wir suchen nach einem Input vom Typ File.
                file_input = iframe.locator('input[type="file"]').first
                file_input.set_input_files(path)
                print(f"    [OK] Datei hochgeladen: {aria_label}")
            except Exception as e:
                print(f"    [FEHLER] Datei-Upload {aria_label}: {e}")

    # Textfelder
    fill_text("Vorname", "vorname")
    fill_text("Nachname", "nachname")
    fill_text("Geburtsname", "geburtsname")
    fill_text("Geburtsort", "geburtsort")
    fill_text("Wie lautet deine Sozialversicherung-Nr.?", "sozialversicherungsnr")
    fill_text("Straße", "strasse")
    fill_text("Hausnummer", "hausnummer")
    fill_text("PLZ", "plz")
    fill_text("Ort", "ort")
    fill_text("Telefonnummer", "telefon")
    fill_text("Email Adresse", "email")
    fill_text("Arbeitszeit pro Woche", "arbeitszeit_woche")
    fill_text("Arbeitsentgelt", "arbeitsentgelt")
    fill_text("Jobtitel", "jobtitel")

    # Textareas
    try:
        taetigkeit = mitarbeiter.get("taetigkeitsbeschreibung", "")
        if taetigkeit:
            ta = iframe.locator('textarea[aria-label*="Beschreibe, welche Tätigkeit"]').first
            ta.scroll_into_view_if_needed()
            ta.fill(taetigkeit)
            print("    [OK] Tätigkeitsbeschreibung")
    except Exception as e:
        print(f"    [FEHLER] Tätigkeitsbeschreibung: {e}")

    # Dropdown-Felder (React-Select / Combobox)
    fill_dropdown("Nationalität", "nationalitaet")
    fill_dropdown("Arbeitstage", "arbeitstage")
    fill_dropdown("Arbeitszeit 1 von", "arbeitszeit_1_von")
    fill_dropdown("Arbeitszeit 1 bis", "arbeitszeit_1_bis")
    fill_dropdown("Arbeitszeit 2 von", "arbeitszeit_2_von")
    fill_dropdown("Arbeitszeit 2 bis", "arbeitszeit_2_bis")
    
    # Airtable & Spezielle Buttons
    select_airtable_option("Welche Weiterbildung wird der Mitarbeiter besuchen?", mitarbeiter.get("weiterbildung"))

    # Datumsfelder
    fill_date("Geburtsdatum", "geburtsdatum")
    fill_date("Beginn des Beschäftigungsverhältnisses (TT.MM.JJJJ)", "beschaeftigung_beginn")
    select_plus_date("Zu welchem Datum soll der Mitarbeiter in die Förderung gehen?", "foerderung_start")

    # Radio-Buttons (Allgemein)
    click_radio(mitarbeiter.get("gehaltsform", "Monatsgehalt"))
    click_radio(mitarbeiter.get("verguetung_ist", "ortsüblich"))
    click_radio(mitarbeiter.get("kurzarbeitergeld", "Nein"))
    
    # Neue Radio-Fragen
    click_radio_for_question(iframe, "mehr als 4 Jahre", mitarbeiter.get("mehr_als_4_jahre", "Nein"))
    
    # Befristete Verhältnisse (Nein aus Screenshot)
    click_radio_for_question(iframe, "Befristetes Arbeitsverhältnis", mitarbeiter.get("befristet", "Nein"))
    click_radio_for_question(iframe, "Befristete Arbeitserlaubnis", mitarbeiter.get("befristete_arbeitserlaubnis", "Nein"))

    # Ausbildung
    click_radio_for_question(iframe, "Abgeschlossene Ausbildung", mitarbeiter.get("ausbildung_vorhanden", "Ja"))
    if mitarbeiter.get("ausbildung_vorhanden") == "Ja":
        page.wait_for_timeout(1000) # Warten bis Feld erscheint
        fill_dropdown("Ausbildung / Studium", "ausbildung")
        
    click_radio_for_question(iframe, "Übernahme der Weiterbildungskosten", mitarbeiter.get("kostenuebernahme_dritter", "Nein"))
    click_radio_for_question(iframe, "fortbestehen", mitarbeiter.get("fortbestand_arbeitsverhaeltnis", "Ja"))
    click_radio_for_question(iframe, "freigestellt", mitarbeiter.get("freistellung_bescheinigt", "Ja"))
    click_radio_for_question(iframe, "Bedarfsgemeinschaft", mitarbeiter.get("bedarfsgemeinschaft", "Nein"))
    click_radio_for_question(iframe, "Bildungsgutschein", mitarbeiter.get("bildungsgutschein", "Nein"))
    click_radio_for_question(iframe, "Eingliederungszuschuss", mitarbeiter.get("eingliederungszuschuss", "Nein"))

    # Datei hochladen (Arbeitsvertrag)
    upload_file("Aktueller Arbeitsvertrag", "arbeitsvertrag_pfad")

    # Warte bis der Upload abgeschlossen ist
    print("    [INFO] Warte auf Datei-Upload...")
    page.wait_for_timeout(5000)

    # Checkboxen
    if mitarbeiter.get("schwerbehinderung") == "Ja":
        try:
            cb = iframe.locator('button[role="checkbox"]').first
            cb.scroll_into_view_if_needed()
            cb.click()
            print("    [OK] Schwerbehinderung")
        except Exception:
            pass

    # Einreichen (mit Retry falls Upload noch nicht fertig war)
    try:
        btn = iframe.locator('button:has-text("Einreichen")').first
        btn.scroll_into_view_if_needed()
        btn.click()
        print(f"    [INFO] Erster Klick auf Einreichen...")
        page.wait_for_timeout(3000)

        # Prüfe ob das Modal noch da ist (z.B. wegen Upload-Fehler)
        # Falls ja, nochmal klicken
        if iframe.locator('button:has-text("Einreichen")').count() > 0:
            print(f"    [INFO] Modal noch offen, versuche erneut...")
            btn = iframe.locator('button:has-text("Einreichen")').first
            btn.click()
            page.wait_for_timeout(2000)

        print(f"    [OK] Mitarbeiter eingereicht")
        try:
            page.wait_for_selector('iframe[title="Create record form"]', state="hidden", timeout=5000)
        except Exception:
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
    except Exception as e:
        print(f"    [FEHLER] Einreichen: {e}")


# =============================================================================
# HAUPTFUNKTION
# =============================================================================

def fill_form():
    print("=" * 50)
    print("FORMULAR-AUSFÜLLER")
    print("=" * 50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(viewport={"width": 1400, "height": 900}, locale="de-DE")
        page = context.new_page()

        # Formular laden
        print("[1/10] Lade Formular...")
        page.goto(FORM_URL)
        page.wait_for_load_state("networkidle")

        # Start klicken
        print("[2/10] Starte Formular...")
        page.click('button:has-text("Start")')
        page.wait_for_load_state("networkidle")

        # Persönliche Daten
        print("[3/10] Persönliche Daten...")
        click_radio(page, TEST_DATA["geschlecht"])
        fill_by_aria(page, "Vorname Ansprechpartner", TEST_DATA["vorname"])
        fill_by_aria(page, "Nachname", TEST_DATA["nachname"])
        fill_by_aria(page, "Telefonnummer", TEST_DATA["telefon"])
        fill_by_aria(page, "Email-Adresse", TEST_DATA["email"])

        # Geburtsdatum (readonly DatePicker - per Klick + Keyboard)
        if TEST_DATA.get("geburtsdatum"):
            try:
                parts = TEST_DATA["geburtsdatum"].split(".")
                if len(parts) == 3:
                    us_date = f"{parts[1]}/{parts[0]}/{parts[2]}"
                    date_input = page.locator('input[aria-label="Geburtsdatum"]')
                    date_input.click()
                    page.keyboard.type(us_date)
                    page.keyboard.press("Escape")
                    print(f"  [OK] Geburtsdatum")
            except Exception as e:
                print(f"  [FEHLER] Geburtsdatum: {e}")

        # Unternehmensdaten
        print("[4/10] Unternehmensdaten...")
        fill_by_aria(page, "Name des Unternehmens", TEST_DATA["firma"])
        select_react_dropdown(page, "Unternehmensbranche", TEST_DATA["branche"])
        fill_by_aria(page, "Straße", TEST_DATA["strasse"])
        fill_by_aria(page, "Hausnummer", TEST_DATA["hausnummer"])
        fill_by_aria(page, "PLZ", TEST_DATA["plz"])
        fill_by_aria(page, "Ort", TEST_DATA["ort"])
        select_react_dropdown(page, "Bundesland", TEST_DATA["bundesland"])
        select_react_dropdown(page, "Rechtsform", TEST_DATA["rechtsform"])

        # Mitarbeiterzahlen
        print("[5/10] Mitarbeiterzahlen...")
        fill_by_partial_aria(page, "10 Stunden pro Woche", TEST_DATA["mitarbeiter_unter_10h"])
        fill_by_partial_aria(page, "10-20 Stunden", TEST_DATA["mitarbeiter_10_20h"])
        fill_by_partial_aria(page, "20-30 Stunden", TEST_DATA["mitarbeiter_20_30h"])
        fill_by_partial_aria(page, "mehr als 30 Stunden", TEST_DATA["mitarbeiter_ueber_30h"])

        # Betriebsdaten
        print("[6/10] Betriebsdaten...")
        click_radio_for_question(page, "Betriebsnummer vorhanden", TEST_DATA["betriebsnummer_vorhanden"])
        if TEST_DATA["betriebsnummer_vorhanden"] == "Ja":
            page.wait_for_selector('input[aria-label*="Betriebsnummer"]', timeout=3000)
            fill_by_partial_aria(page, "Betriebsnummer", TEST_DATA["betriebsnummer"])

        click_radio_for_question(page, "E-Service Zugang", TEST_DATA["eservice_zugang"])
        click_radio_for_question(page, "Betriebsvereinbarung", TEST_DATA["betriebsvereinbarung"])

        # Bankdaten
        print("[7/10] Bankdaten...")
        fill_by_partial_aria(page, "IBAN", TEST_DATA["iban"])
        fill_by_partial_aria(page, "BIC", TEST_DATA["bic"])
        fill_by_partial_aria(page, "Kreditinstitut", TEST_DATA["bank_name"])

        # Mitarbeiter-Subformular
        print("[8/10] Mitarbeiter anlegen...")
        if TEST_DATA.get("mitarbeiter"):
            for i, mitarbeiter in enumerate(TEST_DATA["mitarbeiter"]):
                print(f"  Mitarbeiter {i+1}:")
                # Scroll und klicke "Mitarbeiter anlegen"
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.click('button:has-text("Mitarbeiter anlegen")')
                page.wait_for_timeout(3000)  # Warte auf iframe

                # Fülle das Subformular
                fill_mitarbeiter_subform(page, mitarbeiter)

                # Warte auf Schließen des Modals
                page.wait_for_timeout(3000)
                # Stelle sicher, dass das Modal geschlossen ist
                try:
                    page.wait_for_selector('[role="dialog"]', state="hidden", timeout=5000)
                except Exception:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(1000)

        # AGB (ist ein Button mit role="checkbox", kein normales Input)
        print("[9/10] AGB...")
        if TEST_DATA.get("agb_akzeptiert"):
            try:
                # Scroll zum AGB-Bereich
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                # AGB-Checkbox ist ein Button mit role="checkbox"
                agb_checkbox = page.locator('button[role="checkbox"]').first
                agb_checkbox.click()
                print("  [OK] AGB akzeptiert")
            except Exception as e:
                print(f"  [FEHLER] AGB: {e}")

        # Scroll nach unten zum Absenden-Button
        print("[10/10] Absenden...")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)

        absenden_btn = page.locator('button:has-text("Absenden")').first
        if absenden_btn.count() > 0:
            absenden_btn.scroll_into_view_if_needed()
            absenden_btn.click()
            print("  [INFO] Klick auf Absenden...")
        else:
            print("  [FEHLER] Absenden-Button nicht gefunden!")

        # Warte auf Bestätigung
        print("  [INFO] Warte auf Bestätigung...")
        page.wait_for_timeout(5000)

        # Prüfe ob eine Erfolgsmeldung erscheint
        page_content = page.content()
        if "Vielen Dank" in page_content or "erfolgreich" in page_content.lower() or "Thank you" in page_content:
            print("  [OK] Erfolgsmeldung gefunden!")
        else:
            print("  [WARNUNG] Keine Erfolgsmeldung gefunden. Prüfe manuell.")
            # Warte noch länger, damit man sehen kann was passiert ist
            page.wait_for_timeout(5000)

        print()
        print("=" * 50)
        print("FERTIG!")
        print("=" * 50)

        if not HEADLESS:
            print("Formular wurde verarbeitet. Browser bleibt 10 Sekunden offen...")
            page.wait_for_timeout(10000)

        browser.close()


if __name__ == "__main__":
    fill_form()
