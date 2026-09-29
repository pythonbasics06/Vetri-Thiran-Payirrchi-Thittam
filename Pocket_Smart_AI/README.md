# PocketSmart AI

A complete FastAPI + Jinja2 + Gemini application based on the supplied PocketSmart AI project documentation.

## Features

- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit image
- Gemini multimodal recommendations
- Budget allocation and budget validation
- Platform-aware shopping/service links
- User registration/login/logout with JWT
- Recommendation history
- Dashboard
- AI fallback mode when no Gemini key is configured or the API is unavailable
- SQLite database
- Responsive frontend
- API health and startup endpoints

## Architecture

```text
PocketSmart-AI/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── services/
│   │   ├── gemini_service.py
│   │   └── recommendation_service.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── planners.py
│   │   └── pages.py
│   ├── templates/
│   └── static/
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Quick start

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set `GEMINI_API_KEY` if you want live AI recommendations.

Run:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

API docs:

http://127.0.0.1:8000/docs

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

## Gemini

The application uses the current Google `google-genai` Python SDK.

Set:

```env
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
```

The model is configurable so you can switch to another Gemini model available to your account without changing application code.

If `GEMINI_API_KEY` is empty, the app still works using deterministic fallback recommendations. This is intentional so the UI, authentication, validation, database, and API can be tested without an API key.

## Test

```bash
python -m pytest -q
```

## Important

The platform links in this project are search/landing links, not live Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO product APIs. The supplied documentation explicitly called for mock/simulated sourcing. Replace `recommendation_service.py` with approved partner APIs or affiliate feeds if live catalog accuracy is required.
