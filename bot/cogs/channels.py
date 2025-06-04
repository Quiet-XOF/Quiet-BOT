import logging
from discord.ext import commands
from ..utils.checks import check_channels
from ..utils.channel_config import channel_config


logger = logging.getLogger(__name__)

class Channels(commands.Cog):
    """ For viewing and changing channels """
    # TODO include path updates in this file
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="getchannel", help="Check a channel ID.")
    @check_channels("error")
    async def getchannel(self, ctx, channel_name=None):
        logger.info("Getting channels...")
        try:
            if channel_name is None:
                response = "\n".join(f"{cn}: {ci}" for cn, ci in channel_config.channels.items())
                await ctx.send(response if response else "No channels configured.")
            else:
                channel_id = channel_config.getchannel(channel_name)
                if channel_id:
                    await ctx.send(f"{channel_name}: {channel_id}")
                else:
                    await ctx.bot_channels["error"].send(f"{channel_name} is not configured.")
        except Exception as e:
            logger.error(f"getchannel error: {e}")
            await ctx.bot_channels["error"].send(f"getchannel error: {e}")

    @commands.command(name="setchannel", help="Override a channel ID.")
    @check_channels("error")
    async def setchannel(self, ctx, channel_name, channel_id):
        # TODO add channels such as logs, admin information, etc
        try:
            # TODO check if ID in THIS server
            channel_config.setchannel(channel_name, channel_id)
            await ctx.send(f"{channel_name} has been set to {channel_id}")
        except Exception as e:
            logger.error(f"setchannel error: {e}")
            await ctx.bot_channels["error"].send(f"setchannel error: {e}")

    @commands.command(name="getpath", help="Check paths")
    @check_channels("error")
    async def getpath(self, ctx, path_name=None):
        logger.info("Getting paths...")
        try:
            if path_name is None:
                response = "\n".join(f"{pn}: {pi}" for pn, pi in channel_config.paths.items())
                await ctx.send(response if response else "No paths configured.")
            else:
                path_id = channel_config.getpath(path_name)
                if path_id:
                    await ctx.send(f"{path_name}: {path_id}")
                else:
                    await ctx.bot_channels["error"].send(f"{path_name} is not configured.")
        except Exception as e:
            logger.error(f"getpath error: {e}")
            await ctx.bot_channels["error"].send(f"getpath error: {e}")

async def setup(bot):
    await bot.add_cog(Channels(bot))