import discord  # main packages
from discord.ext import commands
import random  # utility packages
import os
import json

intents = discord.Intents().all()  # Making sure the bot has all the permissions
intents.members = True
client = commands.Bot(command_prefix='*', intents=intents, help_command=None)  # Initialize bot

client.load_extension("settings")
client.load_extension("game")


@client.event
async def on_ready():
    """ Event handler that is called when bot is turned on. """
    print("Bot's ready")
    await client.change_presence(  # change the bot's description on Discord member list
        activity=discord.Activity(
            type=discord.ActivityType.watching,  # get the "is watching ..." format
            name="*wordsy to start!"
        )
    )


@client.command()
async def help(ctx):
    embed = discord.Embed(
        color=0x11f80d,
        title="📜 DISCORD WORDSY 📜",
        description="Basic commands"
    )
    embed.add_field(
        name="🖥 MAIN COMMANDS",
        value="""
        `*wordsy`
        Main command used to start the game.
        """,
        inline=False
    )
    embed.add_field(
        name="⚙ SETTINGS",
        value="""
        `*set_channel`
        Use this command in specific channel to prevent usage of Discord Wordsy in other channels
        """,
        inline=False
    )
    file = discord.File('Media/w2.png', filename="image.png")
    embed.set_thumbnail(url="attachment://image.png")
    await ctx.send(embed=embed, file=file)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MaxConcurrencyReached):  # called when you don't have permission to use that command.
        await ctx.send(f"{ctx.author.mention}, finish the game before starting new one!")
        return

client.run(os.getenv('TOKEN'))
