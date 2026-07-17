DB_PASSWORD_VIOLATION = "SuperSecurePa$$word123"
DB_USER_VIOLATION = "admin_user"
API_KEY_VIOLATION = "XYZ123ABC456DEF789GHI000"
#database_pasword="test@1234"
def connect_to_db_violation():
    """Simulates a database connection using hardcoded credentials."""
    print(f"--- Violation 1: Hardcoded Credentials ---")
    print(f"Attempting to connect with: User='{DB_USER_VIOLATION}', Password='{DB_PASSWORD_VIOLATION}'")
    # In a real app, this would be the actual connection attempt
    print("Database connection simulated.")


import sqlite3
# Note: sqlite3 is used here for simplicity; the principle applies to all databases.

def unsafe_sql_query_violation(user_id):
    """
    Vulnerable function: Directly concatenates user input into a SQL query.
    An attacker could pass '1 OR 1=1 --' as the user_id.
    """
    print(f"\n--- Violation 2: SQL Injection Vulnerability ---")
    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"Unsafe query constructed: {query}")
    
    try:
        # Simulate connection and execution
        conn = sqlite3.connect(':memory:') # Use in-memory for example
        cursor = conn.cursor()
        
        print("Simulating execution of unsafe query...")
        cursor.execute(query) 
        # For '1 OR 1=1 --', this would return ALL users, not just user 1.
        
        # Example of a *safe* version (using parameterization):
        # safe_query = "SELECT * FROM users WHERE id = ?"
        # cursor.execute(safe_query, (user_id,))
        
    except Exception as e:
        print(f"Error during simulated execution (good, this prevents the attack from working): {e}")
    finally:
        conn.close()


import httpx
from fastapi import HTTPException

def fetch_upstream_resource_violation(resource_id):
    url = f"https://api.example.com/resources/{resource_id}"
    try:
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Upstream returned an error: {e}")
        raise HTTPException(status_code=502, detail="Upstream service failed")
    except httpx.RequestError as e:
        print(f"Failed to reach upstream service: {e}")
        raise HTTPException(status_code=502, detail="Could not reach upstream service")


def sync_user_profile_violation(user_id, payload):
    def _normalize_payload(data):
        return {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}

    normalized = _normalize_payload(payload)
    url = f"https://api.example.com/users/{user_id}"
    try:
        response = httpx.put(url, json=normalized, timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="Failed to sync user profile")
    return response.json()


def unsafe_eval_violation(user_input_math):
    """
    Vulnerable function: Uses eval() on unverified input.
    An attacker could pass '__import__("os").system("rm -rf /")'
    """
    print(f"\n--- Violation 3: Unsafe Use of 'eval()' ---")
    print(f"Input received: {user_input_math}")
    
    try:
        # User input could be a simple calculation, or malicious code.
        result = ast.literal_eval(user_input_math)
        print(f"Result of eval(): {result}")
        print("Violation: Arbitrary code executed successfully.")
    except Exception as e:
        print(f"An error occurred (good, implies the malicious code may not have run): {e}")

# --- Execution of Violations ---

if __name__ == "__main__":
    

    connect_to_db_violation()
    print("--- REMEDIATION: Store secrets in a secure vault/environment variables, NOT in code. ---")
    
    malicious_input = "1 OR 1=1 --" 
    # The '--' comments out the rest of the original query, tricking the database.
    unsafe_sql_query_violation(malicious_input)
    print("--- REMEDIATION: Use parameterized queries to treat input as data, not code. ---")

    unsafe_eval_violation("20 * 5 + 1")
    

    malicious_eval_input = "__import__('os').getenv('PATH')"
    unsafe_eval_violation(malicious_eval_input)
    print("--- REMEDIATION: NEVER use eval() on untrusted input. Use ast.literal_eval instead. ---")
