import discord
import os
from discord.ext import commands


class QuietBot(commands.Bot):
    def __init__(self, command_prefix="!", intents=None):
        help_command = commands.DefaultHelpCommand(no_category = "Commands")
        if intents is None:
            intents = discord.Intents.default()
            intents.messages = True
            intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents, help_command = help_command)

    async def load_cogs(self):
        #for file in os.listdir("bot/cogs"):
        #    if file.endswith(".py"):
        #        cog_check = f"bot.cogs.{file[:-3]}"
        #        try:
        #            await self.load_extension(cog_check)
        #            print(f"Loaded cog: {cog_check}")
        #        except Exception as e:
        #            print(f"{cog_check} load failed: {e}")
        await self.load_extension("bot.cogs.channels")
        await self.load_extension("bot.cogs.core")
        await self.load_extension("bot.cogs.ytdl")
        # TODO create directory for os paths

    #@check_channels("main")
    async def on_ready(self):
        print(f"Logged in as {self.user.name}: {self.user.id}")
        #print(f"Channels loaded: {channel_config.channels}")
        #await ctx.destination.send("I am online :butterfly:")