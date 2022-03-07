from discord.ext import commands
from pymongo import MongoClient
import os


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def set_channel(self, ctx):
        """
        Command used to set channel in which bot can be used

        :param ctx: passing context of the command
        """
        mongo_client = MongoClient(os.getenv('MONGOURL'))
        db = mongo_client['Wordsy_Database']
        collection = db['wordsy_channels']
        check = collection.find_one({"_id": ctx.guild.id})
        if not check:
            query = {
                '_id': ctx.guild.id,
                'channel_id': ctx.channel.id
            }
            collection.insert_one(query)
            await ctx.send(f"Channel {ctx.channel.mention} was set for Wordsy BOT!")
        else:
            collection.update_one({"_id": ctx.guild.id},
                                  {"$set": {'_id': ctx.guild.id, 'channel_id': ctx.channel.id}})
            channel = ctx.guild.get_channel(check['channel_id'])
            try:
                await ctx.send(f"Channel {ctx.channel.mention} was set for Wordsy BOT! (was {channel.mention})")
            except:
                await ctx.send(f"Channel {ctx.channel.mention} was set for Wordsy BOT!")


def setup(client):
    client.add_cog(Settings(client))
