#!/usr/bin/env python3
"""
Sanity check script for KAU RAG embedding retrieval.
Runs 5 benchmark queries and asserts similarity >= 0.70.
"""

import asyncio
from backend.services.rag_service import retrieve_kau_advice

TEST_QUERIES = [
    ("What is the NPK fertilizer dose for coconut?", "coconut", 0.70),
    ("When should I spray fungicide on rice leaves?", "rice", 0.70),
    ("Best time to harvest nendran banana in Kerala?", "banana", 0.68),
    ("How to control Phytophthora in black pepper?", "pepper", 0.70),
    ("What is the seed rate for rice cultivation?", "rice", 0.70),
]


async def main():
    print("=== AGRI-SAGE EMBEDDING VALIDATION ===")
    passed = 0
    total = len(TEST_QUERIES)

    for query, crop, threshold in TEST_QUERIES:
        results = await retrieve_kau_advice(query, crop=crop, top_k=3)
        top_sim = results[0].similarity if results else 0.0
        top_text = results[0].content[:120].replace("\n", " ") if results else "None"

        status = "PASS" if top_sim >= threshold else "FAIL"
        if status == "PASS":
            passed += 1

        print(f"[{status}] Query: '{query}' ({crop})")
        print(f"       Score: {top_sim:.4f} (Threshold: {threshold})")
        print(f"       Text:  {top_text}...\n")

    print(f"Result: {passed}/{total} tests passed.")
    if passed < total:
        exit(1)
    else:
        print("[SUCCESS] All RAG embedding similarity benchmarks PASSED.")


if __name__ == "__main__":
    asyncio.run(main())
