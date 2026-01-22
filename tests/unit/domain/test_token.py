import pytest
from decimal import Decimal
from domain.models.token import Token

def test_token_initialization():
    token = Token(symbol="TEST", address="0x123", decimals=18)
    assert token.symbol == "TEST"
    assert token.address == "0x123"
    assert token.decimals == 18

def test_token_validation():
    with pytest.raises(ValueError):
        Token(symbol="", address="0x123")
    
    with pytest.raises(ValueError):
        Token(symbol="TEST", address="")
        
    with pytest.raises(ValueError):
        Token(symbol="TEST", address="0x123", decimals=-1)

def test_format_amount():
    token = Token(symbol="TEST", address="0x123", decimals=18)
    # 1 token (10^18 wei)
    raw_amount = 1000000000000000000
    formatted = token.format_amount(raw_amount)
    assert formatted == Decimal("1.0")

def test_format_amount_decimals_6():
    token = Token(symbol="USDC", address="0x123", decimals=6)
    # 1 USDC (10^6 wei)
    raw_amount = 1000000
    formatted = token.format_amount(raw_amount)
    assert formatted == Decimal("1.0")

def test_to_raw_amount():
    token = Token(symbol="TEST", address="0x123", decimals=18)
    amount = Decimal("1.5")
    raw = token.to_raw_amount(amount)
    assert raw == 1500000000000000000
