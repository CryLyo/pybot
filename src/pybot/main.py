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

"""Contains the main :py:class:`PyBot`."""

from typing import Optional

from discord.ext import commands


class PyBot(commands.Bot):
    """The main bot class onto which all :py:class:`Cog` are attached.

    A :py:class:`Cog` is a collection of commands and listeners that
    implements certain functionality required by the bot.
    """

    def __init__(
        self,
        command_prefix: str,
        help_command: str,
        description: Optional[str] = None,
    ):
        super().__init__(command_prefix, help_command, description)


if __name__ == "__main__":
    bot = PyBot()
