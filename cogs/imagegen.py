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
import io
import discord
import slash_util
from jishaku.functools import executor_function
from PIL import Image, ImageDraw, ImageFont
import textwrap

class ImageGen(slash_util.Cog):
    """
    Image generation that isn't using an API.
    
    All commands here have been ported from Lightning under the AGPLv3 license. (https://gitlab.com/lightning-bot/Lightning)
    """
    
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

    @slash_util.slash_command()
    async def lakitufyi(self, ctx: slash_util.Context, text: str) -> None:
        """Makes a Lakitu FYI meme with your own text"""
        await ctx.defer()
        image_buffer = await self.make_lakitu(text)
        await ctx.send(file=discord.File(image_buffer, filename="fyi.png"))

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

    @slash_util.slash_command()
    async def kurisudraw(self, ctx: slash_util.Context, text: str) -> None:
        """Kurisu can solve this, can you?"""
        await ctx.defer()
        img_buff = await self.make_kcdt(text)
        await ctx.send(file=discord.File(img_buff, filename="kurisudraw.png"))


def setup(bot):
    bot.add_cog(ImageGen(bot))