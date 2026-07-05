# run.py
# Entry point — processes all sample documents and prints results

import json
import os
from pipeline import DocumentPipeline

pipeline = DocumentPipeline()

SAMPLE_DIR = "sample_docs"

def load_document(filename: str) -> str:
    path = os.path.join(SAMPLE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def run_all():
    files = [
        "invoice.txt",
        "resume.txt",
        "email.txt",
        "contract.txt"
    ]

    for filename in files:
        print(f"\n{'='*60}")
        print(f"Processing: {filename}")
        print('='*60)

        text   = load_document(filename)
        result = pipeline.process_document(text)

        print(json.dumps(result, indent=2))

    print(f"\n{'='*60}")
    print("All documents processed.")

if __name__ == "__main__":
    run_all()