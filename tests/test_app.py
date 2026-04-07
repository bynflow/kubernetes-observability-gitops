from app.app import app


def test_index_get():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to the Flask App!" in resp.data


def test_square_valid_integer():
    client = app.test_client()
    resp = client.post("/", data={"number": "8"})
    assert resp.status_code == 200
    assert b"Input number:" in resp.data
    assert b"8" in resp.data
    assert b"Square:" in resp.data
    assert b"64" in resp.data


def test_square_zero():
    client = app.test_client()
    resp = client.post("/", data={"number": "0"})
    assert resp.status_code == 200
    assert b"Input number:" in resp.data
    assert b"0" in resp.data
    assert b"Square:" in resp.data


def test_square_invalid_non_numeric():
    client = app.test_client()
    resp = client.post("/", data={"number": "abc"})
    assert resp.status_code == 200
    assert b"Please enter a valid non-negative integer." in resp.data


def test_square_empty_input():
    client = app.test_client()
    resp = client.post("/", data={"number": ""})
    assert resp.status_code == 200
    assert b"Please enter a valid non-negative integer." in resp.data


def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json["status"] == "ok"


def test_metrics():
    client = app.test_client()
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"app_requests_total" in resp.data or b"# HELP" in resp.data
