import discord
from discord.ext import commands
import secrets
from channel_config import channel_config


channel_config = channel_config()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

help_command = commands.DefaultHelpCommand(
    no_category = "Commands"
)

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command = help_command
)

def check_channels(*required_channels):
    async def predicate(ctx):
        ctx.bot_channels = {}
        for channel_name in required_channels:
            channel_id = channel_config.get(channel_name)
            channel = ctx.guild.get_channel(channel_id)
            ctx.bot_channels[channel_name] = channel or ctx.channel
        return True
    return commands.check(predicate)

@bot.event
@check_channels("main")
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    #print(f"Channels loaded: {channel_config.channels}")
    await ctx.bot_channels["main"].send("I am online :butterfly:")

@bot.command(name="getchannel", help="Check a channel ID.")
@check_channels("error")
async def getchannel(ctx, channel_name=None):
    try:
        if channel_name is None:
            await ctx.send(f"{"\n".join(f"{cn}: {ci}" for cn, ci in channel_config.channels.items())}")
        else:
            channel_id = channel_config.get(channel_name)
            if channel_id:
                await ctx.send(f"{channel_name}: {channel_id}")
            else:
                await ctx.send(f"{channel_name} is not configured.")
    except Exception as e:
        await ctx.bot_channels["error"].send(f"Error: {e}")

@bot.command(name="setchannel", help="Override a channel ID.")
@check_channels("error")
async def setchannel(ctx, channel_name, channel_id):
    # TODO add channels such as logs, admin information, etc
    try:
        # TODO check if ID in THIS server
        channel_config.set(channel_name, channel_id)
        await ctx.send(f"Done.")
    except Exception as e:
        await ctx.bot_channels["error"].send(f"Error: {e}")

@bot.command(name="ping", help="Check latency.")
async def ping(ctx):
    latency = round(bot.latency * 1000, 2)
    await ctx.send(f"pong! {latency}ms")

@bot.command(name="shutdown", help="Shutdown the server remotely.")
async def shutdown(ctx):
    await ctx.send("Ok good night :pleading_face:")
    # TODO this doesn't seem to cut it
    await bot.close()

async def main():
    await bot.start(secrets.token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())