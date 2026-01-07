import discord
from discord.ext import commands

# ------------------- SETTINGS -------------------
import os
TOKEN = os.getenv("DISCORD_TOKEN")  # <-- Replace this with your bot token
intents = discord.Intents.default()
intents.message_content = True  # Needed to read command messages
bot = commands.Bot(command_prefix="!", intents=intents)
# ------------------------------------------------

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("Bot is ready to use!")

# Command to post in the current channel
@bot.command()
async def say(ctx, *, message):
    """Posts the message in the current channel"""
    await ctx.send(message)

# Command to post in a specific channel by ID
@bot.command()
async def post(ctx, channel_id: int, *, message):
    """Posts the message in a specific channel"""
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        await ctx.send("Channel not found! Make sure the ID is correct.")

# Run the bot
bot.run(TOKEN)
