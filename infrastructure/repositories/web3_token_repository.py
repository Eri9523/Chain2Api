from decimal import Decimal
from typing import Optional
from injector import inject
from web3 import Web3

from domain.models.token import Token
from domain.ports.token_repository import ITokenRepository
from abis.loader import load_abi


class Web3TokenRepository(ITokenRepository):
    """
    Adapter implementation of ITokenRepository using Web3.
    This is the infrastructure layer that interacts with the blockchain.
    """
    
    @inject
    def __init__(self, w3: Web3):
        """
        Initialize repository with Web3 instance.
        
        Args:
            w3: Web3 instance (injected)
        """
        self.w3 = w3
    
    def _get_contract(self, token: Token):
        """Get Web3 contract instance for a token"""
        checksum_address = self.w3.to_checksum_address(token.address)
        erc20_abi = load_abi('ERC20')
        return self.w3.eth.contract(address=checksum_address, abi=erc20_abi)
    
    def get_balance(self, token: Token, address: str) -> Decimal:
        """
        Get token balance for an address.
        
        Args:
            token: Token instance
            address: Wallet address
            
        Returns:
            Balance in human-readable format
        """
        contract = self._get_contract(token)
        checksum_address = self.w3.to_checksum_address(address)
        
        raw_balance = contract.functions.balanceOf(checksum_address).call()
        return token.format_amount(raw_balance)
    
    def get_total_supply(self, token: Token) -> Decimal:
        """
        Get total supply of a token.
        
        Args:
            token: Token instance
            
        Returns:
            Total supply in human-readable format
        """
        contract = self._get_contract(token)
        raw_supply = contract.functions.totalSupply().call()
        return token.format_amount(raw_supply)
    
    def get_token_info(self, token_address: str) -> dict:
        """
        Get token information from blockchain.
        
        Args:
            token_address: Token contract address
            
        Returns:
            Dictionary with name, symbol, and decimals
        """
        checksum_address = self.w3.to_checksum_address(token_address)
        erc20_abi = load_abi('ERC20')
        contract = self.w3.eth.contract(address=checksum_address, abi=erc20_abi)
        
        try:
            name = contract.functions.name().call()
        except Exception:
            name = None
            
        try:
            symbol = contract.functions.symbol().call()
        except Exception:
            symbol = None
            
        try:
            decimals = contract.functions.decimals().call()
        except Exception:
            decimals = 18  # Default to 18 if not available
        
        return {
            "name": name,
            "symbol": symbol,
            "decimals": decimals
        }
    
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
        contract = self._get_contract(token)
        owner_checksum = self.w3.to_checksum_address(owner)
        spender_checksum = self.w3.to_checksum_address(spender)
        
        raw_allowance = contract.functions.allowance(owner_checksum, spender_checksum).call()
        return token.format_amount(raw_allowance)
