import discord  # main packages
from discord.ext import commands
import json


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def set_channel(self, ctx):
        """
        Command used to set channel in which bot can be used

        :param ctx: passing context of the command
        """
        with open("JsonData/guild_configs.json") as guild_configs_file:  # getting .json file that contains server's config
            guild_config = guild_configs_file.read()
            guild_config_dict = json.loads(guild_config)
            guild_configs_file.close()

        guild_config_dict[ctx.guild.id] = ctx.channel.id  # assign channel's id to specific server's id

        with open("JsonData/guild_configs.json", 'w') as guild_configs_file:  # write collected ids to .json file
            json.dump(guild_config_dict, guild_configs_file, indent=6)
            guild_configs_file.close()

        await ctx.send(f"{ctx.channel.mention} was set for Discord Wordsy")


def setup(client):
    client.add_cog(Settings(client))
