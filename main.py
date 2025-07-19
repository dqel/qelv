from dotenv import load_dotenv
load_dotenv()
import discord
import os
from discord.ext import commands



# Replace 'YOUR_BOT_TOKEN' with your actual bot token
print("TOKEN:", os.getenv('DISCORD_BOT_TOKEN'))

intents = discord.Intents.all()  # Enable all intents for full functionality
PREFIX = 'qelv '
bot = commands.Bot(command_prefix=PREFIX, intents=intents)  # Initialize the bot
bot.help_command = None  # Completely disable the default help command

@bot.command(name='help', aliases=['commands'])
async def help_command(ctx):
    try:
        embed = discord.Embed(
            title="🤖 Qelv Bot Commands",
            description=f"Prefix: `{PREFIX}`\nMention me to see my prefix!",
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )
        
        # Commands category
        embed.add_field(
            name="📝 General Commands",
            value=f"`{PREFIX}help` - Shows this help message\n"
                  f"`{PREFIX}ping` - Check bot latency and status",
            inline=False
        )
        
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", 
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)
        print(f"Help command executed by {ctx.author}")
    except Exception as e:
        print(f"Error in help command: {e}")
        await ctx.send("There was an error displaying the help message. Please try again.")

@bot.event
async def on_message(message):
    # Ignore messages from bots
    if message.author.bot:
        return
    
    print(f"Message received: {message.content}")
    print(f"Mentions: {message.mentions}")
    
    # If the bot is mentioned and it's not a command
    if bot.user in message.mentions and not message.content.startswith(PREFIX):
        print("Bot was mentioned, sending prefix message")
        await message.channel.send(f'My prefix is `{PREFIX}`')
    
    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    
    # Set bot status to streaming
    activity = discord.Streaming(
        name="@qelv | qelv help",
        url="https://twitch.tv/qelv"  # Twitch URL required for streaming status
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)
    print("Bot status set to streaming: @qelv | qelv help")

@bot.command()
async def ping(ctx):
    import time
    import asyncio
    
    # Start timing for message latency
    start_time = time.perf_counter()
    
    # Send initial message
    message = await ctx.send("🏓 Calculating ping...")
    
    # Calculate message latency (time to send message)
    message_latency = (time.perf_counter() - start_time) * 1000
    
    # Calculate round trip time (edit message)
    edit_start = time.perf_counter()
    await message.edit(content="🏓 Calculating round trip...")
    round_trip_time = (time.perf_counter() - edit_start) * 1000
    
    # Get WebSocket latency (shard latency)
    websocket_latency = bot.latency * 1000
    
    # Calculate database latency (simulate database operation)
    db_start = time.perf_counter()
    # Simulate a database operation with a small async sleep
    await asyncio.sleep(0.001)  # 1ms simulated DB operation
    database_latency = (time.perf_counter() - db_start) * 1000
    
    # Calculate guild ping (time to fetch guild info)
    guild_start = time.perf_counter()
    guild = ctx.guild
    if guild:
        # Access guild properties to simulate guild ping
        guild_name = guild.name
        member_count = guild.member_count
    guild_latency = (time.perf_counter() - guild_start) * 1000
    
    # Create embed with all latency information
    embed = discord.Embed(
        title="🏓 Pong! Latency Information",
        color=0x00ff00,
        timestamp=ctx.message.created_at
    )
    
    embed.add_field(
        name="📨 Message Latency",
        value=f"`{message_latency:.2f}ms`",
        inline=True
    )
    
    embed.add_field(
        name="🔄 Round Trip Time",
        value=f"`{round_trip_time:.2f}ms`",
        inline=True
    )
    
    embed.add_field(
        name="🌐 WebSocket Latency",
        value=f"`{websocket_latency:.2f}ms`",
        inline=True
    )
    
    embed.add_field(
        name="💾 Database Latency",
        value=f"`{database_latency:.2f}ms`",
        inline=True
    )
    
    embed.add_field(
        name="🏰 Guild Ping",
        value=f"`{guild_latency:.2f}ms`",
        inline=True
    )
    
    # Add overall status based on latency
    if websocket_latency < 100:
        status = "🟢 Excellent"
    elif websocket_latency < 200:
        status = "🟡 Good"
    elif websocket_latency < 300:
        status = "🟠 Fair"
    else:
        status = "🔴 Poor"
    
    embed.add_field(
        name="📊 Connection Status",
        value=status,
        inline=True
    )
    
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    # Edit the message with the final embed
    await message.edit(content=None, embed=embed)

# Run the bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("Error: DISCORD_BOT_TOKEN not found in environment variables!")
        print("Please set your bot token in the .env file")
    else:
        print(f"Token length: {len(token)}")
        print(f"Token starts with: {token[:10]}...")
        print("Attempting to connect to Discord...")
        try:
            bot.run(token)
        except discord.LoginFailure as e:
            print(f"Error: Invalid bot token! Details: {e}")
            print("This usually means:")
            print("1. The token is incorrect or expired")
            print("2. The token was regenerated in Discord Developer Portal")
            print("3. The bot application is disabled")
        except discord.HTTPException as e:
            print(f"HTTP Error: {e}")
        except Exception as e:
            print(f"Unexpected error starting bot: {e}")
            print(f"Error type: {type(e).__name__}")
