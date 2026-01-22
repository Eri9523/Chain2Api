import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from decimal import Decimal

from launcher import create_app
from application.managers.token_manager import TokenManager
from domain.models.token_wrapper import TokenWrapper
from domain.models.token import Token

@pytest.fixture
def mock_token_manager():
    tm = Mock(spec=TokenManager)
    
    # Create mock wrappers
    slp_token = Token("SLP", "0xSLP", "Smooth Love Potion", 0)
    slp_wrapper = Mock(spec=TokenWrapper)
    slp_wrapper.symbol = "SLP"
    slp_wrapper.address = "0xSLP"
    slp_wrapper.decimals = 0
    slp_wrapper._token = slp_token # Access private member for list endpoint
    
    # Setup methods
    slp_wrapper.getBalance.return_value = Decimal("100")
    slp_wrapper.getPrice.return_value = Decimal("0.003")
    slp_wrapper.getTotalSupply.return_value = Decimal("1000000")
    
    # Setup Manager
    tm.get_all_tokens.return_value = {"slp": slp_wrapper}
    
    def get_token_side_effect(symbol):
        if symbol.lower() == "slp":
            return slp_wrapper
        raise KeyError(f"Token {symbol} not found")
        
    tm.get_token.side_effect = get_token_side_effect
    
    return tm

@pytest.fixture
def client(mock_token_manager):
    # Create a mock injector
    mock_injector = Mock()
    mock_injector.get.return_value = mock_token_manager
    
    # Create app with mock injector
    app = create_app(mock_injector)
    
    # Override dependency if needed, but our create_app uses middleware/dependency injection pattern
    # The create_app function in launcher.py sets request.state.injector = root_injector
    # So passing mock_injector to create_app should work
    
    return TestClient(app)

def test_list_tokens(client):
    response = client.get("/tokens/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["symbol"] == "SLP"
    assert data[0]["address"] == "0xSLP"

def test_get_balance(client):
    response = client.get("/tokens/slp/balance/0xUser")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "SLP"
    assert data["balance"] == 100.0

def test_get_price(client):
    response = client.get("/tokens/slp/price")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "SLP"
    assert data["price_usdc"] == 0.003

def test_get_supply(client):
    response = client.get("/tokens/slp/supply")
    assert response.status_code == 200
    data = response.json()
    assert data["total_supply"] == 1000000.0

def test_token_not_found(client):
    response = client.get("/tokens/invalid/price")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
