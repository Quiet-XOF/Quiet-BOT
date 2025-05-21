import discord
from discord.ext import commands
import secrets
from channel_setup import channel_config


channel_config = channel_config()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Channels loaded: {channel_config.channels}")
    # TODO check main_channel is valid id
    await main_channel.send("I am online :butterfly:")

@bot.command(name="getchannel", help="Check a channel ID.")
async def getchannel(ctx, channel_name: str):
    try:
        if channel_config.get(channel_name):
            await ctx.send("Channel found.")
        else:
            await ctx.send("Channel not found.")
    except Exception as e:
        # TODO check if error_channel valid
        await ctx.send(f"Error: {e}")
        print(f"Error: {e}")

@bot.command(name="setchannel", help="Override a channel ID.")
async def setchannel(ctx, channel_name, channel_id):
    try:
        channel_config.set(channel_name, channel_id)
        await ctx.send(f"Done.")
    except Exception as e:
        # TODO check if error_channel valid
        await ctx.send(f"Error: {e}")
        print(f"Error: {e}")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("pong!")

@bot.command(name="shutdown")
async def shutdown(ctx):
    await ctx.send("Ok good night :pleading_face:")
    await bot.close()

async def main():
    await bot.start(secrets.token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())