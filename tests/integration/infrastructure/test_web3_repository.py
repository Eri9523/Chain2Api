import pytest
from unittest.mock import Mock, MagicMock
from decimal import Decimal
from web3 import Web3

from infrastructure.repositories.web3_token_repository import Web3TokenRepository

@pytest.fixture
def mock_web3():
    w3 = Mock(spec=Web3)
    w3.eth = Mock()
    w3.to_checksum_address = lambda x: x  # Identity function for simplicity
    return w3

@pytest.fixture
def mock_contract():
    contract = Mock()
    contract.functions = Mock()
    return contract

def test_get_balance(mock_web3, mock_contract, mock_token):
    # Setup
    mock_web3.eth.contract.return_value = mock_contract
    # Mock balanceOf call returning 1 token (10^18 wei)
    mock_contract.functions.balanceOf.return_value.call.return_value = 1000000000000000000
    
    repo = Web3TokenRepository(mock_web3)
    
    # Execute
    balance = repo.get_balance(mock_token, "0xUser")
    
    # Verify
    assert balance == Decimal("1.0")
    mock_contract.functions.balanceOf.assert_called()

def test_get_total_supply(mock_web3, mock_contract, mock_token):
    # Setup
    mock_web3.eth.contract.return_value = mock_contract
    # Mock totalSupply returning 1M tokens
    mock_contract.functions.totalSupply.return_value.call.return_value = 1000000 * 10**18
    
    repo = Web3TokenRepository(mock_web3)
    
    # Execute
    supply = repo.get_total_supply(mock_token)
    
    # Verify
    assert supply == Decimal("1000000")

def test_get_allowance(mock_web3, mock_contract, mock_token):
    # Setup
    mock_web3.eth.contract.return_value = mock_contract
    mock_contract.functions.allowance.return_value.call.return_value = 500 * 10**18
    
    repo = Web3TokenRepository(mock_web3)
    
    # Execute
    allowance = repo.get_allowance(mock_token, "0xOwner", "0xSpender")
    
    # Verify
    assert allowance == Decimal("500")

def test_get_token_info(mock_web3, mock_contract):
    # Setup
    mock_web3.eth.contract.return_value = mock_contract
    mock_contract.functions.name.return_value.call.return_value = "Test Token"
    mock_contract.functions.symbol.return_value.call.return_value = "TEST"
    mock_contract.functions.decimals.return_value.call.return_value = 18
    
    repo = Web3TokenRepository(mock_web3)
    
    # Execute
    info = repo.get_token_info("0xToken")
    
    # Verify
    assert info["name"] == "Test Token"
    assert info["symbol"] == "TEST"
    assert info["decimals"] == 18
