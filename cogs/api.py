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
import urllib.parse

import discord
from discord import app_commands
from discord.ext import commands


class API(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command()
    @app_commands.describe(application="the application to search for")
    async def universaldb(self, interaction: discord.Interaction, application: str):
        """Searches for applications on Universal-DB"""
        async with self.bot.session.get(f"https://udb-api.lightsage.dev/get/{urllib.parse.quote(application)}") as resp:
            if resp.status != 200:
                await interaction.response.send_message("Unable to connect to UDB-API. Try again later?")
                return

            entry = await resp.json()

        embed = discord.Embed(title=entry['title'], description=entry['description'] or "No description found...",
                              color=discord.Color.blurple())

        if "website" in entry:
            embed.url = entry['website']

        if "avatar" in entry:
            embed.set_author(name=entry['author'], icon_url=entry['avatar'])
        else:
            embed.set_author(name=entry['author'])

        # Downloads formatting
        if "downloads" in entry:
            joined = "\n".join([f"[{key}]({value['url']})" for key, value in entry['downloads'].items()])

            if len(joined) > 1024:
                embed.description += f"\n\n**Latest Downloads**\n{joined}"
            else:
                embed.add_field(name="Latest Downloads", value=joined)

        # We probably don't have a qr if there's no downloads...
        if "qr" in entry:
            embed.set_thumbnail(url=list(entry['qr'].values())[0])

        await interaction.response.send_message(embed=embed)

    @universaldb.autocomplete('application')
    async def udb_autocomplete(self, _: discord.Interaction, string: str):
        resp = await self.bot.session.get(f"https://udb-api.lightsage.dev/search/{urllib.parse.quote(string)}")
        if resp.status != 200:
            return None

        resp = await resp.json()

        if not resp['results']:
            return None

        return [app_commands.Choice(name=app['title'], value=app['title']) for app in resp['results'][:25]]


async def setup(bot: commands.Bot):
    await bot.add_cog(API(bot))