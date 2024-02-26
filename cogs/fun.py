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
from typing import TYPE_CHECKING, Literal

import discord
import slowo
import yarl
from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from main import Thunder


MAX_CHILL_TEMP = -50
MAX_WARM_TEMP = 100
BAIT = ["https://i.imgur.com/5VKDzO6.png",
        "https://i.imgur.com/28hcpAL.png",
        "https://i.imgur.com/bb2QhRT.png",
        "https://i.imgur.com/coTPufb.png",
        "https://i.imgur.com/AXnYOuW.png",
        "https://i.imgur.com/QcxVJGB.png",
        "https://i.imgur.com/yedHnzp.png",
        "https://i.imgur.com/j98dUfd.jpg",
        "https://i.imgur.com/UKiDbzb.png",
        "https://i.imgur.com/TJuk44x.jpg",
        "https://i.imgur.com/3jIgvE6.png",
        "https://i.imgur.com/sYxJqfg.png",
        "https://i.imgur.com/oz4rlRj.png",
        "https://garfield-is-a.lasagna.cat/i/5kx4.png",
        "https://i.imgur.com/QsL2mQM.png"]


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot: Thunder = bot
        self.temp_cache = {}  # user_id: temperature (in C)

    @app_commands.command()
    async def bam(self, interaction: discord.Interaction, target: discord.Member) -> None:
        """Bams a member"""
        random_bams = ["n̟̤͙̠̤̖ǫ̺̻ͅw̴͍͎̱̟ ̷̭̖̫͙̱̪b͏͈͇̬̠̥ͅ&̻̬.̶̜͍̬͇̬ ҉̜̪̘̞👍̡̫͙͚͕ͅͅ", "n͢ow̢ ͜b&͢. ̷👍̷",
                       "n҉̺o̧̖̱w̯̬̜̺̘̮̯ ͉͈͎̱̰͎͡b&̪̗̮̣̻͉.͍͖̪͕̤͔ ͢👍̵͙̯͍̫̬",
                       "ńo̶̡͜w͘͟͏ ҉̶b̧&̧.̡͝ ̕👍̡͟", "n҉o̢͘͞w̢͢ ̢͏̢b͠&̴̛.̵̶ ̢́👍̴",
                       "n̶̵̵̷̡̲̝̺o̵̶̷̴̜͚̥͓w̶̶̶̴͔̲͢͝ ḇ̶̷̶̵̡̨͜&̷̴̶̵̢̗̻͝.̷̵̴̶̮̫̰͆ 👍̵̶̵̶̡̡̹̹",
                       "n̸̶̵̵̷̴̷̵̷̒̊̽ò̷̷̷̶̶̶̶̴̝ͥ̄w̶̶̷̶̵̴̷̶̴̤̑ͨ b̷̵̶̵̶̷̵̴̶̧͌̓&̵̶̵̶̷̴̵̴̻̺̓̑.̵̴̷̵̶̶̶̷̷̹̓̉ 👍",
                       "no̥̊w ͜͠b̹̑&̛͕.̡̉ 👍̡̌",
                       "n̐̆ow͘ ̌̑b͛͗&͗̂̍̒.̄ ͊👍͂̿͘",
                       "ₙₒw b&. 👍", "n҉o҉w҉ b҉&. 👍"]
        await interaction.response.send_message(f"{target} is {random.choice(random_bams)}")

    def c_to_f(self, c) -> int:
        return math.floor(9.0 / 5.0 * c + 32)

    def crease_by(self):
        return random.randint(1, 20)

    @app_commands.command()
    async def warm(self, interaction: discord.Interaction, member: discord.Member) -> None:
        """Warms a user"""
        temp = self.temp_cache.get(member.id, 0)
        if temp == MAX_WARM_TEMP:
            await interaction.response.send_message(f"{member} is too hot...")
            return

        temp += self.crease_by()
        temp = min(temp, MAX_WARM_TEMP)
        self.temp_cache[member.id] = temp

        await interaction.response.send_message(f"{member} warmed. Member is now {temp}°C ({self.c_to_f(temp)}°F).")

    @app_commands.command()
    async def chill(self, interaction: discord.Interaction, member: discord.Member) -> None:
        """Chills a user"""
        temp = self.temp_cache.get(member.id, 0)
        if temp == MAX_CHILL_TEMP:
            await interaction.response.send_message(f"{member} is too cold...")
            return

        temp -= self.crease_by()
        temp = max(MAX_CHILL_TEMP, temp)
        self.temp_cache[member.id] = temp

        await interaction.response.send_message(f"{member} chilled. Member is now {temp}°C ({self.c_to_f(temp)}°F).")

    @app_commands.command()
    @app_commands.describe(member="The member to check the temperature of")
    async def temperature(self, interaction: discord.Interaction, member: discord.Member):
        """Gets the temperature of a member"""
        temp = self.temp_cache.get(member.id)
        if not temp:
            await interaction.response.send_message(f"{member} does not have a temperature...")
            return

        await interaction.response.send_message(f"{member} has a temperature of {temp}°C ({self.c_to_f(temp)}°F) \N{THERMOMETER}")

    @app_commands.command()
    async def discordcopypaste(self, interaction: discord.Interaction, member: discord.Member):
        """Generates a discord copy paste message"""
        msg = f"Look out for a Discord user by the name of \"{member.name}\" with the tag #{member.discriminator}. "\
              "He is going around sending friend requests to random Discord users,"\
              " and those who accept his friend requests will have their accounts "\
              "DDoSed and their groups exposed with the members inside it "\
              "becoming a victim aswell. Spread the word and send this to as many discord servers as you can. "\
              "If you see this user, DO NOT accept his friend "\
              "request and immediately block him. Our team is "\
              "currently working very hard to remove this user from our database, please stay safe."
        await interaction.response.send_message(msg)

    @app_commands.command()
    @app_commands.describe(member="The member to eject", color="The color of the crewmate",
                           impostor="Whether the member is an impostor or not")
    async def eject(self, interaction: discord.Interaction, member: discord.Member, 
                    color: Literal['black', 'blue', 'brown', 'cyan', 'darkgreen', 'lime', 'orange', 'pink', 'purple', \
                         'red', 'white', 'yellow'], impostor: bool = False):
        """amogus"""
        await interaction.response.defer()

        url = yarl.URL.build(scheme="https", host="vacefron.nl", path="/api/ejected",
                             query={'name': member.display_name, 'crewmate': color, 'impostor': str(impostor)})
        req = await self.bot.session.get(url)

        if req.status != 200:
            await interaction.followup.send("Sorry, /eject is not working. Try again later(?)")
            return

        _bytes = await req.read()
        tmp = io.BytesIO(_bytes)
        tmp.seek(0)

        await interaction.followup.send(file=discord.File(tmp, "eject.png"))

    async def make_json_request(self, interaction: discord.Interaction, url):
        req = await self.bot.session.get(url)

        if req.status != 200:
            await interaction.followup.send("Sorry, this command is not working. Try again later(?)")
            return

        return await req.json()

    @app_commands.command()
    async def xkcd(self, interaction: discord.Interaction, value: int = None):
        """Displays an xkcd"""
        await interaction.response.defer()

        xkcd_latest = await self.make_json_request(interaction, "https://xkcd.com/info.0.json")

        xkcd_max = xkcd_latest.get("num")

        if value is not None and value > 0 and value < xkcd_max:
            entry = value
        else:
            entry = xkcd_max

        xkcd = await self.make_json_request(interaction, f"https://xkcd.com/{entry}/info.0.json")

        timestamp = datetime.strptime(f"{xkcd['year']}-{xkcd['month']}-{xkcd['day']}",
                                      "%Y-%m-%d")
        embed = discord.Embed(title=f"xkcd {xkcd['num']}: {xkcd['safe_title']}",
                              url=f"https://xkcd.com/{xkcd['num']}",
                              timestamp=timestamp, color=discord.Color(0x96A8C8))
        embed.set_image(url=xkcd["img"])
        embed.set_footer(text=xkcd["alt"])
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def slap(self, interaction: discord.Interaction, member: discord.Member):
        """Slaps someone"""
        await interaction.response.defer()

        resp = await self.make_json_request(interaction, "https://nekos.life/api/v2/img/slap")
        embed = discord.Embed(title=f"{interaction.user.display_name} slapped {member.display_name}")
        embed.set_image(url=resp['url'])
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def hug(self, interaction: discord.Interaction, member: discord.Member):
        """Hugs someone"""
        await interaction.response.defer()

        resp = await self.make_json_request(interaction, "https://nekos.life/api/v2/img/hug")
        embed = discord.Embed(title=f"{interaction.user.display_name} hugs {member.display_name}")
        embed.set_image(url=resp['url'])
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def pat(self, interaction: discord.Interaction, member: discord.Member):
        """Pats someone"""
        await interaction.response.defer()
        resp = await self.make_json_request(interaction, "https://nekos.life/api/v2/img/pat")
        embed = discord.Embed(title=f"{interaction.user.display_name} pats {member.display_name}")
        embed.set_image(url=resp['url'])
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def lolice(self, interaction: discord.Interaction, user: discord.User) -> None:
        """Lolice chief"""
        await interaction.response.defer()
        data = await self.make_json_request(interaction, f'https://nekobot.xyz/api/imagegen?type=lolice&url={user.avatar.with_format("png")}')
        embed = discord.Embed()
        embed.set_image(url=data['message'])
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def awooify(self, interaction: discord.Interaction, user: discord.User) -> None:
        """Awooify a user"""
        await interaction.response.defer()
        data = await self.make_json_request(interaction, f'https://nekobot.xyz/api/imagegen?type=awooify&url={user.avatar.with_format("png")}')
        embed = discord.Embed()
        embed.set_image(url=data['message'])
        await interaction.followup.send(embed=embed)

    @app_commands.command()
    async def bait(self, interaction: discord.Interaction):
        """Sends a random bait image"""
        await interaction.response.send_message(random.choice(BAIT))

    @app_commands.command()
    @app_commands.describe(text="The test to owoify")
    async def owoify(self, interaction: discord.Interaction, text: str) -> None:
        """Turns a message into owo-speak"""
        await interaction.response.send_message(slowo.UwU.ify(text))

    @app_commands.command()
    @app_commands.describe(text="The type of server")
    async def roleplay(self, interaction: discord.Interaction, text: str = "furry"):
        """Generates a personalized end-of-year server message"""
        tmp = "Hey guys, just wanted to wish you all happy holidays. "\
              "Discord is filled with ready-made messages that you don't even read, "\
              "you just copy and paste to every server, I don't like that, I like "\
              "writing from my heart. Our friendship, from the deepest to virtual, "\
              "is very important to me and couldn't ever be represented by a "\
              "cookie-cutter message from anywhere. So, I'd like to thank you all, "\
              f"you're the best {text} roleplaying server I've ever interacted with."
        await interaction.response.send_message(tmp)


@app_commands.context_menu(name='Owoify')
async def owoify(interaction: discord.Interaction, message: discord.Message) -> None:
    if not message.content:
        await interaction.response.send_message("This message has no content I can get...", ephemeral=True)
        return

    await interaction.response.send_message(slowo.UwU.ify(message.content))


@app_commands.context_menu(name="Mock")
async def mock(interaction: discord.Interaction, message: discord.Message):
    if not message.content:
        await interaction.response.send_message("This message has no content I can get...", ephemeral=True)
        return

    m = [random.choice([char.upper(), char.lower()]) for char in message.content]
    await interaction.response.send_message(discord.utils.escape_mentions("".join(m)))


async def setup(bot):
    await bot.add_cog(Fun(bot))
    bot.tree.add_command(mock)
    bot.tree.add_command(owoify)
