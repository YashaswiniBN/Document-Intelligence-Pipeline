import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"
MODEL        = "llama-3.3-70b-versatile"

def call_llm(system: str, user: str, temperature: float = 0.1) -> str:
    """
    Raw LLM call. Returns the model's text response as a string.
    Temperature 0.1 for deterministic structured output.
    """
    if not GROQ_API_KEY:
        return _mock_response(user)

    with httpx.Client(timeout=30.0) as client:
        r = client.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": MODEL,
                "temperature": temperature,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user}
                ]
            }
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

def _mock_response(user_text: str) -> str:
    """
    Mock responses for development without an API key.
    Returns realistic JSON based on keywords in the text.
    """
    text = user_text.lower()

    if "invoice" in text or "total due" in text or "vendor" in text:
        return json.dumps({
            "doc_type": "invoice",
            "confidence": 0.96
        })
    elif "resume" in text or "experience" in text or "skills" in text:
        return json.dumps({
            "doc_type": "resume",
            "confidence": 0.94
        })
    elif "agreement" in text or "party" in text or "whereas" in text:
        return json.dumps({
            "doc_type": "contract",
            "confidence": 0.91
        })
    elif "from:" in text or "subject:" in text or "dear" in text:
        return json.dumps({
            "doc_type": "email",
            "confidence": 0.93
        })
    else:
        return json.dumps({
            "doc_type": "other",
            "confidence": 0.55
        })