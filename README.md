# Zomato AI Recommender — Backend

A FastAPI-powered REST API that ingests real Zomato restaurant data from Hugging Face (41,000+ restaurants), filters based on user preferences, and generates personalized recommendations using Google Gemini AI.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_AI-2.0_Flash-4285F4?logo=google&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?logo=pandas&logoColor=white)

---

## Features

- **Real Data** — Downloads and processes the Zomato dataset (51,000+ entries) from Hugging Face, cleaned to 41,000+ valid restaurants
- **Smart Filtering** — Filter by location, cuisine, budget (low/medium/high), and minimum rating with relevance-based ranking
- **AI Recommendations** — Google Gemini generates natural language recommendations explaining why each restaurant is a great pick
- **Auto-Caching** — Dataset is downloaded once and cached locally as CSV for fast subsequent startups
- **Metadata Endpoint** — Provides available cities, cuisines, and restaurant count for frontend dropdowns
- **CORS Enabled** — Pre-configured to work with the React frontend

---

## Tech Stack

| Technology | Purpose |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com) | Web framework |
| [Pandas](https://pandas.pydata.org) | Data processing & filtering |
| [Hugging Face Datasets](https://huggingface.co/docs/datasets) | Dataset ingestion |
| [Google Generative AI](https://ai.google.dev) | Gemini LLM integration |
| [Pydantic](https://docs.pydantic.dev) | Request/response validation |
| [Uvicorn](https://www.uvicorn.org) | ASGI server |
| [pytest](https://pytest.org) | Testing |

---

## Project Structure

```
zomato-recommendation-backend/
├── main.py                    # FastAPI app entry point, CORS, lifespan
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (GEMINI_API_KEY)
├── data/
│   ├── __init__.py
│   ├── data_loader.py         # Load, clean & cache Zomato dataset from Hugging Face
│   └── processed/             # Auto-generated cached CSV (gitignored)
├── models/
│   ├── __init__.py
│   └── preferences.py         # Pydantic schemas (UserPreferences, RecommendationResponse)
├── services/
│   ├── __init__.py
│   ├── filter_service.py      # Filter & rank restaurants by user preferences
│   └── llm_service.py         # Gemini AI prompt building & API calls
├── api/
│   ├── __init__.py
│   └── routes.py              # API route definitions (/health, /metadata, /recommend)
└── README.md
```

---

## Prerequisites

- **Python** 3.10+
- **Gemini API Key** — Get one at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/zomato-recommendation-backend.git
cd zomato-recommendation-backend
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Start the server

```bash
uvicorn main:app --reload --port 8000
```

On first startup, the Zomato dataset (~574 MB) will be downloaded from Hugging Face and cached locally. Subsequent startups load from the cache and are much faster.

The API will be available at **http://localhost:8000**.

### 6. Verify it's running

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/metadata` | Available cities, cuisines, total restaurant count |
| `POST` | `/recommend` | Get AI-powered restaurant recommendations |

### `GET /metadata`

Returns data for populating frontend dropdowns.

```json
{
  "cities": ["Koramangala", "Indiranagar", "Whitefield", "..."],
  "cuisines": ["Italian", "Chinese", "North Indian", "..."],
  "total_restaurants": 41418
}
```

### `POST /recommend`

**Request Body:**

```json
{
  "place": "Koramangala",
  "cuisine": "Italian",
  "price": "medium",
  "rating": 4.0
}
```

All fields are optional. Omit or leave empty to skip that filter.

| Field | Type | Values | Description |
|---|---|---|---|
| `place` | string | Any city from `/metadata` | Filter by location |
| `cuisine` | string | Any cuisine from `/metadata` | Filter by cuisine type |
| `price` | string | `low`, `medium`, `high` | Budget bracket (≤₹300, ₹300–800, ₹800+) |
| `rating` | float | `0.0` – `5.0` | Minimum rating threshold |

**Response:**

```json
{
  "summary": "AI-generated recommendation narrative...",
  "restaurants": [
    {
      "name": "ECHOES Koramangala",
      "cuisines": "Chinese, American, Continental, Italian",
      "rating": 4.7,
      "cost_for_two": 750.0,
      "city": "Koramangala 5th Block",
      "price_category": "medium"
    }
  ],
  "filtered_count": 10
}
```

---

## Running Tests

```bash
pytest tests/ -v
```

Tests are organized by phase:

| Folder | Tests |
|---|---|
| `tests/test_phase1/` | Data loading, cleaning, normalization |
| `tests/test_phase2/` | Filtering logic, price categorization, sorting |
| `tests/test_phase3/` | Prompt building, LLM integration stubs |

> The LLM integration test requires a valid `GEMINI_API_KEY` and is skipped by default.

---

## Deployment (Render)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `GEMINI_API_KEY` = your key
6. Deploy

---

## Related Repository

- **Frontend**: [zomato-recommendation-frontend](https://github.com/YOUR_USERNAME/zomato-recommendation-frontend) — React + TypeScript + Tailwind CSS

---

## License

This project is for educational and demonstration purposes.
