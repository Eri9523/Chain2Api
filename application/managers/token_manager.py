from injector import inject, singleton

from domain.models.token import Token
from domain.models.token_wrapper import TokenWrapper
from application.services.token_service import TokenService
from settings.settings import Settings


@singleton
class TokenManager:
    """
    Manager class that provides easy access to all configured tokens.
    This allows syntax like: token_manager.slp.getBalance(address)
    """
    
    @inject
    def __init__(self, settings: Settings, token_service: TokenService):
        """
        Initialize token manager with settings and service.
        
        Args:
            settings: Application settings (injected)
            token_service: Token service (injected)
        """
        self._settings = settings
        self._service = token_service
        self._tokens = {}
        self._initialize_tokens()
    
    def _initialize_tokens(self):
        """Initialize all tokens from settings"""
        # Create Token instances from settings
        token_configs = {
            'slp': {
                'symbol': 'SLP',
                'address': self._settings.tokens.SLP_ADDRESS,
                'name': 'Smooth Love Potion',
                'decimals': 0  # SLP has 0 decimals
            },
            'axs': {
                'symbol': 'AXS',
                'address': self._settings.tokens.AXS_ADDRESS,
                'name': 'Axie Infinity Shard',
                'decimals': 18
            },
            'usdc': {
                'symbol': 'USDC',
                'address': self._settings.tokens.USDC_ADDRESS,
                'name': 'USD Coin',
                'decimals': 6
            },
            'eth': {
                'symbol': 'ETH',
                'address': self._settings.tokens.ETH_ADDRESS,
                'name': 'Wrapped Ether',
                'decimals': 18
            },
            'btc': {
                'symbol': 'BTC',
                'address': self._settings.tokens.BTC_ADDRESS,
                'name': 'Wrapped Bitcoin',
                'decimals': 8
            },
            'ron': {
                'symbol': 'RON',
                'address': self._settings.tokens.RON_ADDRESS,
                'name': 'Ronin',
                'decimals': 18
            }
        }
        
        # Create TokenWrapper instances
        for key, config in token_configs.items():
            token = Token(
                symbol=config['symbol'],
                address=config['address'],
                name=config['name'],
                decimals=config['decimals']
            )
            self._tokens[key] = TokenWrapper(token, self._service)
    
    @property
    def slp(self) -> TokenWrapper:
        """Get SLP token wrapper"""
        return self._tokens['slp']
    
    @property
    def axs(self) -> TokenWrapper:
        """Get AXS token wrapper"""
        return self._tokens['axs']
    
    @property
    def usdc(self) -> TokenWrapper:
        """Get USDC token wrapper"""
        return self._tokens['usdc']
    
    @property
    def eth(self) -> TokenWrapper:
        """Get ETH token wrapper"""
        return self._tokens['eth']
    
    @property
    def btc(self) -> TokenWrapper:
        """Get BTC token wrapper"""
        return self._tokens['btc']
    
    @property
    def ron(self) -> TokenWrapper:
        """Get RON token wrapper"""
        return self._tokens['ron']
    
    def get_token(self, symbol: str) -> TokenWrapper:
        """
        Get token by symbol.
        
        Args:
            symbol: Token symbol (lowercase)
            
        Returns:
            TokenWrapper instance
            
        Raises:
            KeyError: If token not found
        """
        return self._tokens[symbol.lower()]
    
    def get_all_tokens(self) -> dict[str, TokenWrapper]:
        """
        Get all configured tokens.
        
        Returns:
            Dictionary of token symbol -> TokenWrapper
        """
        return self._tokens.copy()
