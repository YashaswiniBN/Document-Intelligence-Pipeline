import json
from pipeline import DocumentPipeline

pipeline = DocumentPipeline()

SAMPLE_DOCS = [
    {
        "id": "inv_001",
        "text": """INVOICE
Vendor: Acme Office Supplies Pvt Ltd
Invoice No: INV-2847
Date: 2026-06-15
Due Date: 2026-07-15

Items:
- Ergonomic chairs x10 @ ₹8,500 = ₹85,000
- Standing desks x5 @ ₹22,000 = ₹1,10,000

Subtotal: ₹1,95,000
GST 18%: ₹35,100
TOTAL DUE: ₹2,30,100""",
        "expected_type": "invoice",
        "expected_fields": ["vendor_name", "invoice_number", "total_amount"]
    },
    {
        "id": "res_001",
        "text": """Yashaswini B N
Bengaluru, Karnataka | github.com/YashaswiniBN
RPA Developer → AI Engineer

EXPERIENCE
UST Global | RPA Developer | 2023–present
- Automation Anywhere A360, UiPath
- Batch Sentiment Analyzer (FastAPI + Groq)

EDUCATION
B.Tech Information Science | VTU | 2023

SKILLS
Python, LangChain, LangGraph, FastAPI, Pydantic""",
        "expected_type": "resume",
        "expected_fields": ["candidate_name", "current_role", "skills"]
    },
    {
        "id": "email_001",
        "text": """From: priya.sharma@techcorp.com
To: vendor@acme.com
Subject: RE: Invoice INV-2847 — Payment Query

Hi team, following up on invoice INV-2847 for ₹2,30,100.
Our finance team has processed it but the payment is showing
delayed due to a bank holiday. Expected by July 20th.

Regards,
Priya Sharma | Finance Manager""",
        "expected_type": "email",
        "expected_fields": ["sender", "subject", "key_action"]
    },
    {
        "id": "unknown_001",
        "text": "The quick brown fox jumps over the lazy dog. 1234567890.",
        "expected_type": "other",
        "expected_fields": []
    },
    {
        "id": "low_conf_001",
        "text": "Meeting notes from Q2 review. Sales up 12%. Team morale good.",
        "expected_type": None,
        "expected_status": "needs_review"
    }
]

def test_all():
    passed = 0
    failed = 0

    for doc in SAMPLE_DOCS:
        print(f"\n{'─'*50}")
        print(f"Testing: {doc['id']}")
        result = pipeline.process_document(doc["text"])
        print(f"Status : {result.get('status')}")
        print(f"Type   : {result.get('classification', {}).get('doc_type', 'n/a')}")

        if doc.get("expected_type"):
            actual_type = result.get("classification", {}).get("doc_type")
            assert actual_type == doc["expected_type"], \
                f"FAIL: expected {doc['expected_type']}, got {actual_type}"

        if doc.get("expected_status"):
            assert result.get("status") == doc["expected_status"], \
                f"FAIL: expected status {doc['expected_status']}"

        if doc.get("expected_fields") and result.get("entities"):
            for field in doc["expected_fields"]:
                assert field in result["entities"], \
                    f"FAIL: missing field '{field}' in entities"

        print("PASS")
        passed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")

if __name__ == "__main__":
    test_all()