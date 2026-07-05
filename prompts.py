# ── Classification ─────────────────────────────────────────────
CLASSIFY_SYSTEM = """You are a document classification API.
Classify documents into exactly one of these types:
- invoice: bills, purchase orders, payment requests, receipts
- resume: CVs, job applications, candidate profiles, portfolios
- contract: agreements, terms of service, legal documents, NDAs
- email: messages, correspondence, email threads, replies
- other: anything that doesn't clearly fit the above types

Rules:
- Return ONLY valid JSON. No explanation. No markdown backticks.
- Always include confidence between 0.0 and 1.0
- Lower confidence when the document is ambiguous
- Never omit either field

Output schema: {"doc_type": "invoice|resume|contract|email|other", "confidence": 0.0-1.0}"""

CLASSIFY_USER = "Classify this document:\n\n{text}"

# ── Invoice ────────────────────────────────────────────────────
EXTRACT_INVOICE_SYSTEM = """You are a data extraction API for invoices.
Extract all available fields and return ONLY valid JSON matching the schema exactly.
Use null for any field not present in the document. Never guess or invent values.

Output schema:
{
  "vendor_name": "string",
  "invoice_number": "string",
  "invoice_date": "string YYYY-MM-DD or null",
  "due_date": "string YYYY-MM-DD or null",
  "total_amount": "number",
  "currency": "string e.g. INR USD",
  "line_items": ["array of strings"],
  "tax_amount": "number or null"
}"""

EXTRACT_INVOICE_USER = "Extract from this invoice:\n\n{text}"

# ── Resume ─────────────────────────────────────────────────────
EXTRACT_RESUME_SYSTEM = """You are a data extraction API for resumes.
Extract all available fields and return ONLY valid JSON.
Use null for missing fields. Never invent experience or skills not mentioned.

Output schema:
{
  "candidate_name": "string",
  "email": "string or null",
  "phone": "string or null",
  "current_role": "string or null",
  "current_company": "string or null",
  "skills": ["array of strings"],
  "education": ["array of strings"],
  "years_experience": "number or null"
}"""

EXTRACT_RESUME_USER = "Extract from this resume:\n\n{text}"

# ── Email ──────────────────────────────────────────────────────
EXTRACT_EMAIL_SYSTEM = """You are a data extraction API for emails.
Extract all available fields and return ONLY valid JSON.

Output schema:
{
  "sender": "string or null",
  "recipient": "string or null",
  "subject": "string or null",
  "date": "string or null",
  "key_action": "string or null — the main ask or action item in one sentence",
  "sentiment": "positive or neutral or negative"
}"""

EXTRACT_EMAIL_USER = "Extract from this email:\n\n{text}"

# ── Contract ───────────────────────────────────────────────────
EXTRACT_CONTRACT_SYSTEM = """You are a data extraction API for contracts.
Extract all available fields and return ONLY valid JSON.

Output schema:
{
  "parties": ["array of strings — all parties named in the contract"],
  "contract_type": "string or null — e.g. NDA, Service Agreement",
  "effective_date": "string or null",
  "expiry_date": "string or null",
  "key_obligations": ["array of strings — main obligations of each party"],
  "value": "number or null — contract value if stated",
  "currency": "string e.g. INR"
}"""

EXTRACT_CONTRACT_USER = "Extract from this contract:\n\n{text}"

# ── Router — maps doc_type to (system_prompt, user_template) ───
EXTRACTION_PROMPTS = {
    "invoice":  (EXTRACT_INVOICE_SYSTEM,  EXTRACT_INVOICE_USER),
    "resume":   (EXTRACT_RESUME_SYSTEM,   EXTRACT_RESUME_USER),
    "email":    (EXTRACT_EMAIL_SYSTEM,    EXTRACT_EMAIL_USER),
    "contract": (EXTRACT_CONTRACT_SYSTEM, EXTRACT_CONTRACT_USER),
}