from dotenv import load_dotenv
load_dotenv()
import os
import sys

def test_token():
    print("=== Discord Bot Token Test ===")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✓ .env file found")
    else:
        print("✗ .env file not found")
        return
    
    # Check if token is loaded
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        print("✓ Token loaded from environment")
        print(f"Token length: {len(token)}")
        print(f"Token format: {token[:10]}...{token[-10:]}")
        
        # Check token format
        parts = token.split('.')
        if len(parts) == 3:
            print("✓ Token has correct format (3 parts)")
        else:
            print(f"✗ Token has incorrect format ({len(parts)} parts)")
            
        # Check for whitespace
        if token.strip() == token:
            print("✓ No leading/trailing whitespace")
        else:
            print("✗ Token has whitespace issues")
            
    else:
        print("✗ Token not found in environment")
    
    # Test discord.py import
    try:
        import discord
        print(f"✓ discord.py imported successfully (version: {discord.__version__})")
    except ImportError as e:
        print(f"✗ Failed to import discord.py: {e}")
        print("Run: pip install discord.py")
        return
    
    # Test basic connection attempt
    if token:
        print("\n=== Testing Connection ===")
        try:
            import asyncio
            
            async def test_connection():
                try:
                    client = discord.Client(intents=discord.Intents.default())
                    
                    @client.event
                    async def on_ready():
                        print(f"✓ Successfully connected as {client.user}")
                        await client.close()
                    
                    await client.start(token)
                    
                except discord.LoginFailure:
                    print("✗ Invalid token - LoginFailure")
                    print("Possible causes:")
                    print("  1. Token is incorrect")
                    print("  2. Token was regenerated")
                    print("  3. Bot is disabled")
                except discord.HTTPException as e:
                    print(f"✗ HTTP Error: {e}")
                except Exception as e:
                    print(f"✗ Unexpected error: {e}")
            
            asyncio.run(test_connection())
            
        except Exception as e:
            print(f"✗ Connection test failed: {e}")

if __name__ == "__main__":
    test_token()
