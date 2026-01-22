import pytest
from unittest.mock import Mock
from decimal import Decimal

from domain.models.token import Token
from domain.ports.token_repository import ITokenRepository
from settings.settings import Settings, TokenAddresses, ProviderSettings, SmartContractAddresses

@pytest.fixture
def mock_token():
    return Token(
        symbol="TEST",
        address="0x1234567890123456789012345678901234567890",
        name="Test Token",
        decimals=18
    )

@pytest.fixture
def mock_repository():
    return Mock(spec=ITokenRepository)

@pytest.fixture
def mock_settings():
    settings = Mock(spec=Settings)
    settings.tokens = Mock(spec=TokenAddresses)
    settings.tokens.SLP_ADDRESS = "0xSLP"
    settings.tokens.AXS_ADDRESS = "0xAXS"
    settings.tokens.USDC_ADDRESS = "0xUSDC"
    settings.tokens.ETH_ADDRESS = "0xETH"
    settings.tokens.BTC_ADDRESS = "0xBTC"
    settings.tokens.RON_ADDRESS = "0xRON"
    
    settings.contracts = Mock(spec=SmartContractAddresses)
    settings.contracts.KATANA_ADDRESS = "0xKATANA"
    
    settings.provider = Mock(spec=ProviderSettings)
    settings.provider.WEB3_HTTPS_PROVIDER_URL = "http://localhost:8545"
    
    return settings
