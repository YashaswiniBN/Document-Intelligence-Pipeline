from pydantic import BaseModel, Field
from typing import Literal, Optional

# ── Classification ─────────────────────────────────────────────
class DocumentClassification(BaseModel):
    doc_type: Literal["invoice", "resume", "contract", "email", "other"]
    confidence: float = Field(ge=0.0, le=1.0)

# ── Invoice ────────────────────────────────────────────────────
class InvoiceEntities(BaseModel):
    vendor_name: str
    invoice_number: str
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    total_amount: float
    currency: str = "INR"
    line_items: list[str] = Field(default_factory=list)
    tax_amount: Optional[float] = None

# ── Resume ─────────────────────────────────────────────────────
class ResumeEntities(BaseModel):
    candidate_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    current_role: Optional[str] = None
    current_company: Optional[str] = None
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    years_experience: Optional[float] = None

# ── Email ──────────────────────────────────────────────────────
class EmailEntities(BaseModel):
    sender: Optional[str] = None
    recipient: Optional[str] = None
    subject: Optional[str] = None
    date: Optional[str] = None
    key_action: Optional[str] = None
    sentiment: Literal["positive", "neutral", "negative"] = "neutral"

# ── Contract ───────────────────────────────────────────────────
class ContractEntities(BaseModel):
    parties: list[str] = Field(default_factory=list)
    contract_type: Optional[str] = None
    effective_date: Optional[str] = None
    expiry_date: Optional[str] = None
    key_obligations: list[str] = Field(default_factory=list)
    value: Optional[float] = None
    currency: str = "INR"

# ── Router — maps doc_type to its entity model ─────────────────
ENTITY_MODEL_MAP = {
    "invoice":  InvoiceEntities,
    "resume":   ResumeEntities,
    "email":    EmailEntities,
    "contract": ContractEntities,
}