"""
Thunder
Copyright (C) 2022 LightSage

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import logging

import aiohttp
import discord
from discord.ext.commands import Bot

import config

logging.basicConfig(level="INFO")

cogs = ['jishaku',
        'cogs.fun',
        'cogs.stats',
        'cogs.imagegen',
        'cogs.api',
        'cogs.emoji']

class Thunder(Bot):
    def __init__(self):
        super().__init__(command_prefix=['t!'], allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
                         intents=discord.Intents(messages=True, members=True, guilds=True))
        self.ready_fired = False

    async def setup_hook(self):
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()

        for cog in cogs:
            await self.load_extension(cog)

    async def on_ready(self):
        if self.ready_fired:
            return

        self.ready_fired = True
        await self.tree.sync()


if __name__ == '__main__':
    bot = Thunder()
    bot.run(config.TOKEN)