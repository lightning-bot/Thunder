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
import discord
from discord import app_commands
from discord.ext import commands
from rapidfuzz import process


class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(emoji="The emoji to find")
    async def nitro(self, interaction: discord.Interaction, emoji: str):
        """You know what this is"""
        em = self.bot.get_emoji(int(emoji))
        if not em:
            await interaction.response.send_message("Couldn't find that emoji!")
            return

        await interaction.response.send_message(str(em))

    @nitro.autocomplete('emoji')
    async def nitro_autocomplete(self, _: discord.Interaction, string: str):
        emojis = [e.name for e in self.bot.emojis]
        choices = []
        for result, _, idx in process.extract_iter(string, emojis, score_cutoff=70):
            choices.append(app_commands.Choice(name=result, value=str(self.bot.emojis[idx].id)))
        return choices[:25]


async def setup(bot):
    await bot.add_cog(Emoji(bot))
