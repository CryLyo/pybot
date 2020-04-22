import discord
from discord.ext import commands
from Shared_Classes import data, Queue
import emoji
# The magic condition: str(ctx.emoji) == emoji.emojize(":one:",use_aliases=True)


class Question_Manager(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command("question", aliases=("ask","TA"))
    async def ask_question(self,ctx,*question):
        question = " ".join(question)
        author = ctx.author
        channel = ctx.channel
        guild = ctx.guild

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,ctx):
        # We don't care about it if it's the bot
        if ctx.user_id == self.client.user.id:
            return




def setup(client):
    client.add_cog(Question_Manager(client))
