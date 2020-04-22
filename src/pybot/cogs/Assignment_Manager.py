import discord
from discord.ext import commands
from Shared_Classes import data, Queue

class Assignment_Manager(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("ready", aliases=("handin","hand_in","hand-in"))
    async def assignment_handin(self,ctx):
        pass


def setup(client):
    client.add_cog(Assignment_Manager(client))
