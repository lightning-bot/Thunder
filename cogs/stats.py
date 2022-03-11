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

import config


class Stats(commands.Cog):

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        embed = discord.Embed(title="Guild Join", color=discord.Color.blue())
        owner = await self.bot.fetch_user(guild.owner_id) or "Unknown User"
        embed.description = f"**Name**: {guild.name}\n**ID**: {guild.id}\n**Owner**: {str(owner)} ({guild.owner_id})"

        if hasattr(guild, 'members'):
            bots = sum(member.bot for member in guild.members)
            humans = guild.member_count - bots
            embed.add_field(name='Member Count', value=f"Bots: {bots}\nHumans: {humans}\nTotal: {len(guild.members)}")

        channel = self.bot.get_channel(config.GUILD_STATUS_CHANNEL)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        embed = discord.Embed(title="Guild Leave", color=discord.Color.red())
        owner = await self.bot.fetch_user(guild.owner_id) or "Unknown User"
        embed.description = f"**Name**: {guild.name}\n**ID**: {guild.id}\n**Owner**: {str(owner)} ({guild.owner_id})"

        if hasattr(guild, 'members'):
            bots = sum(member.bot for member in guild.members)
            humans = guild.member_count - bots
            embed.add_field(name='Member Count', value=f"Bots: {bots}\nHumans: {humans}\nTotal: {len(guild.members)}")

        channel = self.bot.get_channel(config.GUILD_STATUS_CHANNEL)
        await channel.send(embed=embed)

    @app_commands.command()
    async def about(self, interaction: discord.Interaction):
        """Tells you information about this bot"""
        await interaction.response.send_message("Thunder, a companion bot to Lightning. This bot is open source and can be found at "
                                                "<https://gitlab.com/lightning-bot/thunder>")

def setup(bot):
    bot.add_cog(Stats(bot))