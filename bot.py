import discord
from discord.ext import commands
import os

# ------------------- SETTINGS -------------------
TOKEN = os.getenv("DISCORD_TOKEN")  # Make sure this is set in Railway or your .env
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
# ------------------------------------------------

# Helper function to convert color names to discord.Color
def get_color(color_name: str):
    color_name = color_name.lower()
    colors = {
        "default": discord.Color.default(),
        "teal": discord.Color.teal(),
        "dark_teal": discord.Color.dark_teal(),
        "green": discord.Color.green(),
        "dark_green": discord.Color.dark_green(),
        "blue": discord.Color.blue(),
        "dark_blue": discord.Color.dark_blue(),
        "purple": discord.Color.purple(),
        "dark_purple": discord.Color.dark_purple(),
        "magenta": discord.Color.magenta(),
        "dark_magenta": discord.Color.dark_magenta(),
        "gold": discord.Color.gold(),
        "dark_gold": discord.Color.dark_gold(),
        "orange": discord.Color.orange(),
        "dark_orange": discord.Color.dark_orange(),
        "red": discord.Color.red(),
        "dark_red": discord.Color.dark_red(),
        "lighter_grey": discord.Color.lighter_grey(),
        "dark_grey": discord.Color.dark_grey(),
        "light_grey": discord.Color.light_grey(),
        "darker_grey": discord.Color.darker_grey(),
        "blurple": discord.Color.blurple(),
        "greyple": discord.Color.greyple(),
    }
    return colors.get(color_name, discord.Color.green())  # default green if unknown

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("Bot is ready to use!")

# ------------------- COMMANDS -------------------

@bot.command()
async def say(ctx, color: str, *, message):
    """Bot posts an embed in the current channel with dynamic color and GIF"""
    embed_color = get_color(color)
    embed = discord.Embed(
        description=message,
        color=embed_color
    )
    file = discord.File("JMC_STUDIOS_Discord_PFP.gif", filename="gif.gif")
    embed.set_image(url="attachment://gif.gif")

    if ctx.channel.permissions_for(ctx.guild.me).send_messages:
        await ctx.send(embed=embed, file=file)
        await ctx.message.delete()
    else:
        await ctx.send("❌ I don't have permission to send messages here!", delete_after=5)

@bot.command()
async def post(ctx, channel: discord.TextChannel, color: str, *, message):
    """Bot posts an embed in a specific channel with dynamic color and GIF"""
    embed_color = get_color(color)
    embed = discord.Embed(
        description=message,
        color=embed_color
    )
    file = discord.File("JMC_STUDIOS_Discord_PFP.gif", filename="gif.gif")
    embed.set_image(url="attachment://gif.gif")

    if channel.permissions_for(ctx.guild.me).send_messages:
        await channel.send(embed=embed, file=file)
        await ctx.message.delete()
    else:
        await ctx.send(f"❌ I don't have permission to send messages in {channel.mention}.", delete_after=5)

# ------------------- ERROR HANDLING -------------------

@say.error
@post.error
async def command_error(ctx, error):
    """Handle missing arguments or bad arguments."""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Missing argument! Usage:\n!say <color> <message>\n!post <channel> <color> <message>", delete_after=7)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument! Make sure to mention a valid text channel.", delete_after=7)
    else:
        await ctx.send(f"❌ An error occurred: {error}", delete_after=7)

# ------------------- RUN BOT -------------------
bot.run(TOKEN)
