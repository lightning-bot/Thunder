"""
Thunder
Copyright (C) 2022-2023 LightSage

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


class Memes(commands.GroupCog, group_name="memes"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def airdrop(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://i.imgur.com/a/RzxTBHj")

    @app_commands.command()
    async def stackz(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://i.imgur.com/kQUG6pq")

    @app_commands.command()
    async def jerry(self, interaction: discord.Interaction):
        await interaction.response.send_message("https://i.imgur.com/D141jYu.png")


async def setup(bot):
    await bot.add_cog(Memes(bot))
