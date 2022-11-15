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

from .models import VoteBanBallots, VoteBanCandidates, VoteBanConfig

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

        try:
            await self.view.add_vote(interaction.user.id)
        except discord.HTTPException as e:
            await interaction.response.edit_message(content=f"Failed to ban {self.member} for {e}! Closing...")
            self.view.stop()

        await interaction.response.edit_message(content=f"{fmt} ({self.view.vote_count} voters)")


class VoteBanView(discord.ui.View):
    def __init__(self, member: discord.Member, model: VoteBanCandidates, max_votes: int = 5):
        super().__init__(timeout=None)
        self.member = member  # member to ban
        self.voters = []
        self.model = model
        self.max_votes = max_votes
        self.add_item(VoteButton(self, emoji="<:voted:649356870376488991>"))

        self.view_voters_button.custom_id = f"thunder-vote-ban-voters-{member.guild.id}-{member.id}"

    @classmethod
    async def from_database(cls, record: VoteBanCandidates):
        cls = cls(record.member, record)
        cls.voters = [v.voter_id for v in await record.voters.all()]
        return cls

    @property
    def vote_count(self):
        return len(self.voters)

    async def ban(self):
        self.model.active = False
        await self.model.save(update_fields=['active'])

        await self.member.ban(delete_message_days=0, reason="Votebanned")
        self.stop()

    async def add_vote(self, user_id: int):
        await VoteBanBallots.create(candidate_id=self.model.id, voter_id=user_id)
        self.voters.append(user_id)

        if self.vote_count >= self.max_votes:
            await self.ban()

    async def remove_vote(self, user_id: int):
        ballot = await VoteBanBallots.get_or_none(candidate_id=self.model.id,
                                                  voter_id=user_id)
        if ballot:
            self.voters.remove(ballot.voter_id)
            await ballot.delete()

    @discord.ui.button(label="View Votes", row=2, style=discord.ButtonStyle.blurple)
    async def view_voters_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.voters:
            content = "\n".join(f"<@!{id}>" for id in self.voters)
        else:
            content = "Nobody has voted yet!"

        await interaction.response.send_message(content=content,
                                                ephemeral=True)


class ConfirmView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, *, timeout=60):
        super().__init__(timeout=timeout)
        self.status = None
        self.member = interaction.user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.member.id == interaction.user.id

    @discord.ui.button(emoji="<:greenTick:613702930444451880>")
    async def yes_button(self, itx: discord.Interaction, button: discord.ui.Button):
        self.status = True
        await itx.response.edit_message()
        self.stop()

    @discord.ui.button(emoji="<:redTick:613703043283681290>")
    async def no_button(self, itx: discord.Interaction, button: discord.ui.Button):
        self.status = False
        await itx.response.edit_message()
        self.stop()


class VoteBan(GroupCog, name="voteban"):
    """The voteban commands"""
    def __init__(self, bot: Thunder) -> None:
        super().__init__()
        self.bot: Thunder = bot

    def cog_load(self) -> None:
        self.bot.loop.create_task(self.init_existing_views())

    async def init_existing_views(self):
        await self.bot.wait_until_ready()

        async for model in VoteBanCandidates.filter(active=True):
            guild = self.bot.get_guild(model.guild_id)
            if not guild:
                continue
            setattr(model, 'member', guild.get_member(model.user_id))
            self.bot.add_view(await VoteBanView.from_database(model), message_id=model.message_id)

    @app_commands.command(name="new")
    @app_commands.describe(member="The member to voteban", pin="Whether to pin the message to the channel's pins")
    async def new(self, interaction: discord.Interaction, member: discord.Member, pin: bool = False):
        """Starts a new vote to ban someone"""
        m = await VoteBanCandidates.get_or_none(guild_id=interaction.guild.id, user_id=member.id, active=True)
        if m:
            view = ConfirmView(interaction)
            await interaction.response.send_message("There is already a voteban going on! Do you want to start a new one?", view=view)
            await view.wait()

            if view.status is not True:
                return

            m.active = False
            await m.save()

        model = await VoteBanCandidates.create(guild_id=interaction.guild.id, user_id=member.id)
        config = await VoteBanConfig.get_or_create(guild_id=interaction.guild.id, vote_count=5)

        if interaction.response.is_done():
            await interaction.original_message()
            resp = interaction.edit_original_message
        else:
            resp = interaction.response.send_message

        await resp(content="Click the <:voted:649356870376488991> button to vote!", view=VoteBanView(member, model, config[0].vote_count))

        message = await interaction.original_message()
        model.message_id = message.id
        await model.save()

    @app_commands.command(name="max-votes")
    @app_commands.default_permissions(manage_guild=True)
    async def max_votes(self, interaction: discord.Interaction, votes: int = 5):
        """Allows you to configure how many votes are required for a vote ban"""
        await VoteBanConfig.update_or_create(guild_id=interaction.guild.id, vote_count=votes)
        await interaction.response.send_message("Updated the config!\n> Please note any ongoing vote bans are still using the old value!")


async def setup(bot: Thunder):
    await Tortoise.init(db_url=config.DB_URL, modules={'models': ['cogs.voteban.models']})
    await Tortoise.generate_schemas(safe=True)

    await bot.add_cog(VoteBan(bot))


async def teardown(bot: Thunder):
    await Tortoise.close_connections()
