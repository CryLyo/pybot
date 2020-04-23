import discord
from discord.ext import commands
from Shared_Classes import data, Queue
import emoji


class Assignment_Manager(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def is_TA(self,ctx):
        for guild in self.client.guilds:
            member = guild.get_member(ctx.author.id)
            if member.guild_permissions.administrator:
                return True
        return False

    async def connect_user(self, queue):
        user = queue.current
        target_guild = queue.guild
        target_user = queue.owner
        guild_obj = None
        for guild in self.client.guilds:
            if guild.id == data.settings["Guilds"][target_guild]:
                guild_obj = guild
                break
        if not guild_obj:
            return

        target = guild_obj.get_member(target_user)
        user = guild_obj.get_member(user)
        if not target.voice.channel:
            await target.send("You are not connected to a voice channel!")
            return

        try:
            await user.move_to(target.voice.channel)
        except:
            await user.send("It seems like you are not in the waiting room voice channel!")
            await target.send("Next person in queue was not in waiting room.")
            return None

    async def next_queue(self,queue):
        next_person = next(queue)
        if next_person:
            await self.connect_user(queue)

    async def reaction_queue_message(self,ctx):
        emoji_equals = lambda em: str(ctx.emoji) == emoji.emojize(em,use_aliases=True)

        message = await self.client.get_channel(ctx.channel_id).fetch_message(ctx.message_id)

        if emoji_equals(":stop_button:"):
            await self.queue_cleanup(ctx.message_id)
            await message.delete()

        elif emoji_equals(":arrow_forward:"):
            await self.next_queue(Queue.get_queue_by_message(ctx.message_id))

        elif emoji_equals(":record_button:"):
            queue = Queue.get_queue_by_message(ctx.message_id)
            if queue.current:
                await self.connect_user(queue)





    @commands.Cog.listener()
    async def on_raw_reaction_add(self,ctx):
        # We don't care about it if it's the bot
        if ctx.user_id == self.client.user.id:
            return
        if ctx.message_id in data.messages:
            switch = {
                "queue": self.reaction_queue_message
            }
            await switch[data.messages[ctx.message_id]](ctx)


    async def re_distribute_queues(self, guild_name):
        # We will first cut all current queues with more than 2 remaining elements to redistribute them
        for queue in data.queues[guild_name]:
            queue_cut = queue.cut_after_next()
            if queue_cut:
                data.waiting_queues[guild_name].add(*queue_cut)

        next_waiting = data.waiting_queues[guild_name].current
        available_queue_index = 0
        while next_waiting and len(data.queues[guild_name]) > 0:
            available_queue_index = (available_queue_index+1)%len(data.queues[guild_name])
            data.queues[guild_name][available_queue_index].add(next_waiting)
            next_waiting = next(data.waiting_queues[guild_name])
        for guild in data.waiting_queues:
            data.waiting_queues[guild].clear()


    @commands.command("ready", aliases=("handin","hand_in","hand-in"))
    @commands.guild_only()
    async def assignment_handin(self,ctx):
        guild_id = ctx.guild.id
        guild_name = None
        for guild in data.settings["Guilds"]:
            if guild_id == data.settings["Guilds"][guild]:
                guild_name = guild
                break
        if not guild_name:
            return
        if len(data.queues[guild_name]) == 0:
            data.waiting_queues[guild_name].add(ctx.author.id)
        else:
            sorted(data.queues[guild_name], key=lambda k: k.length)[0].add(ctx.author.id)

    @commands.command("start_queue",aliases=("sq","startqueue","start-queue"))
    async def start_queue(self,ctx, arg):
        if not await self.is_TA(ctx):
            return
        guild_name = arg.upper()
        if not guild_name in ("A","B"):
            await ctx.channel.send("<@{}> Invalid server!".format(ctx.author.id))
            return

        queue_owner = ctx.author.id

        stop_em, next_em, current_em = ":stop_button:",":arrow_forward:",":record_button:"
        get_emoji = lambda em: emoji.emojize(em, use_aliases = True)

        embed = discord.Embed(title="Hand-in Queue",
                              description="""
                              Hand-in queue created on server {} 
                              To terminate the queue, react with {}.
                              To call in the first member in the queue, react with {}.
                              To call in the next member in the queue, react with {}.
                              """.format(guild_name,get_emoji(stop_em),get_emoji(current_em),get_emoji(next_em)),
                              colour=0x41f109)
        message = await ctx.channel.send(embed=embed)
        message_id = message.id
        await message.add_reaction(get_emoji(stop_em))
        await message.add_reaction(get_emoji(current_em))
        await message.add_reaction(get_emoji(next_em))
        data.messages[message_id] = "queue"

        new_queue = Queue(queue_owner, message_id, guild_name)
        data.queues[guild_name].append(new_queue)

        await self.re_distribute_queues(guild_name)

    async def queue_cleanup(self, queue_message_id):
        queue_to_remove = Queue.get_queue_by_message(queue_message_id)
        guild_name = queue_to_remove.guild
        data.queues[guild_name].remove(queue_to_remove)
        queue_cut = queue_to_remove.cut_after_current()
        if queue_cut:
            data.waiting_queues[guild_name].add(*queue_cut)
        Queue.remove_queue_by_message(queue_message_id)
        await self.re_distribute_queues(guild_name)



    @commands.command("end_queue", aliases=("eq","endqueue","end-queue"))
    async def end_queue(self,ctx):
        if not await self.is_TA(ctx):
            return
        # End each queue that belongs to the author
        for guild_queue in data.queues:
            for queue in data.queues[guild_queue]:
                if queue.owner == ctx.author.id:
                    await self.queue_cleanup(queue.message_id)



def setup(client):
    client.add_cog(Assignment_Manager(client))
