import logging
import os
import yt_dlp
from discord.ext import commands
from ..utils.channel_config import channel_config
from ..utils.checks import check_channels


logger = logging.getLogger(__name__)

class YTDL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = self.check_path()
        
    def check_path(self):
        default_path = "YouTube-Downloads"
        custom_path = channel_config.getpath("video_download")
        if custom_path:
            path = os.path.join(custom_path, default_path)
        else:
            path = default_path
        logger.info(f"YTDL download path: {path}")
        return path

    @commands.command(name="ytdl")
    @check_channels("error")
    async def ytdl(self, ctx, url=None):
        if not url:
            await ctx.send("No url given, please provide a valid url.")
            return
        await ctx.send("Attempting to download video... :tv:")
        if not os.path.exists(self.path):
            await ctx.send("Creating \"YouTube Download\" folder.")
            os.makedirs(self.path)
        import asyncio
        loop = asyncio.get_event_loop()
        try:
            logger.info("Trying to download.")
            video_info = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL().extract_info(url, download=False)
            )
            video_title = yt_dlp.utils.sanitize_filename(video_info["title"])
            destination_file = os.path.join(self.path, f"{video_title}.mp4")
            # only checks name, add more qualifiers later
            if os.path.exists(destination_file):
                await ctx.send("Video already downloaded. Task aborted.")
                return
            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": f"{self.path}/%(title)s.%(ext)s",
                "merge_output_format": "mp4",
                "quiet": True,
                "noprogress": True
            }          
            await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL(ydl_opts).download(url)
            )
            logger.info(f"Video downloaded: {video_title}.mp4{video_title}")
            await ctx.send(f"Video downloaded: {video_title}.mp4")
        except Exception as e:
            logger.error(f"ytdl error: {e}")
            await ctx.bot_channels["error"].send(f"ytdl error: {e}")

async def setup(bot):
    await bot.add_cog(YTDL(bot))