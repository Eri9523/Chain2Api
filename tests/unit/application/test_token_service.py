import pytest
from unittest.mock import Mock
from decimal import Decimal

from application.services.token_service import TokenService
from application.services.katana_service import KatanaService

@pytest.fixture
def mock_katana_service():
    return Mock(spec=KatanaService)

def test_get_balance(mock_repository, mock_settings, mock_katana_service, mock_token):
    # Setup
    mock_repository.get_balance.return_value = Decimal("100.5")
    service = TokenService(mock_repository, mock_settings, mock_katana_service)
    
    # Execute
    balance = service.get_balance(mock_token, "0xUser")
    
    # Verify
    assert balance == Decimal("100.5")
    mock_repository.get_balance.assert_called_once_with(mock_token, "0xUser")

def test_get_price_normal_token(mock_repository, mock_settings, mock_katana_service, mock_token):
    # Setup
    mock_katana_service.get_token_price.return_value = 2.5
    service = TokenService(mock_repository, mock_settings, mock_katana_service)
    
    # Execute
    price = service.get_price(mock_token)
    
    # Verify
    assert price == Decimal("2.5")
    mock_katana_service.get_token_price.assert_called_once()

def test_get_price_usdc(mock_repository, mock_settings, mock_katana_service):
    # Setup
    usdc_token = Mock()
    usdc_token.address = "0xUSDC"
    # Ensure settings match
    mock_settings.tokens.USDC_ADDRESS = "0xUSDC"
    
    service = TokenService(mock_repository, mock_settings, mock_katana_service)
    
    # Execute
    price = service.get_price(usdc_token)
    
    # Verify
    assert price == Decimal("1.0")
    # Should NOT call katana service
    mock_katana_service.get_token_price.assert_not_called()

def test_get_price_error(mock_repository, mock_settings, mock_katana_service, mock_token):
    # Setup
    mock_katana_service.get_token_price.side_effect = Exception("DEX Error")
    service = TokenService(mock_repository, mock_settings, mock_katana_service)
    
    # Execute
    price = service.get_price(mock_token)
    
    # Verify
    assert price is None
