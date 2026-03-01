# Smart Customer Support (Prototype)

This repository contains a lightweight implementation of a **Smart Customer Support** system covering the requested needs:

## Functionalities implemented
- Smart assignment of tickets to support agents based on:
  - skill match (problem category)
  - solved ticket history
  - review score
  - current workload
- Prioritization based on severity prediction from ticket text and a computed priority score.
- Customer feedback handling to continuously update agent performance score.
- A simple web dashboard (`web/index.html`) for presentation.

## Project structure
- `support_system/` — core logic for NLP, assignment, and feedback.
- `data/` — sample dataset for agents and tickets.
- `tests/` — unit tests.
- `web/` — static dashboard page.
- `app.py` — command-line demo that processes sample tickets.

## Dataset
Sample dataset is included in:
- `data/agents.json`
- `data/tickets.json`

You can replace these with production datasets exported from your CRM/helpdesk.

## NLP model
The prototype uses a deterministic keyword-based NLP baseline:
- `predict_severity(text)`
- `predict_category(text)`
- `compute_priority(severity, sentiment_hint)`
- `predict_ticket_labels(text)`

This keeps the system simple and explainable. In production, replace with:
- fine-tuned transformer classifiers (category + severity)
- historical ticket labels
- periodic retraining pipeline

## Run
```bash
python3 app.py
```

Optional export:
```bash
python3 app.py --export data/processed_tickets.json
```

## Test
```bash
python3 -m unittest discover -s tests -v
```

## Next upgrades
1. Connect to ticketing API providers (Zendesk/Freshdesk/JSM).
2. Persist tickets/agents/feedback in a relational database.
3. Build interactive dashboard with filtering and SLA tracking.
4. Add authentication + role-based access.
5. Add active-learning loop from agent corrections.
