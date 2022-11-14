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
from tortoise import Tortoise

import config

from .models import VoteBanBallots, VoteBanCandidates

if TYPE_CHECKING:
    from main import Thunder


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

        await self.view.add_vote(interaction.user.id)

        await interaction.response.edit_message(content=f"{fmt} ({self.view.vote_count} voters)")


class VoteBanView(discord.ui.View):
    def __init__(self, member: discord.Member, cand_id: int):
        super().__init__(timeout=None)
        self.member = member  # member to ban
        self.voters = []
        self.cand_id = cand_id
        self.add_item(VoteButton(self, emoji="<:voted:649356870376488991>"))

    @classmethod
    async def from_database(cls, record: VoteBanCandidates):
        cls = cls(record.member, record.id)
        cls.voters = [v.voter_id for v in await record.voters.all()]
        return cls

    @property
    def vote_count(self):
        return len(self.voters)

    async def add_vote(self, user_id: int):
        await VoteBanBallots.create(ballot_id=self.cand_id, voter_id=user_id)
        self.voters.append(user_id)

    async def remove_vote(self, user_id: int):
        ballot = await VoteBanBallots.get_or_none(ballot_id=self.cand_id,
                                                  voter_id=user_id)
        if ballot:
            self.voters.remove(ballot.voter_id)
            await ballot.delete()


class VoteBan(GroupCog, name="voteban"):
    """The voteban commands"""
    def __init__(self, bot: Thunder) -> None:
        super().__init__()
        self.bot: Thunder = bot

    def cog_load(self) -> None:
        self.bot.loop.create_task(self.init_existing_views())

    async def init_existing_views(self):
        # somewhere we fetch views
        await self.bot.wait_until_ready()

        async for model in VoteBanCandidates.all():
            guild = self.bot.get_guild(model.guild_id)
            if not guild:
                continue
            setattr(model, 'member', guild.get_member(model.user_id))
            self.bot.add_view(await VoteBanView.from_database(model))

    @app_commands.command(name="new")
    @app_commands.describe(member="The member to voteban")
    async def new(self, interaction: discord.Interaction, member: discord.Member):
        """Starts a new vote to ban someone"""
        cand_id = await VoteBanCandidates.create(guild_id=interaction.guild.id, user_id=member.id)
        await interaction.response.send_message("Click the <:voted:649356870376488991> button to vote!", view=VoteBanView(member, cand_id.id))

    @app_commands.command(name="max-votes")
    async def max_votes(self, interaction: discord.Interaction, votes: int):
        """Allows you to configure how many votes are required for a vote ban"""
        ...


async def setup(bot: Thunder):
    await Tortoise.init(db_url=config.DB_URL, modules={'models': ['cogs.voteban.models']})
    await Tortoise.generate_schemas(safe=True)

    await bot.add_cog(VoteBan(bot))


async def teardown(bot: Thunder):
    await Tortoise.close_connections()
