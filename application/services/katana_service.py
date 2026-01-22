from decimal import Decimal
from injector import inject, singleton
from web3 import Web3

from abis.loader import RESERVES_ABI, ERC20_ABI, KATANA_FACTORY_ABI
from settings.settings import Settings

@singleton
class KatanaService:
    """
    Service for interacting with Katana DEX (Ronin's AMM).
    Handles price fetching and liquidity pool interactions.
    """

    @inject
    def __init__(self, w3: Web3, settings: Settings):
        """
        Initialize Katana service.
        
        Args:
            w3: Web3 instance (injected)
            settings: Application settings (injected)
        """
        self.w3 = w3
        self.settings = settings
        # Ensure factory address is checksummed
        self._factory_address = self.w3.to_checksum_address(self.settings.contracts.KATANA_ADDRESS)

    def get_token_price(self, token_a_address: str, token_b_address: str) -> float:
        """
        Get price of token_a in terms of token_b (quote token).
        
        Args:
            token_a_address: Address of the base token
            token_b_address: Address of the quote token (e.g. USDC)
            
        Returns:
            Price as float
            
        Raises:
            ValueError: If pair doesn't exist
        """
        token_a = self.w3.to_checksum_address(token_a_address)
        token_b = self.w3.to_checksum_address(token_b_address)

        # Get Factory Contract
        factory_contract = self.w3.eth.contract(address=self._factory_address, abi=KATANA_FACTORY_ABI)
        
        # Get Pair Address
        pair_address = factory_contract.functions.getPair(token_a, token_b).call()

        if pair_address == "0x0000000000000000000000000000000000000000":
            raise ValueError(f"Pair does not exist for {token_a} and {token_b}")

        # Get Reserves
        pair_contract = self.w3.eth.contract(address=pair_address, abi=RESERVES_ABI)
        token0 = pair_contract.functions.token0().call()
        token1 = pair_contract.functions.token1().call()
        reserve0, reserve1, _ = pair_contract.functions.getReserves().call()

        reserve0 = Decimal(reserve0)
        reserve1 = Decimal(reserve1)

        # Get Decimals
        # TODO: Consider caching these calls or passing Token objects to avoid RPC calls
        token0_contract = self.w3.eth.contract(address=token0, abi=ERC20_ABI)
        token1_contract = self.w3.eth.contract(address=token1, abi=ERC20_ABI)
        token0_decimals = token0_contract.functions.decimals().call()
        token1_decimals = token1_contract.functions.decimals().call()

        # Calculate Price
        if token0 == token_a:
            token_a_reserve = reserve0
            token_b_reserve = reserve1
            token_a_decimals = token0_decimals
            token_b_decimals = token1_decimals
        else:
            token_a_reserve = reserve1
            token_b_reserve = reserve0
            token_a_decimals = token1_decimals
            token_b_decimals = token0_decimals

        if token_a_reserve == 0:
            return 0.0

        # Price = (Reserve B / 10^Decimals B) / (Reserve A / 10^Decimals A)
        price = (token_b_reserve / Decimal(10 ** token_b_decimals)) / (token_a_reserve / Decimal(10 ** token_a_decimals))
        return float(price)
