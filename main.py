import asyncio
import discord
import json
import logging
from discord.ext import commands


class QuietBot(commands.Bot):
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        self.logger = logging.getLogger(__name__)

        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        super().__init__(
            case_insensitive = True,
            command_prefix = "!",
            description = "self destruct bot",
            help_command = commands.DefaultHelpCommand(no_category = "Commands"),
            intents = intents,
            self_bot = False            
        )

        self.secrets = self.load_secrets()
        self.main_channel = None
        self.download_channel = None
        self.error_channel = None

    def load_secrets(self):
        try:
            with open("secrets.json") as file:
                secrets = json.load(file)
                if not secrets.get("token"):
                    raise ValueError("Token missing. Program ending...")
                return secrets
        except FileNotFoundError:
            default = {
                "token": None, 
                "main_channel": None,
                "download_channel": None,
                "error_channel": None
            }
            with open("secrets.json", "w") as file:
                json.dump(default, file, indent=4)
            self.logger.error("The file was missing, so it was created. Please insert your token and try again.")
            sys.exit()

    async def setup_hook(self):
        await self.load_extension("cogs.core")
        await self.load_extension("cogs.scrape")
        await self.load_extension("cogs.quiz")

    async def on_ready(self):
        self.main_channel = self.get_channel(self.secrets["main_channel"])
        self.download_channel = self.get_channel(self.secrets["download_channel"])
        self.error_channel = self.get_channel(self.secrets["error_channel"])

        self.logger.info(f"Logged in as {self.user.name}: {self.user.id}")
        await self.main_channel.send("I'm online :butterfly:")
        await self.change_presence(activity=discord.Game(name="weh"))

if __name__ == "__main__":
    bot = QuietBot()
    bot.run(bot.secrets["token"])
    #bot = QuietBot()
    #token = bot.load_secrets()
    #try:
    #    await bot.start(token)
    #except KeyboardInterrupt:
    #    await bot.close()  
    #asyncio.run(main())