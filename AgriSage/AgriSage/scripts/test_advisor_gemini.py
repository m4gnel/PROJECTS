import asyncio
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Load .env from root and backend
root_env = REPO_ROOT / ".env"
backend_env = REPO_ROOT / "backend" / ".env"

if root_env.exists():
    load_dotenv(root_env, override=True)
if backend_env.exists():
    load_dotenv(backend_env, override=False)

def check_env_sync():
    root_key = ""
    backend_key = ""
    if root_env.exists():
        for line in root_env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("GEMINI_API_KEY="):
                root_key = line.split("=", 1)[1].strip()
    if backend_env.exists():
        for line in backend_env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("GEMINI_API_KEY="):
                backend_key = line.split("=", 1)[1].strip()
    
    # Sync if one has it and the other doesn't
    if root_key and not backend_key and backend_env.exists():
        content = backend_env.read_text(encoding="utf-8")
        lines = []
        for l in content.splitlines():
            if l.strip().startswith("GEMINI_API_KEY="):
                lines.append(f"GEMINI_API_KEY={root_key}")
            else:
                lines.append(l)
        backend_env.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("[SYNC] Propagated GEMINI_API_KEY from root .env to backend/.env")
    elif backend_key and not root_key and root_env.exists():
        content = root_env.read_text(encoding="utf-8")
        lines = []
        for l in content.splitlines():
            if l.strip().startswith("GEMINI_API_KEY="):
                lines.append(f"GEMINI_API_KEY={backend_key}")
            else:
                lines.append(l)
        root_env.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("[SYNC] Propagated GEMINI_API_KEY from backend/.env to root .env")

    return root_key or backend_key or os.getenv("GEMINI_API_KEY", "")

async def main():
    print("=" * 65)
    print("Agri-SAGE Gemini Advisor Diagnostic & Verification Tool")
    print("=" * 65)
    
    api_key = check_env_sync()

    if not api_key:
        print("\n[!] WARNING: GEMINI_API_KEY is currently empty in .env!")
        print("    If you just pasted your key in VS Code, please PRESS Ctrl+S to save .env to disk.")
        print("    File location: " + str(root_env))
        print("    Expected format: GEMINI_API_KEY=AIzaSy...")
        return 1

    masked_key = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
    print(f"\n[OK] Detected GEMINI_API_KEY: {masked_key}")

    # Set in os.environ so all modules see it
    os.environ["GEMINI_API_KEY"] = api_key

    from backend.config import settings
    settings.GEMINI_API_KEY = api_key
    settings.LLM_PROVIDER = "gemini"
    print(f"[OK] Settings configured -> Provider: {settings.LLM_PROVIDER}, Model: {settings.LLM_MODEL}")

    print("\n--> Step 1: Testing direct Gemini 1.5 Flash API invocation...")
    t0 = time.time()
    try:
        from backend.agents.llm_util import call_gemini_safe
        test_prompt = "A farmer in Palakkad, Kerala noticed yellowing of paddy leaves with stunted growth after heavy rain. Provide a concise 2-sentence agronomist diagnosis and initial recommendation."
        response = await call_gemini_safe(
            prompt=test_prompt,
            system_prompt="You are Agri-SAGE, an expert agronomic AI assistant for Indian farmers."
        )
        elapsed = time.time() - t0

        if response:
            print(f"[OK] SUCCESS! Response received in {elapsed:.2f}s:")
            print("-" * 65)
            print(response)
            print("-" * 65)
        else:
            print(f"[x] FAILED: call_gemini_safe returned empty string. Check API key validity or quota.")
            return 2
    except Exception as e:
        print(f"[x] ERROR during call_gemini_safe: {e}")
        return 3

    print("\n--> Step 2: Testing structured JSON response generation via LLMService...")
    t1 = time.time()
    try:
        from backend.services.llm_service import llm_service
        llm_service.gemini_key = api_key
        llm_service.provider = "gemini"
        
        json_resp = await llm_service.generate(
            system_prompt="You are an agricultural diagnostic system. You MUST output ONLY a valid JSON object with keys: diagnosis, confidence, and immediate_action.",
            user_prompt="Farmer report: Blast lesions observed on basmati rice leaves during tillering stage.",
            temperature=0.1
        )
        elapsed_json = time.time() - t1

        if json_resp and isinstance(json_resp, dict):
            print(f"[OK] SUCCESS! Structured JSON generated in {elapsed_json:.2f}s:")
            import json
            print(json.dumps(json_resp, indent=2))
        else:
            print(f"[x] FAILED: LLMService did not produce valid JSON response.")
            return 4
    except Exception as e:
        print(f"[x] ERROR during LLMService test: {e}")
        return 5

    print("\n" + "=" * 65)
    print("ALL GEMINI ADVISOR CHECKS PASSED PERFECTLY!")
    print("=" * 65)
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code or 0)
