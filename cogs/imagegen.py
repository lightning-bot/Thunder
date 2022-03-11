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

# The AGPLv3 License for Lightning is reproduced below.

Lightning.py - A Discord bot
Copyright (C) 2019-2022 LightSage

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation at version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

import io
import textwrap
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from jishaku.functools import executor_function
from PIL import Image, ImageDraw, ImageFont

if TYPE_CHECKING:
    from typing import Union

class ImageGen(commands.Cog):
    """
    Image generation that isn't using an API.
    
    All commands here have been ported from Lightning under the AGPLv3 license. (https://gitlab.com/lightning-bot/Lightning)
    """
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @executor_function
    def make_lakitu(self, text: str) -> io.BytesIO:
        img = Image.open("assets/templates/fyi.png")
        font = ImageFont.truetype(font="assets/fonts/Heebo-Regular.ttf",
                                  size=86, encoding="unic")
        draw = ImageDraw.Draw(img)
        text = textwrap.wrap(text, width=19)
        y_text = 200
        wdmax = 1150
        for line in text:
            if y_text >= 706:
                break
            line_width, line_height = draw.textsize(line, font=font)
            draw.multiline_text(((wdmax - line_width) / 2, y_text),
                                line, font=font,
                                fill="black")  # align="center")
            y_text += line_height
        finalbuffer = io.BytesIO()
        img.save(finalbuffer, 'png')
        finalbuffer.seek(0)
        return finalbuffer

    @app_commands.command()
    async def lakitufyi(self, interaction: discord.Interaction, text: str) -> None:
        """Makes a Lakitu FYI meme with your own text"""
        await interaction.response.defer()
        image_buffer = await self.make_lakitu(text)
        await interaction.followup.send(file=discord.File(image_buffer, filename="fyi.png"))

    @executor_function
    def make_kcdt(self, text: str) -> io.BytesIO:
        img = Image.open("assets/templates/kurisudraw.png")
        dafont = ImageFont.truetype(font="assets/fonts/Montserrat-Regular.ttf",
                                    size=42, encoding="unic")
        draw = ImageDraw.Draw(img)
        # Shoutouts to that person on stackoverflow that I don't remember
        y_text = 228
        wdmax = 560
        lines = textwrap.wrap(text, width=20)
        for line in lines:
            if y_text >= 390:
                break
            line_width, line_height = draw.textsize(line, font=dafont)
            draw.multiline_text(((wdmax - line_width) / 2, y_text),
                                line, font=dafont,
                                fill="black")  # align="center")
            y_text += line_height
        finalbuffer = io.BytesIO()
        img.save(finalbuffer, 'png')
        finalbuffer.seek(0)
        return finalbuffer

    @app_commands.command()
    async def kurisudraw(self, interaction: discord.Interaction, text: str) -> None:
        """Kurisu can solve this, can you?"""
        await interaction.response.defer()
        img_buff = await self.make_kcdt(text)
        await interaction.followup.send(file=discord.File(img_buff, filename="kurisudraw.png"))

    async def get_user_avatar(self, user: Union[discord.User, discord.Member]) -> bytes:
        async with self.bot.session.get(user.avatar.with_format("png").url) as resp:
            avy_bytes = await resp.read()
        return avy_bytes

    @executor_function
    def make_circle_related_meme(self, avatar_bytes: bytes, path: str, resize_amount: tuple,
                                 paste: tuple) -> io.BytesIO:
        base_image = Image.open(path)
        avatar = Image.open(io.BytesIO(avatar_bytes)).resize(resize_amount).convert("RGB")

        mask = Image.new("L", avatar.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(0, 0), avatar.size], fill=255)
        mask = mask.resize(resize_amount, Image.ANTIALIAS)

        base_image.paste(avatar, paste, mask=mask)

        buffer = io.BytesIO()
        base_image.save(buffer, "png")
        buffer.seek(0)

        return buffer

    @app_commands.command()
    @app_commands.describe(member="The member to use. If member is not provided, it uses the author.")
    # @commands.cooldown(2, 60.0, commands.BucketType.guild)
    async def screwedup(self, interaction: discord.Interaction, member: discord.Member = None) -> None:
        """Miko Iino tells you that you are screwed up in the head"""
        if member is None:
            member = interaction.user

        if member.id in [376012343777427457, self.bot.user.id]:
            return  # :mystery:

        await interaction.response.defer()
        avy = await self.get_user_avatar(member)
        image_buffer = await self.make_circle_related_meme(avy, "assets/templates/inthehead.png", (64, 64),
                                                           (14, 43))
        await interaction.followup.send(file=discord.File(image_buffer, "screwedupinthehead.png"))

    @app_commands.command()
    @app_commands.describe(member="The member to use. If member is not provided, it uses the author.")
    # @commands.cooldown(2, 60.0, commands.BucketType.guild)
    async def iq(self, interaction: discord.Interaction, member: discord.Member = None) -> None:
        """Your iq is 3"""
        if member is None:
            member = interaction.user

        if member.id in [376012343777427457, self.bot.user.id]:
            return  # :mystery:

        await interaction.response.defer()
        avy = await self.get_user_avatar(member)
        image_buffer = await self.make_circle_related_meme(avy, "assets/templates/fujiwara-iq.png", (165, 165),
                                                           (140, 26))
        await interaction.followup.send(file=discord.File(image_buffer, "huh_my_iq_is.png"))


def setup(bot):
    bot.add_cog(ImageGen(bot))