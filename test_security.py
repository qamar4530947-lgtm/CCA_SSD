import pytest
from app_vulnerable import app as app_vuln
from app_fixed import app as app_safe

# --- Test Fixtures to load both apps ---
@pytest.fixture
def client_vuln():
    with app_vuln.test_client() as client:
        yield client

@pytest.fixture
def client_safe():
    with app_safe.test_client() as client:
        yield client

# --- Test 1: SQL Injection ---
# Attack payload to bypass password check: ' OR '1'='1
def test_sql_injection_vuln(client_vuln):
    # This test asserts that the vulnerable app WRONGLY allows login.
    # To show the automated test "failing" the security check, we assert it gets a 401. 
    # Because it's vulnerable, it will get a 200, causing the Pytest to FAIL.
    response = client_vuln.post('/login', data={'username': "admin' OR '1'='1", 'password': "wrong"})
    assert response.status_code == 401, "SECURITY FAILURE: SQL Injection allowed login!"

def test_sql_injection_safe(client_safe):
    # This test expects the fixed app to properly reject the malicious payload with a 401.
    response = client_safe.post('/login', data={'username': "admin' OR '1'='1", 'password': "wrong"})
    assert response.status_code == 401

# --- Test 2: Cross-Site Scripting (XSS) ---
def test_xss_vuln(client_vuln):
    payload = "<script>alert('XSS')</script>"
    response = client_vuln.get(f'/greet?name={payload}')
    # If the exact payload is in the response data, it is vulnerable.
    # We assert it is NOT in the data. The vulnerable app will include it, failing the test.
    assert payload.encode() not in response.data, "SECURITY FAILURE: XSS payload reflected unescaped!"

def test_xss_safe(client_safe):
    payload = "<script>alert('XSS')</script>"
    response = client_safe.get(f'/greet?name={payload}')
    # The fixed app escapes the payload (e.g., &lt;script&gt;)
    assert payload.encode() not in response.data
    assert b"&lt;script&gt;" in response.data

# --- Test 3: Command Injection ---
def test_command_injection_vuln(client_vuln):
    # Payload attempts to append a command using a semicolon
    payload = "127.0.0.1; echo 'HACKED'"
    response = client_vuln.get(f'/ping?ip={payload}')
    # If 'HACKED' is in the output, injection succeeded.
    assert b"HACKED" not in response.data, "SECURITY FAILURE: Command Injection succeeded!"

def test_command_injection_safe(client_safe):
    payload = "127.0.0.1; echo 'HACKED'"
    response = client_safe.get(f'/ping?ip={payload}')
    # The fixed app neutralizes the command separators
    assert b"HACKED" not in response.data