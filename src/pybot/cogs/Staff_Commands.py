import discord
from discord.ext import commands
from Shared_Classes import data, Queue

class Staff_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Staff_Commands(client))
