import asyncio
import config
import discord
from discord.ext import commands
import secrets


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await main_channel.send("I am online :butterfly:")

@bot.command(name="channel")
async def channel(ctx, channel_name: str, channel_id: int = None):
    try:
        # get function
        if channel_id is None:
            if channel_name in config.channels:
                existing_id = config.channels[channel_name]
                check_channel = bot.get_channel(existing_id)
                if check_channel:
                    await ctx.send(f"The channel \"{channel_name}\" is \"{check_channel}\". ({existing_id})")
                else:
                    await ctx.send(f"The channel \"{channel_name}\" isn't in the server! ({existing_id})")
            else:
                await ctx.send(
                    f"I don't know what \"{channel_name}\" is.\n"
                    f"Channels: {", ".join(config.channels.keys())}"
                )
            return
        # set function
        check_channel = bot.get_channel(channel_id)
        if check_channel:
            config.channels[channel_name] = channel_id

            # TODO: implement json file to hold this info
            config.save()
            await ctx.send(f"The channel \"{channel_name}\" is set to {check_channel.mention}.")
        else:
            await ctx.send("That ID doesn't exist, or I cannot see it.")
        return        

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

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
    asyncio.run(main())