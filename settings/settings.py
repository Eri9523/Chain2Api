from pydantic import BaseModel
import os
from dotenv import dotenv_values

class ProviderSettings(BaseModel):
    WEB3_HTTPS_PROVIDER_URL: str

class TokenAddresses(BaseModel):
    SLP_ADDRESS: str
    AXS_ADDRESS: str
    USDC_ADDRESS: str
    ETH_ADDRESS: str
    BTC_ADDRESS: str
    RON_ADDRESS: str

class SmartContractAddresses(BaseModel):
    MARKETPLACE_ADDRESS: str
    APP_ORDER_ADDRESS: str
    MAVIS_MARKET_ADDRESS: str
    AXIE_ADDRESS: str
    KATANA_ADDRESS: str
    MARKETPLACE_MULTISEND_ADDRESS: str

class Settings(BaseModel):
    provider: ProviderSettings
    tokens: TokenAddresses
    contracts: SmartContractAddresses
    DEBUG_ENABLED: bool

def load_settings() -> Settings:
    # Look for .env in project root (parent of settings directory)
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    config = dotenv_values(dotenv_path=env_path)
    return Settings(
        provider=ProviderSettings(
            WEB3_HTTPS_PROVIDER_URL=config['WEB3_HTTPS_PROVIDER_URL'],
        ),
        tokens=TokenAddresses(
            SLP_ADDRESS=config['SLP_ADDRESS'],
            AXS_ADDRESS=config['AXS_ADDRESS'],
            USDC_ADDRESS=config['USDC_ADDRESS'],
            ETH_ADDRESS=config['WETH_ADDRESS'],
            BTC_ADDRESS=config['BTC_ADDRESS'],
            RON_ADDRESS=config['RON_ADDRESS'],
        ),
        contracts=SmartContractAddresses(
            MARKETPLACE_ADDRESS=config['MARKETPLACE_ADDRESS'],
            APP_ORDER_ADDRESS=config['APP_ORDER_ADDRESS'],
            MAVIS_MARKET_ADDRESS=config['MAVIS_MARKET_ADDRESS'],
            AXIE_ADDRESS=config['AXIE_ADDRESS'],
            KATANA_ADDRESS=config['KATANA_ADDRESS'],
            MARKETPLACE_MULTISEND_ADDRESS=config['MARKETPLACE_MULTISEND_ADDRESS'],
        ),
        DEBUG_ENABLED=config['DEBUG_ENABLED'].lower() == 'true'
    )

settings_instance = load_settings()
