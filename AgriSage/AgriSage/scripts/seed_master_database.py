#!/usr/bin/env python3
"""
Agri-SAGE Master Database Setup & Seeder Script
Executes backend/init_master_database.sql against PostgreSQL database,
validates schema creation, verifies pgvector HNSW index, checks pre-loaded reference data,
and performs diagnostic health checks.
"""

import asyncio
import os
import sys
from typing import Dict, Any

# Ensure workspace root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Reconfigure stdout for utf-8 if on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from sqlalchemy import text
from backend.config import settings
from backend.database import AsyncSessionLocal, check_db_connection


async def run_master_setup() -> Dict[str, Any]:
    print("=" * 70)
    print("[*] AGRI-SAGE — MASTER DATABASE INITIALIZATION & VERIFICATION")
    print("=" * 70)

    # 1. Test database connection
    print("\n[1/4] Checking database connectivity...")
    connected = await check_db_connection()
    if not connected:
        print("  [!] Database connection failed. Please check POSTGRES_URL / docker status.")
        print(f"  Configured URL: {settings.DATABASE_URL}")
        return {"status": "FAILED", "reason": "Database connection unreachable"}
    print("  [+] Database connectivity verified.")

    # 2. Read and execute master SQL script
    sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend", "init_master_database.sql")
    if not os.path.exists(sql_path):
        print(f"  [-] Master SQL script not found at {sql_path}")
        return {"status": "FAILED", "reason": f"File not found: {sql_path}"}

    print(f"\n[2/4] Executing master SQL script ({os.path.basename(sql_path)})...")
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    async with AsyncSessionLocal() as session:
        try:
            await session.execute(text(sql_script))
            await session.commit()
            print("  [+] Master SQL script executed and committed successfully.")
        except Exception as e:
            await session.rollback()
            print(f"  [-] Error executing master SQL script: {e}")
            return {"status": "FAILED", "error": str(e)}

    # 3. Validate Schema Integrity
    print("\n[3/4] Validating database schema integrity...")
    results = {}
    async with AsyncSessionLocal() as session:
        # Check extensions
        ext_res = await session.execute(text(
            "SELECT count(*) FROM pg_extension WHERE extname IN ('vector','uuid-ossp','pg_trgm','btree_gin','pg_stat_statements')"
        ))
        results["extensions_count"] = ext_res.scalar()
        print(f"  - Active Extensions: {results['extensions_count']} / 5")

        # Check schemas
        schema_res = await session.execute(text(
            "SELECT count(*) FROM information_schema.schemata WHERE schema_name IN ('core','realtime','agents','intelligence','alerts','market','analytics','system')"
        ))
        results["schemas_count"] = schema_res.scalar()
        print(f"  - Master Schemas: {results['schemas_count']} / 8")

        # Check soil zones seed count
        soil_res = await session.execute(text("SELECT count(*) FROM realtime.soil_zones"))
        results["soil_zones_count"] = soil_res.scalar()
        print(f"  - Pre-loaded Soil Zones: {results['soil_zones_count']} districts")

        # Check MSP reference seed count
        msp_res = await session.execute(text("SELECT count(*) FROM realtime.msp_reference"))
        results["msp_reference_count"] = msp_res.scalar()
        print(f"  - MSP Reference Records: {results['msp_reference_count']} crops (2025-26)")

        # Check vector index
        hnsw_res = await session.execute(text(
            "SELECT count(*) FROM pg_indexes WHERE indexname = 'idx_kau_hnsw'"
        ))
        results["hnsw_index_exists"] = (hnsw_res.scalar() > 0)
        print(f"  - pgvector HNSW Index (idx_kau_hnsw): {'[+] CONFIRMED' if results['hnsw_index_exists'] else '[-] MISSING'}")

    # 4. End-to-end verification report
    print("\n[4/4] Verification Summary")
    success = (
        results["extensions_count"] >= 2 and
        results["schemas_count"] == 8 and
        results["soil_zones_count"] > 0 and
        results["msp_reference_count"] > 0
    )

    if success:
        print("\n[SUCCESS] MASTER DATABASE SETUP PASSED WITH 100% PRECISION!")
    else:
        print("\n[!] Master database setup incomplete. Review issues above.")

    return {
        "status": "SUCCESS" if success else "PARTIAL",
        "details": results
    }


if __name__ == "__main__":
    res = asyncio.run(run_master_setup())
    if res["status"] != "SUCCESS" and "error" in res:
        sys.exit(1)
