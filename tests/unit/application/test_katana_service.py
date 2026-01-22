import pytest
from unittest.mock import Mock
from decimal import Decimal
from web3 import Web3

from application.services.katana_service import KatanaService

@pytest.fixture
def mock_web3():
    w3 = Mock(spec=Web3)
    w3.eth = Mock()
    w3.to_checksum_address = lambda x: x
    return w3

def test_get_token_price(mock_web3, mock_settings):
    # Setup Contracts
    factory_contract = Mock()
    pair_contract = Mock()
    token0_contract = Mock()
    token1_contract = Mock()
    
    # Mock Web3 contract creation sequence
    # 1. Factory -> 2. Pair -> 3. Token0 -> 4. Token1
    mock_web3.eth.contract.side_effect = [
        factory_contract, 
        pair_contract, 
        token0_contract, 
        token1_contract
    ]
    
    # Mock Factory: getPair returns a valid address
    factory_contract.functions.getPair.return_value.call.return_value = "0xPair"
    
    # Mock Pair: token0, token1, reserves
    # Let's say Token A (Base) is token0, Token B (USDC) is token1
    token_a_addr = "0xTokenA"
    token_b_addr = "0xTokenB"
    
    pair_contract.functions.token0.return_value.call.return_value = token_a_addr
    pair_contract.functions.token1.return_value.call.return_value = token_b_addr
    
    # Reserves: 10 TokenA, 20 TokenB (Price should be 2.0)
    # Assuming both have 18 decimals for simplicity first
    reserve0 = 10 * 10**18
    reserve1 = 20 * 10**18
    pair_contract.functions.getReserves.return_value.call.return_value = [reserve0, reserve1, 0]
    
    # Mock Decimals
    token0_contract.functions.decimals.return_value.call.return_value = 18
    token1_contract.functions.decimals.return_value.call.return_value = 18
    
    service = KatanaService(mock_web3, mock_settings)
    
    # Execute
    price = service.get_token_price(token_a_addr, token_b_addr)
    
    # Verify
    # Price = (20 / 10) = 2.0
    assert price == 2.0

def test_get_token_price_different_decimals(mock_web3, mock_settings):
    # Test with USDC (6 decimals) and WETH (18 decimals)
    # Price of ETH in USDC = 3000
    
    factory_contract = Mock()
    pair_contract = Mock()
    token0_contract = Mock()
    token1_contract = Mock()
    
    mock_web3.eth.contract.side_effect = [factory_contract, pair_contract, token0_contract, token1_contract]
    factory_contract.functions.getPair.return_value.call.return_value = "0xPair"
    
    weth_addr = "0xWETH"
    usdc_addr = "0xUSDC"
    
    # WETH is token0, USDC is token1
    pair_contract.functions.token0.return_value.call.return_value = weth_addr
    pair_contract.functions.token1.return_value.call.return_value = usdc_addr
    
    # Reserves: 1 WETH, 3000 USDC
    reserve_weth = 1 * 10**18
    reserve_usdc = 3000 * 10**6
    
    pair_contract.functions.getReserves.return_value.call.return_value = [reserve_weth, reserve_usdc, 0]
    
    # Decimals
    token0_contract.functions.decimals.return_value.call.return_value = 18 # WETH
    token1_contract.functions.decimals.return_value.call.return_value = 6  # USDC
    
    service = KatanaService(mock_web3, mock_settings)
    
    price = service.get_token_price(weth_addr, usdc_addr)
    
    # Price = (3000*10^6 / 10^6) / (1*10^18 / 10^18) = 3000 / 1 = 3000
    assert price == 3000.0

def test_pair_not_exists(mock_web3, mock_settings):
    factory_contract = Mock()
    mock_web3.eth.contract.return_value = factory_contract
    
    # Return zero address
    factory_contract.functions.getPair.return_value.call.return_value = "0x0000000000000000000000000000000000000000"
    
    service = KatanaService(mock_web3, mock_settings)
    
    with pytest.raises(ValueError, match="Pair does not exist"):
        service.get_token_price("0xA", "0xB")
