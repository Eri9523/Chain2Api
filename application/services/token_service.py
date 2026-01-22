from decimal import Decimal
from typing import Optional
from injector import inject, singleton

from domain.models.token import Token
from domain.ports.token_repository import ITokenRepository
from settings.settings import Settings
from application.services.katana_service import KatanaService

@singleton
class TokenService:
    """
    Application service for token operations.
    This contains the business logic for working with tokens.
    """
    
    @inject
    def __init__(self, repository: ITokenRepository, settings: Settings, katana_service: KatanaService):
        """
        Initialize service with repository and settings.
        
        Args:
            repository: Token repository implementation (injected)
            settings: Application settings (injected)
            katana_service: Katana DEX service (injected)
        """
        self.repository = repository
        self.settings = settings
        self.katana_service = katana_service
    
    def get_balance(self, token: Token, address: str) -> Decimal:
        """
        Get token balance for an address.
        
        Args:
            token: Token instance
            address: Wallet address
            
        Returns:
            Balance in human-readable format
        """
        return self.repository.get_balance(token, address)
    
    def get_total_supply(self, token: Token) -> Decimal:
        """
        Get total supply of a token.
        
        Args:
            token: Token instance
            
        Returns:
            Total supply in human-readable format
        """
        return self.repository.get_total_supply(token)
    
    def get_allowance(self, token: Token, owner: str, spender: str) -> Decimal:
        """
        Get allowance for a spender.
        
        Args:
            token: Token instance
            owner: Owner address
            spender: Spender address
            
        Returns:
            Allowance in human-readable format
        """
        return self.repository.get_allowance(token, owner, spender)
    
    def get_price(self, token: Token) -> Optional[Decimal]:
        """
        Get token price in USDC using KatanaService.
        
        Args:
            token: Token instance
            
        Returns:
            Token price in USD (or None if not available)
        """
        # If token is USDC, price is 1
        if token.address.lower() == self.settings.tokens.USDC_ADDRESS.lower():
            return Decimal(1)

        try:
            # Calculate price against USDC
            price_float = self.katana_service.get_token_price(token.address, self.settings.tokens.USDC_ADDRESS)
            return Decimal(str(price_float))
        except Exception as e:
            print(f"Error fetching price for {token.symbol}: {e}")
            return None
