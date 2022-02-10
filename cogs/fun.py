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
import math
import random
from datetime import datetime
from typing import Literal

import discord
import slash_util
import yarl

MAX_CHILL_TEMP = -50
MAX_WARM_TEMP = 100

class Fun(slash_util.Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.temp_cache = {}  # user_id: temperature (in C)

    @slash_util.slash_command()
    async def bam(self, ctx: slash_util.Context, target: discord.Member) -> None:
        """Bams a member"""
        random_bams = ["n̟̤͙̠̤̖ǫ̺̻ͅw̴͍͎̱̟ ̷̭̖̫͙̱̪b͏͈͇̬̠̥ͅ&̻̬.̶̜͍̬͇̬ ҉̜̪̘̞👍̡̫͙͚͕ͅͅ", "n͢ow̢ ͜b&͢. ̷👍̷",
                       "n҉̺o̧̖̱w̯̬̜̺̘̮̯ ͉͈͎̱̰͎͡b&̪̗̮̣̻͉.͍͖̪͕̤͔ ͢👍̵͙̯͍̫̬",
                       "ńo̶̡͜w͘͟͏ ҉̶b̧&̧.̡͝ ̕👍̡͟", "n҉o̢͘͞w̢͢ ̢͏̢b͠&̴̛.̵̶ ̢́👍̴",
                       "n̶̵̵̷̡̲̝̺o̵̶̷̴̜͚̥͓w̶̶̶̴͔̲͢͝ ḇ̶̷̶̵̡̨͜&̷̴̶̵̢̗̻͝.̷̵̴̶̮̫̰͆ 👍̵̶̵̶̡̡̹̹",
                       "n̸̶̵̵̷̴̷̵̷̒̊̽ò̷̷̷̶̶̶̶̴̝ͥ̄w̶̶̷̶̵̴̷̶̴̤̑ͨ b̷̵̶̵̶̷̵̴̶̧͌̓&̵̶̵̶̷̴̵̴̻̺̓̑.̵̴̷̵̶̶̶̷̷̹̓̉ 👍",
                       "no̥̊w ͜͠b̹̑&̛͕.̡̉ 👍̡̌",
                       "n̐̆ow͘ ̌̑b͛͗&͗̂̍̒.̄ ͊👍͂̿͘",
                       "ₙₒw b&. 👍", "n҉o҉w҉ b҉&. 👍"]

        await ctx.send(f"{target} is {random.choice(random_bams)}")

    @slash_util.message_command(name="Mock")
    async def mock(self, ctx: slash_util.Context, message: discord.Message):
        if not message.content:
            await ctx.send("This message has no content I can get...", ephemeral=True)
            return

        m = [random.choice([char.upper(), char.lower()]) for char in message.content]
        await ctx.send(discord.utils.escape_mentions("".join(m)))

    def c_to_f(self, c) -> int:
        return math.floor(9.0 / 5.0 * c + 32)

    def crease_by(self):
        return random.randint(1, 20)

    @slash_util.slash_command()
    async def warm(self, ctx: slash_util.Context, member: discord.Member) -> None:
        """Warms a user"""
        temp = self.temp_cache.get(member.id, 0)
        if temp == MAX_WARM_TEMP:
            await ctx.send(f"{member} is too hot...")
            return

        temp += self.crease_by()
        temp = min(temp, MAX_WARM_TEMP)
        self.temp_cache[member.id] = temp

        await ctx.send(f"{member} warmed. Member is now {temp}°C ({self.c_to_f(temp)}°F).")

    @slash_util.slash_command()
    async def chill(self, ctx: slash_util.Context, member: discord.Member) -> None:
        """Chills a user"""
        temp = self.temp_cache.get(member.id, 0)
        if temp == MAX_CHILL_TEMP:
            await ctx.send(f"{member} is too cold...")
            return

        temp -= self.crease_by()
        temp = max(MAX_CHILL_TEMP, temp)
        self.temp_cache[member.id] = temp

        await ctx.send(f"{member} chilled. Member is now {temp}°C ({self.c_to_f(temp)}°F).")

    @slash_util.slash_command()
    @slash_util.describe(member="The member to check the temperature of")
    async def temperature(self, ctx: slash_util.Context, member: discord.Member):
        """Gets the temperature of a member"""
        temp = self.temp_cache.get(member.id)
        if not temp:
            await ctx.send(f"{member} does not have a temperature...")
            return

        await ctx.send(f"{member} has a temperature of {temp}°C ({self.c_to_f(temp)}°F) \N{THERMOMETER}")

    @slash_util.slash_command()
    async def discordcopypaste(self, ctx: slash_util.Context, member: discord.Member):
        """Generates a discord copy paste message"""
        msg = f"Look out for a Discord user by the name of \"{member.name}\" with the tag #{member.discriminator}. "\
              "He is going around sending friend requests to random Discord users,"\
              " and those who accept his friend requests will have their accounts "\
              "DDoSed and their groups exposed with the members inside it "\
              "becoming a victim aswell. Spread the word and send this to as many discord servers as you can. "\
              "If you see this user, DO NOT accept his friend "\
              "request and immediately block him. Our team is "\
              "currently working very hard to remove this user from our database, please stay safe."
        await ctx.send(msg)

    @slash_util.slash_command()
    @slash_util.describe(member="The member to eject", color="The color of the crewmate",
                         impostor="Whether the member is an impostor or not")
    async def eject(self, ctx: slash_util.Context, member: discord.Member, 
                    color: Literal['black', 'blue', 'brown', 'cyan', 'darkgreen', 'lime', 'orange', 'pink', 'purple', \
                         'red', 'white', 'yellow'], impostor: bool = False):
        """amogus"""
        url = yarl.URL.build(scheme="https", host="vacefron.nl", path="/api/ejected",
                             query={'name': member.display_name, 'crewmate': color, 'impostor': str(impostor)})
        req = await self.bot.session.get(url)

        if req.status != 200:
            await ctx.send("Sorry, /eject is not working. Try again later(?)")
            return

        _bytes = await req.read()
        tmp = io.BytesIO(_bytes)
        tmp.seek(0)

        await ctx.send(file=discord.File(tmp, "eject.png"))

    async def make_json_request(self, ctx, url):
        req = await self.bot.session.get(url)

        if req.status != 200:
            await ctx.send(f"Sorry, /{ctx.command.name} is not working. Try again later(?)")
            return
        
        return await req.json()

    @slash_util.slash_command()
    async def xkcd(self, ctx: slash_util.Context, value: int = None):
        """Displays an xkcd"""
        xkcd_latest = await self.make_json_request(ctx, "https://xkcd.com/info.0.json")

        xkcd_max = xkcd_latest.get("num")

        if value is not None and value > 0 and value < xkcd_max:
            entry = value
        else:
            entry = xkcd_max

        xkcd = await self.make_json_request(ctx, f"https://xkcd.com/{entry}/info.0.json")

        timestamp = datetime.strptime(f"{xkcd['year']}-{xkcd['month']}-{xkcd['day']}",
                                      "%Y-%m-%d")
        embed = discord.Embed(title=f"xkcd {xkcd['num']}: {xkcd['safe_title']}",
                              url=f"https://xkcd.com/{xkcd['num']}",
                              timestamp=timestamp, color=discord.Color(0x96A8C8))
        embed.set_image(url=xkcd["img"])
        embed.set_footer(text=xkcd["alt"])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
