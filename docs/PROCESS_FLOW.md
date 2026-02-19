# Prozessübersicht

## Gesamtablauf

```mermaid
flowchart TD
    subgraph prod["Produktiver Ablauf"]
        P1["1. Applikationsformular ausgefüllt"]
        P2["2. Dokumente/Business-Daten anlegen"]
        P3["3. Close #11: PandaDoc Vertrag erstellen"]
        P4["4. Kunde unterschreibt PandaDoc"]
        P5["5. Make: QCG Auftrag starten"]
        P6["6. Ordner werden erstellt"]
        P7["7. Weiterleitung an MANAVA"]
        P8["8. Kursfreigabe bei Startdatum"]

        P1 --> P2 --> P3 --> P4 --> P5 --> P6 --> P7 --> P8
    end

    subgraph test["Test-Simulation"]
        T1["create_test_data.py"]
        T2["fill_form.py"]
        T3["trigger_document_creation.py"]
        T4["simulate_pandadoc_signed.py"]
        T5["forward_to_manava.py"]
        T6["activate_courses_on_start_date.py"]
        T7["delete_test_data.py"]

        T1 --> T2 --> T3 --> T4 --> T5 --> T6 --> T7
    end

    prod -.->|"simuliert durch"| test
```

## Datenfluss

```mermaid
flowchart LR
    subgraph airtable["Airtable"]
        BIZ[businesses_clients]
        DEAL[deals]
        EMP[employees_students]
        DOC[documents]
        APP[applications]
    end

    subgraph external["Externe Systeme"]
        CLOSE[Close CRM]
        PANDA[PandaDoc]
        MAKE[Make.com]
        N8N[N8N]
        GDRIVE[Google Drive]
        MANAVA[MANAVA Kurs-System]
    end

    BIZ --> DEAL --> EMP --> DOC --> APP
    APP --> N8N
    CLOSE --> PANDA
    PANDA --> MAKE
    MAKE --> GDRIVE
    EMP --> N8N --> MANAVA
    N8N --> GDRIVE
```

## Skript-Zuordnung

| Produktions-Schritt | Test-Skript | Beschreibung |
|---------------------|-------------|--------------|
| Applikationsformular | `fill_form.py` | Füllt das Formular automatisch aus |
| Daten anlegen | `create_test_data.py` | Erstellt Testdaten in Airtable |
| Dokumente generieren | `trigger_document_creation.py` | Triggert N8N Webhook |
| PandaDoc unterschrieben | `simulate_pandadoc_signed.py` | Simuliert Webhook-Event |
| Weiterleitung an MANAVA | `forward_to_manava.py` | Sendet Daten an MANAVA, erstellt PandaDoc für Schulungsrichtlinien |
| Kursfreigabe | `activate_courses_on_start_date.py` | Automatische Freigabe bei Startdatum |
| Aufräumen | `delete_test_data.py` | Löscht Testdaten |
