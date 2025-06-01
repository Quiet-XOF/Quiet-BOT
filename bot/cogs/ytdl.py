import os
import yt_dlp
from discord.ext import commands
from ..utils.paths import paths
from ..utils.checks import check_channels
from ..utils.channel_config import ChannelConfig


class YTDL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.path = self.check_path()
        
    def check_path(self):
        default_path = "YouTube-Downloads"
        custom_path = paths.get("video_download")
        if custom_path:
            path = os.path.join(custom_path, default_path)
        else:
            path = default_path
        print(f"YTDL download path: {path}")
        return path

    @commands.command(name="ytdl")
    @check_channels("error")
    async def ytdl(self, ctx, url):
        await ctx.send("Attempting to download video... :tv:")
        if not os.path.exists(self.path):
            await ctx.send("Creating \"YouTube Download\" folder.")
            os.makedirs(self.path)
        import asyncio
        loop = asyncio.get_event_loop()
        try:
            print("Trying to download.")
            video_info = await loop.run_in_executor(
                None,
                lambda: yt_dlp.YoutubeDL().extract_info(url, download=False)
            )
            video_title = yt_dlp.utils.sanitize_filename(video_info["title"])
            destination_file = os.path.join(self.path, f"{video_title}.mp4")
            print(f"{video_title}")
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
            await ctx.send(f"Video downloaded: {video_title}.mp4")
        except Exception as e:
            print(f"ytdl error: {e}")
            await ctx.bot_channels["error"].send(f"ytdl error: {e}")

async def setup(bot):
    await bot.add_cog(YTDL(bot))