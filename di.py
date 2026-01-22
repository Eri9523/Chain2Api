from injector import Injector, singleton
from web3 import Web3

from settings.settings import Settings, settings_instance
from domain.ports.token_repository import ITokenRepository
from infrastructure.repositories.web3_token_repository import Web3TokenRepository
from application.services.token_service import TokenService
from application.managers.token_manager import TokenManager
from application.services.katana_service import KatanaService


def create_application_injector() -> Injector:
    """
    Create and configure the application's dependency injection container.
    
    Returns:
        Configured Injector instance
    """
    _injector = Injector(auto_bind=True)
    
    # Bind settings as singleton
    _injector.binder.bind(Settings, to=settings_instance, scope=singleton)
    
    # Create and bind Web3 instance as singleton
    w3 = Web3(Web3.HTTPProvider(
        settings_instance.provider.WEB3_HTTPS_PROVIDER_URL,
        request_kwargs={'timeout': 60}
    ))
    _injector.binder.bind(Web3, to=w3, scope=singleton)
    
    # Bind repository interface to implementation
    _injector.binder.bind(ITokenRepository, to=Web3TokenRepository, scope=singleton)
    
    # Services will be auto-bound as singletons
    _injector.binder.bind(TokenService, scope=singleton)
    _injector.binder.bind(TokenManager, scope=singleton)
    _injector.binder.bind(KatanaService, scope=singleton)
    
    return _injector


global_injector: Injector = create_application_injector()

