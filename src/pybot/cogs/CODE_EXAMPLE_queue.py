# Copyright 2020 San Kilkis

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

"""Contains the :py:class:`Queue` Cog definition."""

from discord.ext import commands

class Queue(commands.Cog):
    """Provides the functionality of queuing in voice channels."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = member.guild.system_channel
    #     if channel is not None:
    #         await channel.send("Welcome {0.mention}.".format(member))

    # @commands.command()
    # async def hello(self, ctx, *, member: discord.Member = None):
    #     """Says hello"""
    #     member = member or ctx.author
    #     if self._last_member is None or self._last_member.id != member.id:
    #         await ctx.send("Hello {0.name}~".format(member))
    #     else:
    #         await ctx.send(
    #             "Hello {0.name}... This feels familiar.".format(member)
    #         )
    #     self._last_member = member
