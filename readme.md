# Document Intelligence Pipeline

Classifies and extracts structured data from raw documents
using LLMs — no framework abstraction, raw API calls only.

## Architecture

Raw document
     │
     ▼
Classification (LLM call 1)
  → doc_type: invoice | resume | email | contract | other
  → confidence: 0.0–1.0
     │
     ├─ confidence < 0.7 ──▶ needs_review queue
     │
     ▼
Type-specific extraction (LLM call 2)
  → entity schema per doc_type
     │
     ▼
Pydantic validation
  → schema enforced, partial results flagged
     │
     ▼
Structured JSON output

## Tech stack
- Python 3.11+
- Groq API (llama3-70b-8192) — free tier
- Pydantic v2 — output validation
- asyncio + Semaphore — batch concurrency
- tenacity — retry logic

## Setup
cp .env.example .env
# add GROQ_API_KEY=gsk_...
pip install -r requirements.txt
python test_pipeline.py

## Sample output
{
  "status": "success",
  "classification": {
    "doc_type": "invoice",
    "confidence": 0.97
  },
  "entities": {
    "vendor_name": "Acme Office Supplies Pvt Ltd",
    "invoice_number": "INV-2847",
    "total_amount": 230100.0,
    "due_date": "2026-07-15",
    "line_items": ["Ergonomic chairs x10", "Standing desks x5"]
  }
}

## Key design decisions
1. Classify before extracting — fast fail on unknown documents
2. Confidence threshold at 0.7 — routes ambiguous docs to review
3. Type-specific extraction prompts — tighter schemas, better accuracy
4. Pydantic validation after every extraction — no silent bad data
5. All errors are structured dicts, never bare exceptions