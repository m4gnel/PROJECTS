import asyncio
import json
import os
import sys

# Ensure backend package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.knowledge.ingestion import DocumentIngestionPipeline


async def main():
    json_path = os.path.join(os.path.dirname(__file__), "seed_urls.json")
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        seeds = json.load(f)

    pipeline = DocumentIngestionPipeline()
    print(f"Starting ingestion of {len(seeds)} documents...")

    for idx, item in enumerate(seeds, start=1):
        url = item["url"]
        title = item.get("title", f"Document {idx}")
        meta = {
            "crop": item.get("crop"),
            "source_tier": item.get("source_tier", 1),
            "source_authority": item.get("source_authority", "ICAR/KAU")
        }
        print(f"[{idx}/{len(seeds)}] Fetching and ingesting: {title} ({url})")
        try:
            doc_id = await pipeline.ingest(url, title=title, manual_meta=meta)
            print(f"  ✓ Success! Ingested Document ID: {doc_id}")
        except Exception as e:
            print(f"  ✗ Failed to ingest {url}: {e}")

    print("Knowledge seeding process complete.")


if __name__ == "__main__":
    asyncio.run(main())
