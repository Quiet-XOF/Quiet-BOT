import logging
from discord.ext import commands
from .channel_config import channel_config


logger = logging.getLogger(__name__)

def check_channels(*required_channels):
    async def predicate(ctx):
        #bot_channels = getattr(ctx, "bot_channels", {})
        #ctx.destination = bot_channels.get(channel_name) or ctx.channel 
        logger.info(f"Checking channels: {required_channels}")
        ctx.bot_channels = {}
        for name in required_channels:
            channel_id = channel_config.getchannel(name)
            channel = ctx.guild.get_channel(channel_id) if channel_id else None
            ctx.bot_channels[name] = channel or ctx.channel
        logger.info("Leaving checks...")
        return True
    return commands.check(predicate)