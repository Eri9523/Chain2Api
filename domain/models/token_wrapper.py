from decimal import Decimal
from typing import Optional

from domain.models.token import Token
from application.services.token_service import TokenService


class TokenWrapper:
    """
    Wrapper class that provides a fluent interface for token operations.
    This allows syntax like: token.slp.getBalance(address)
    """
    
    def __init__(self, token: Token, service: TokenService):
        """
        Initialize wrapper with token and service.
        
        Args:
            token: Token domain model
            service: Token service for operations
        """
        self._token = token
        self._service = service
    
    @property
    def symbol(self) -> str:
        """Get token symbol"""
        return self._token.symbol
    
    @property
    def address(self) -> str:
        """Get token address"""
        return self._token.address
    
    @property
    def decimals(self) -> int:
        """Get token decimals"""
        return self._token.decimals
    
    def getBalance(self, address: str) -> Decimal:
        """
        Get token balance for an address.
        
        Args:
            address: Wallet address
            
        Returns:
            Balance in human-readable format
        """
        return self._service.get_balance(self._token, address)
    
    def getTotalSupply(self) -> Decimal:
        """
        Get total supply of the token.
        
        Returns:
            Total supply in human-readable format
        """
        return self._service.get_total_supply(self._token)
    
    def getPrice(self) -> Optional[Decimal]:
        """
        Get token price in USD.
        
        Returns:
            Token price or None if not available
        """
        return self._service.get_price(self._token)
    
    def getAllowance(self, owner: str, spender: str) -> Decimal:
        """
        Get allowance for a spender.
        
        Args:
            owner: Owner address
            spender: Spender address
            
        Returns:
            Allowance in human-readable format
        """
        return self._service.get_allowance(self._token, owner, spender)
    
    def __repr__(self) -> str:
        return f"TokenWrapper({self._token.symbol} - {self._token.address})"
