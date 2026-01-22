"""
Example usage of the Token architecture.

This demonstrates how to use the TokenManager to interact with tokens
using a clean, fluent interface.
"""

from di import global_injector
from application.managers.token_manager import TokenManager


def main():
    """Example usage of token manager"""
    
    # Get TokenManager instance from DI container
    token_manager = global_injector.get(TokenManager)
    
    # Example wallet address (replace with actual address)
    wallet_address = "0x1234567890123456789012345678901234567890"
    
    # ============================================
    # Usage examples - exactly what you wanted!
    # ============================================
    
    # Get SLP balance
    slp_balance = token_manager.slp.getBalance(wallet_address)
    print(f"SLP Balance: {slp_balance}")
    
    # Get AXS price (placeholder for now)
    axs_price = token_manager.axs.getPrice()
    print(f"AXS Price: {axs_price}")
    
    # Get AXS balance
    axs_balance = token_manager.axs.getBalance(wallet_address)
    print(f"AXS Balance: {axs_balance}")
    
    # Get USDC total supply
    usdc_supply = token_manager.usdc.getTotalSupply()
    print(f"USDC Total Supply: {usdc_supply}")
    
    # Get RON balance
    ron_balance = token_manager.ron.getBalance(wallet_address)
    print(f"RON Balance: {ron_balance}")
    
    # Get token by symbol dynamically
    eth_token = token_manager.get_token('eth')
    eth_balance = eth_token.getBalance(wallet_address)
    print(f"ETH Balance: {eth_balance}")
    
    # Get all tokens
    all_tokens = token_manager.get_all_tokens()
    print(f"\nAvailable tokens: {list(all_tokens.keys())}")
    
    # Access token properties
    print(f"\nSLP Address: {token_manager.slp.address}")
    print(f"SLP Symbol: {token_manager.slp.symbol}")
    print(f"SLP Decimals: {token_manager.slp.decimals}")
    
    # Get allowance
    spender_address = "0x0987654321098765432109876543210987654321"
    allowance = token_manager.axs.getAllowance(wallet_address, spender_address)
    print(f"\nAXS Allowance: {allowance}")


if __name__ == "__main__":
    main()
