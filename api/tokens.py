from fastapi import APIRouter, Depends, HTTPException, Path, Request
from injector import Injector, inject
from typing import Dict, List, Any
from pydantic import BaseModel

from application.managers.token_manager import TokenManager
from domain.models.token_wrapper import TokenWrapper

router = APIRouter(prefix="/tokens", tags=["Tokens"])

class TokenInfo(BaseModel):
    symbol: str
    name: str
    address: str
    decimals: int

class TokenBalance(BaseModel):
    symbol: str
    address: str
    balance: float

class TokenPrice(BaseModel):
    symbol: str
    price_usdc: float

class TokenSupply(BaseModel):
    symbol: str
    total_supply: float

def get_token_manager(request: Request) -> TokenManager:
    return request.state.injector.get(TokenManager)

@router.get("/", response_model=List[TokenInfo])
def list_tokens(tm: TokenManager = Depends(get_token_manager)):
    """List all configured tokens."""
    tokens = tm.get_all_tokens()
    result = []
    for symbol, wrapper in tokens.items():
        result.append(TokenInfo(
            symbol=wrapper.symbol,
            name=wrapper._token.name or symbol.upper(),
            address=wrapper.address,
            decimals=wrapper.decimals
        ))
    return result

@router.get("/{symbol}/balance/{address}", response_model=TokenBalance)
def get_balance(
    symbol: str = Path(..., description="Token symbol (e.g., slp, axs)"),
    address: str = Path(..., description="Wallet address"),
    tm: TokenManager = Depends(get_token_manager)
):
    """Get token balance for a specific address."""
    try:
        token = tm.get_token(symbol)
        balance = token.getBalance(address)
        return TokenBalance(
            symbol=token.symbol,
            address=address,
            balance=float(balance)
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Token '{symbol}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/price", response_model=TokenPrice)
def get_price(
    symbol: str = Path(..., description="Token symbol (e.g., slp, axs)"),
    tm: TokenManager = Depends(get_token_manager)
):
    """Get current token price in USDC."""
    try:
        token = tm.get_token(symbol)
        price = token.getPrice()
        if price is None:
             raise HTTPException(status_code=404, detail=f"Price not available for '{symbol}'")
        return TokenPrice(
            symbol=token.symbol,
            price_usdc=float(price)
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Token '{symbol}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{symbol}/supply", response_model=TokenSupply)
def get_supply(
    symbol: str = Path(..., description="Token symbol (e.g., slp, axs)"),
    tm: TokenManager = Depends(get_token_manager)
):
    """Get total supply of the token."""
    try:
        token = tm.get_token(symbol)
        supply = token.getTotalSupply()
        return TokenSupply(
            symbol=token.symbol,
            total_supply=float(supply)
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Token '{symbol}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
