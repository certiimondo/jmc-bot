import discord
from discord.ext import commands
import os

# ------------------- SETTINGS -------------------
TOKEN = os.getenv("DISCORD_TOKEN")  # Set this in Railway or your .env
intents = discord.Intents.default()
intents.message_content = True  # Needed to read command messages
bot = commands.Bot(command_prefix="!", intents=intents)
# ------------------------------------------------

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("Bot is ready to use!")

# ------------------- COMMANDS -------------------

@bot.command()
async def say(ctx, *, message):
    """Bot posts a message in the current channel only."""
    if ctx.channel.permissions_for(ctx.guild.me).send_messages:
        await ctx.send(message)       # Bot sends the message
        await ctx.message.delete()    # Delete your command
    else:
        await ctx.send("❌ I don't have permission to send messages here!", delete_after=5)

@bot.command()
async def post(ctx, channel: discord.TextChannel, *, message):
    """
    Bot posts a message in a specific channel.
    You can mention the channel: !post #general Hello!
    """
    # Check if bot has permission to send messages
    if channel.permissions_for(ctx.guild.me).send_messages:
        await channel.send(message)
        await ctx.message.delete()
    else:
        await ctx.send(f"❌ I don't have permission to send messages in {channel.mention}.", delete_after=5)

# ------------------- ERROR HANDLING -------------------

@say.error
@post.error
async def command_error(ctx, error):
    """Handle missing arguments or bad arguments."""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing argument! Check your command usage.", delete_after=5)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument! Make sure to mention a valid text channel.", delete_after=5)
    else:
        # Catch-all for unexpected errors
        await ctx.send(f"❌ An error occurred: {error}", delete_after=5)

# ------------------- RUN BOT -------------------
bot.run(TOKEN)
