import json
import logging
from pydantic import ValidationError
from schemas import DocumentClassification, ENTITY_MODEL_MAP
from prompts import CLASSIFY_SYSTEM, CLASSIFY_USER, EXTRACTION_PROMPTS
from llm_client import call_llm

logging.basicConfig(level=logging.INFO, format="%(levelname)s — %(message)s")
logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.70

class DocumentPipeline:

    def classify(self, text: str) -> DocumentClassification:
        logger.info("Step 1: classifying document")
        user  = CLASSIFY_USER.format(text=text[:3000])
        raw   = call_llm(system=CLASSIFY_SYSTEM, user=user, temperature=0.1)
        clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
        data  = json.loads(clean)
        return DocumentClassification(**data)

    def extract(self, doc_type: str, text: str) -> dict:
        logger.info(f"Step 2: extracting entities for type={doc_type}")

        if doc_type not in EXTRACTION_PROMPTS:
            return {}

        system_prompt, user_template = EXTRACTION_PROMPTS[doc_type]
        user  = user_template.format(text=text[:4000])
        raw   = call_llm(system=system_prompt, user=user, temperature=0.1)
        clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
        data  = json.loads(clean)

        entity_model = ENTITY_MODEL_MAP[doc_type]
        validated    = entity_model(**data)
        return validated.model_dump()

    def process_document(self, text: str) -> dict:
        classification = self.classify(text)
        logger.info(f"Classified as: {classification.doc_type} (confidence={classification.confidence})")

        if classification.confidence < CONFIDENCE_THRESHOLD:
            return {
                "status":         "needs_review",
                "reason":         "low_confidence",
                "classification": classification.model_dump(),
                "entities":       None
            }

        if classification.doc_type == "other":
            return {
                "status":         "success",
                "classification": classification.model_dump(),
                "entities":       None
            }

        try:
            entities = self.extract(classification.doc_type, text)
            return {
                "status":         "success",
                "classification": classification.model_dump(),
                "entities":       entities
            }
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"Extraction failed: {e}")
            return {
                "status":         "partial",
                "classification": classification.model_dump(),
                "entities":       None,
                "error":          str(e)
            }


if __name__ == "__main__":
    pipeline = DocumentPipeline()

    SAMPLE_INVOICE = """
    INVOICE — Acme Office Supplies Pvt Ltd
    Invoice No: INV-2847
    Date: 2026-06-15 | Due: 2026-07-15

    Ergonomic chairs x10 @ ₹8,500 = ₹85,000
    Standing desks x5 @ ₹22,000 = ₹1,10,000
    Subtotal: ₹1,95,000 | GST 18%: ₹35,100
    TOTAL DUE: ₹2,30,100
    """

    SAMPLE_RESUME = """
    Yashaswini B N | Bengaluru | github.com/YashaswiniBN
    RPA Developer → AI Engineer | 1.8 yrs experience

    UST Global | RPA Developer | 2023–present
    Automation Anywhere A360, UiPath, FastAPI, Python

    B.Tech Information Science | VTU | 2023
    Skills: Python, LangChain, LangGraph, Pydantic, asyncio
    """

    for doc in [SAMPLE_INVOICE, SAMPLE_RESUME]:
        print("\n" + "─" * 60)
        result = pipeline.process_document(doc)
        print(json.dumps(result, indent=2))