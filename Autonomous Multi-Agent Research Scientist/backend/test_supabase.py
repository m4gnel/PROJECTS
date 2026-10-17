"""
Quick script to test Supabase connection and verify the `users` table.
Reads credentials from `.env`.
"""
import os
import uuid
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    print("❌ SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_ANON_KEY) must be set in .env")
    exit(1)

print(f"Connecting to Supabase at: {url}")
supabase: Client = create_client(url, key)

try:
    # 1. Insert a test row
    test_id = str(uuid.uuid4())
    test_email = f"test-{test_id[:8]}@example.com"
    print(f"\nInserting test user: {test_email}")
    
    insert_res = supabase.table("users").insert({
        "id": test_id,
        "email": test_email,
        "auth_provider": "guest",
        "role": "guest"
    }).execute()
    
    print("✅ Insert successful!")
    
    # 2. Read it back
    print(f"\nReading back user with ID: {test_id}")
    select_res = supabase.table("users").select("*").eq("id", test_id).execute()
    
    if len(select_res.data) > 0:
        print("✅ Read successful! Row data:")
        print(select_res.data[0])
    else:
        print("❌ Could not read the inserted row.")
        
    # 3. Clean up
    print("\nCleaning up (deleting test row)...")
    supabase.table("users").delete().eq("id", test_id).execute()
    print("✅ Cleanup successful!")

except Exception as e:
    print(f"\n❌ Error interacting with Supabase: {e}")
    print("Ensure the 'users' table exists with columns: id (uuid), email (text), auth_provider (text), role (text)")
