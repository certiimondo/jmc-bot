import discord
from discord.ext import commands
import os

# ------------------- SETTINGS -------------------
TOKEN = os.getenv("DISCORD_TOKEN")
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

async def send_embed(ctx, color, message, gif_pos=None, channel=None):
    """Helper function to send embed with optional GIF positions"""
    embed = discord.Embed(description=message, color=get_color(color))
    files = []

    # Determine which GIFs to attach based on gif_pos
    if gif_pos:
        gif_pos = gif_pos.lower()
        # Top-right thumbnail
        if "t" in gif_pos:
            file_thumb = discord.File("JMC_STUDIOS_Discord_PFP.gif", filename="thumb.gif")
            embed.set_thumbnail(url="attachment://thumb.gif")
            files.append(file_thumb)
        # Bottom full GIF
        if "b" in gif_pos:
            file_image = discord.File("JMC_STUDIOS_Discord_PFP.gif", filename="image.gif")
            embed.set_image(url="attachment://image.gif")
            files.append(file_image)

    target = channel if channel else ctx.channel

    if target.permissions_for(ctx.guild.me).send_messages:
        await target.send(embed=embed, files=files if files else None)
        await ctx.message.delete()
    else:
        await ctx.send(f"❌ I don't have permission to send messages in {target.mention}.", delete_after=5)

# !say command
@bot.command()
async def say(ctx, color: str, gif_pos: str = None, *, message):
    """Send an embed in current channel with optional GIF positions"""
    await send_embed(ctx, color, message, gif_pos)

# !post command
@bot.command()
async def post(ctx, channel: discord.TextChannel, color: str, gif_pos: str = None, *, message):
    """Send an embed in specific channel with optional GIF positions"""
    await send_embed(ctx, color, message, gif_pos, channel=channel)

# ------------------- ERROR HANDLING -------------------
@say.error
@post.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "❌ Missing argument! Usage:\n"
            "!say <color> [t/b/tb] <message>\n"
            "!post <channel> <color> [t/b/tb] <message>",
            delete_after=7
        )
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "❌ Invalid argument! Make sure to mention a valid text channel.",
            delete_after=7
        )
    else:
        await ctx.send(f"❌ An error occurred: {error}", delete_after=7)

# ------------------- RUN BOT -------------------
bot.run(TOKEN)
