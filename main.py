import asyncio
import config
import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await channel.send("I am online :butterfly:")

@bot.command(name="shutdown")
async def shutdown(ctx):
    await ctx.send("Ok good night :pleading_face:")
    await bot.close()

async def main():
    await bot.start(config.token)

if __name__ == "__main__":
    asyncio.run(main())