import pytest
from unittest.mock import Mock

from application.managers.token_manager import TokenManager
from application.services.token_service import TokenService

@pytest.fixture
def mock_token_service():
    return Mock(spec=TokenService)

def test_token_manager_initialization(mock_settings, mock_token_service):
    manager = TokenManager(mock_settings, mock_token_service)
    
    # Verify tokens are created
    assert manager.slp.symbol == "SLP"
    assert manager.axs.symbol == "AXS"
    assert manager.usdc.symbol == "USDC"
    
    # Verify addresses from settings are used
    assert manager.slp.address == "0xSLP"
    assert manager.axs.address == "0xAXS"

def test_get_token_dynamic(mock_settings, mock_token_service):
    manager = TokenManager(mock_settings, mock_token_service)
    
    token = manager.get_token("eth")
    assert token.symbol == "ETH"
    assert token.address == "0xETH"

def test_get_token_case_insensitive(mock_settings, mock_token_service):
    manager = TokenManager(mock_settings, mock_token_service)
    
    token = manager.get_token("ETH")
    assert token.symbol == "ETH"

def test_get_token_not_found(mock_settings, mock_token_service):
    manager = TokenManager(mock_settings, mock_token_service)
    
    with pytest.raises(KeyError):
        manager.get_token("INVALID")
