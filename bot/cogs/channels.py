from discord.ext import commands
from ..utils.config import ChannelConfig


channel_config = ChannelConfig()

class Channels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_channels(*required_channels):
        async def predicate(ctx):
            #bot_channels = getattr(ctx, "bot_channels", {})
            #ctx.destination = bot_channels.get(channel_name) or ctx.channel 
            ctx.bot_channels = {}
            for name in required_channels:
                channel_id = channel_config.get(name)
                channel = ctx.guild.get_channel(channel_id) if channel_id else None
                ctx.bot_channels[name] = channel or ctx.channel
            return True
        return commands.check(predicate)

    @commands.command(name="getchannel", help="Check a channel ID.")
    @check_channels("error")
    async def getchannel(self, ctx, channel_name=None):
        print("Getting channels...")
        try:
            if channel_name is None:
                print("Getting all channels...")
                response = "\n".join(f"{cn}: {ci}" for cn, ci in channel_config.channels.items())
                await ctx.send(response if response else "No channels configured.")
            else:
                print("Getting one channel...")
                channel_id = channel_config.get(channel_name)
                if channel_id:
                    await ctx.send(f"{channel_name}: {channel_id}")
                else:
                    await ctx.bot_channels["error"].send(f"{channel_name} is not configured.")
        except Exception as e:
            print(f"getchannel error: {e}")
            await ctx.bot_channels["error"].send(f"setchannel error: {e}")

    @commands.command(name="setchannel", help="Override a channel ID.")
    @check_channels("error")
    async def setchannel(self, ctx, channel_name, channel_id):
        # TODO add channels such as logs, admin information, etc
        try:
            # TODO check if ID in THIS server
            channel_config.set(channel_name, channel_id)
            await ctx.send(f"{channel_name} has been set to {channel_id}")
        except Exception as e:
            print(f"setchannel error: {e}")
            await ctx.bot_channels["error"].send(f"setchannel error: {e}")

async def setup(bot):
    await bot.add_cog(Channels(bot))