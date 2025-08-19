import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    """Test health check endpoint."""
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.get_json() == {'status': 'ok'}

def test_get_prompt_instructions(client):
    """Test getPromptInstructions endpoint."""
    data = {
        "country": "US",
        "language": "en",
        "sessionType": "session1",
        "userContext": {}
    }
    rv = client.post('/mcp/getPromptInstructions', json=data)
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "You are Quin" in json_data['instructions']
    assert json_data['financial_context']['financial_systems']['insurance'] == "FDIC insurance up to $250k"

def test_test_prompt(client):
    """Test test/prompt endpoint."""
    rv = client.get('/test/prompt?country=US&language=en&session=session1')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "You are Quin" in json_data['instructions']
    assert json_data['financial_context']['financial_systems']['insurance'] == "FDIC insurance up to $250k"

def test_get_available_languages(client):
    """Test getAvailableLanguages endpoint."""
    rv = client.get('/mcp/getAvailableLanguages?country=US')
    assert rv.status_code == 200
    assert rv.get_json() == ['en', 'es']

def test_get_country_financial_context(client):
    """Test getCountryFinancialContext endpoint."""
    rv = client.get('/mcp/getCountryFinancialContext?country=US')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['financial_systems']['insurance'] == "FDIC insurance up to $250k"
