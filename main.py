import discord
import json
import logging
import os
import sys
from discord.ext import commands


class QuietBot(commands.Bot):
    def __init__(self):
        self.secrets = self.load_secrets()

        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        self.logger = logging.getLogger(__name__)

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        super().__init__(command_prefix = "!",
                         intents = intents,
                         help_command = commands.DefaultHelpCommand(no_category = "Commands"),
                         case_insensitive = True)

    async def setup_hook(self):
        await self.load_cogs()

    async def load_cogs(self):
        self.logger.info("Loading cogs...")
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                cog_check = f"cogs.{file[:-3]}"
                try:
                    await self.load_extension(cog_check)
                    self.logger.info(f"Loaded cog: {cog_check}")
                except Exception as e:
                    self.logger.error(f"Failed to load {cog_check}: {e}")

    def load_secrets(self):
        try:
            with open("secrets.json") as file:
                secrets = json.load(file)
                if not secrets.get("token"):
                    raise ValueError("Token missing. Program ending...")
                return secrets
        except FileNotFoundError:
            default = {"token": None, "twit_user": None, "twit_pass": None}
            with open("secrets.json", "w") as file:
                json.dump(default, file, indent=4)
            sys.exit("The file was missing, so it was created. Please insert your token and try again.")

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user.name}: {self.user.id}")
        await self.change_presence(activity=discord.Game(name="weh"))

if __name__ == "__main__":
    bot = QuietBot()
    bot.run(bot.secrets["token"])