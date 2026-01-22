"""
Quick test script to verify the token architecture works correctly.
"""

from di import global_injector
from application.managers.token_manager import TokenManager


def test_token_manager():
    """Test that TokenManager is properly configured"""
    print("🔧 Testing Token Architecture...\n")
    
    # Get TokenManager from DI container
    print("1. Getting TokenManager from DI container...")
    token_manager = global_injector.get(TokenManager)
    print("   ✅ TokenManager created successfully\n")
    
    # Test token properties
    print("2. Testing token properties...")
    print(f"   SLP Symbol: {token_manager.slp.symbol}")
    print(f"   SLP Address: {token_manager.slp.address}")
    print(f"   SLP Decimals: {token_manager.slp.decimals}")
    print("   ✅ Token properties accessible\n")
    
    # Test all tokens are available
    print("3. Testing all configured tokens...")
    all_tokens = token_manager.get_all_tokens()
    for symbol, token in all_tokens.items():
        print(f"   {symbol.upper()}: {token.address}")
    print("   ✅ All tokens configured\n")
    
    # Test dynamic access
    print("4. Testing dynamic token access...")
    axs_token = token_manager.get_token('axs')
    print(f"   AXS via get_token(): {axs_token.symbol} - {axs_token.address}")
    print("   ✅ Dynamic access works\n")
    
    print("✨ All tests passed! Architecture is working correctly.\n")
    print("📝 Usage example:")
    print("   from di import global_injector")
    print("   from services.token_manager import TokenManager")
    print("   ")
    print("   token_manager = global_injector.get(TokenManager)")
    print("   balance = token_manager.slp.getBalance('0x123...')")
    print("   price = token_manager.axs.getPrice()")


if __name__ == "__main__":
    try:
        test_token_manager()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
