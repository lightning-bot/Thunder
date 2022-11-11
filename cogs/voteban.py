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
from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext.commands import GroupCog

if TYPE_CHECKING:
    from main import Thunder


# guild_id: {member_to_ban: {voters: []}} NO PK


class VoteButton(discord.ui.Button['VoteBanView']):
    def __init__(self, view: 'VoteBanView', *, emoji):
        super().__init__(emoji=emoji, custom_id=f"thunder-voteban-view-{view.member.guild.id}-{view.member.id}")
        self._view = view
        assert self.view is not None

        self.member = self.view.member

    async def callback(self, interaction: discord.Interaction) -> None:
        fmt = "Click the <:voted:649356870376488991> button to vote!"
        assert self.view is not None

        if interaction.user.id in self.view.voters:
            await self.view.remove_vote(interaction.user.id)
            await interaction.response.edit_message(content=f"{fmt} ({self.view.vote_count} voters)")
            await interaction.followup.send("Removed your vote!", ephemeral=True)
            return

        await self.view.add_vote(interaction.user)

        await interaction.response.edit_message(content=f"{fmt} ({self.view.vote_count} voters)")


class VoteBanView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member  # member to ban
        self.voters = []
        self.add_item(VoteButton(self, emoji="<:voted:649356870376488991>"))

    @classmethod
    def from_database(cls, record):
        cls = cls(record['member'])
        cls.voters = record['voters']
        return cls

    @property
    def vote_count(self):
        return len(self.voters)

    async def add_vote(self, user: discord.Member):
        self.voters.append(user.id)

    async def remove_vote(self, user_id: int):
        self.voters.remove(user_id)


class VoteBan(GroupCog, name="voteban"):
    """The voteban commands"""
    def __init__(self, bot: Thunder) -> None:
        super().__init__()
        self.bot: Thunder = bot

    async def cog_load(self) -> None:
        ...

    async def init_existing_views(self):
        # somewhere we fetch views
        objs = []
        for obj in objs:
            self.bot.add_view(VoteBanView.from_database(obj))

    @app_commands.command(name="new")
    @app_commands.describe(member="The member to voteban")
    async def new(self, interaction: discord.Interaction, member: discord.Member):
        """Starts a new vote to ban someone"""
        await interaction.response.send_message("Click the <:voted:649356870376488991> button to vote!", view=VoteBanView(member))

    @app_commands.command(name="max-votes")
    async def max_votes(self, interaction: discord.Interaction, votes: int):
        """Allows you to configure how many votes are required for a vote ban"""
        ...


async def setup(bot):
    await bot.add_cog(VoteBan(bot))
