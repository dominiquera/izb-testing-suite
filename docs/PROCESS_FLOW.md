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

        P1 --> P2 --> P3 --> P4 --> P5 --> P6
    end

    subgraph test["Test-Simulation"]
        T1["create_test_data.py"]
        T2["fill_form.py"]
        T3["trigger_document_creation.py"]
        T4["simulate_pandadoc_signed.py"]
        T5["delete_test_data.py"]

        T1 --> T2 --> T3 --> T4 --> T5
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
    end

    BIZ --> DEAL --> EMP --> DOC --> APP
    APP --> N8N
    CLOSE --> PANDA
    PANDA --> MAKE
    MAKE --> GDRIVE
```

## Skript-Zuordnung

| Produktions-Schritt | Test-Skript | Beschreibung |
|---------------------|-------------|--------------|
| Applikationsformular | `fill_form.py` | Füllt das Formular automatisch aus |
| Daten anlegen | `create_test_data.py` | Erstellt Testdaten in Airtable |
| Dokumente generieren | `trigger_document_creation.py` | Triggert N8N Webhook |
| PandaDoc unterschrieben | `simulate_pandadoc_signed.py` | Simuliert Webhook-Event |
| Aufräumen | `delete_test_data.py` | Löscht Testdaten |
