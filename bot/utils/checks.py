from discord.ext import commands


def check_channels(*required_channels):
    async def predicate(ctx):
        #bot_channels = getattr(ctx, "bot_channels", {})
        #ctx.destination = bot_channels.get(channel_name) or ctx.channel 
        ctx.bot_channels = {}
        from .config import ChannelConfig
        channel_config = ChannelConfig()
        for name in required_channels:
            channel_id = channel_config.get(name)
            channel = ctx.guild.get_channel(channel_id) if channel_id else None
            ctx.bot_channels[name] = channel or ctx.channel
        return True
    return commands.check(predicate)