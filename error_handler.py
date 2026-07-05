import json
import logging
from enum import Enum
from typing import Any
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class ProcessingStatus(str, Enum):
    SUCCESS      = "success"
    NEEDS_REVIEW = "needs_review"
    PARTIAL      = "partial"
    FAILED       = "failed"

class DocumentResult:
    def __init__(self, status, data=None, error=None, reason=None):
        self.status = status
        self.data   = data
        self.error  = error
        self.reason = reason

    def to_dict(self):
        return {
            "status": self.status,
            "data":   self.data,
            "error":  self.error,
            "reason": self.reason
        }

def safe_parse_json(raw: str, retry_fn=None) -> dict:
    clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON decode failed: {e}. Raw: {raw[:200]}")
        if retry_fn:
            corrective = (
                f"Your previous output was not valid JSON.\n"
                f"Error: {e}\nOutput was: {raw[:300]}\n"
                f"Return ONLY valid JSON with no explanation or markdown."
            )
            retried = retry_fn(corrective)
            return json.loads(retried)
        raise

def safe_validate(model_class, data: dict) -> tuple:
    try:
        return model_class(**data), None
    except ValidationError as e:
        logger.error(f"Validation failed for {model_class.__name__}: {e}")
        return None, str(e)

def check_critical_fields(result, critical_fields: list[str]) -> list[str]:
    missing = []
    for field in critical_fields:
        val = getattr(result, field, None)
        if val is None or val == "" or val == []:
            missing.append(field)
    return missing