
# Solance Workflow Service (Python/Flask)

This service simulates a lightweight backend for processing customer operations like registration, account opening, deposits, and payments.

## Features

- Flask REST API
- In-memory persistence
- Clean, testable design
- Sample unit tests with `pytest`

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

## Run Tests

```bash
pytest
```

## API Endpoints

- `POST /workflow/register`
- `POST /workflow/account`
- `POST /workflow/deposit`
- `POST /workflow/payment`
- `GET /workflow/messages`

## Deployment

Use Docker or deploy as a Flask app in AWS (via Fargate, Lambda using Zappa, or EC2).

## AI Tooling Plan

See `ai_tooling_strategy.md`.
