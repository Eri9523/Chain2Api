from abc import ABC, abstractmethod
from typing import Optional
from decimal import Decimal
from domain.models.token import Token


class ITokenRepository(ABC):
    """
    Port (interface) for token repository.
    This defines the contract for token data access.
    """
    
    @abstractmethod
    def get_balance(self, token: Token, address: str) -> Decimal:
        """Get token balance for an address"""
        pass
    
    @abstractmethod
    def get_total_supply(self, token: Token) -> Decimal:
        """Get total supply of a token"""
        pass
    
    @abstractmethod
    def get_token_info(self, token_address: str) -> dict:
        """Get token information (name, symbol, decimals)"""
        pass
    
    @abstractmethod
    def get_allowance(self, token: Token, owner: str, spender: str) -> Decimal:
        """Get allowance for a spender"""
        pass
