from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Token:
    """
    Domain model representing an ERC20 token.
    This is a pure domain object with no infrastructure dependencies.
    """
    symbol: str
    address: str
    name: Optional[str] = None
    decimals: int = 18
    
    def __post_init__(self):
        """Validate token data"""
        if not self.address:
            raise ValueError("Token address cannot be empty")
        if not self.symbol:
            raise ValueError("Token symbol cannot be empty")
        if self.decimals < 0:
            raise ValueError("Token decimals must be non-negative")
    
    def format_amount(self, raw_amount: int) -> Decimal:
        """
        Convert raw token amount to human-readable decimal format.
        
        Args:
            raw_amount: Raw amount in smallest unit (e.g., wei for ETH)
            
        Returns:
            Decimal representation of the amount
        """
        return Decimal(raw_amount) / Decimal(10 ** self.decimals)
    
    def to_raw_amount(self, amount: Decimal) -> int:
        """
        Convert human-readable amount to raw token amount.
        
        Args:
            amount: Human-readable amount
            
        Returns:
            Raw amount in smallest unit
        """
        return int(amount * Decimal(10 ** self.decimals))
