import logging
import os


logger = logging.getLogger(__name__)

class ChannelConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChannelConfig, cls).__new__(cls)
            cls._instance._init_config()
        return cls._instance

    def _init_config(self):
#   def __init__(self):
        self.channels_file = os.path.join(os.path.dirname(__file__), "config.py")
        self.channels = self.load()

    def get(self, channel_name):
        return self.channels.get(channel_name)

    def set(self, channel_name, channel_id):
        logger.info(f"Setting {channel_name} to {channel_id}")
        self.channels[channel_name] = int(channel_id)
        self.save()

    def save(self):
        try:
            with open(self.channels_file, "w") as file:
                file.write(f"channels = {repr(self.channels)}\n")
            return f"Channels saved."
        except Exception as e:
            # TODO return false, handle error in main
            return f"Error saving channels: {e}"

    def load(self):
        logger.info("Loading channels...")
        if not os.path.exists(self.channels_file):
            logger.error("Error: File missing. Creating new file.")
            self.channels = {"download": None, "error": None, "main": None}
            self.save()
            return self.channels
        try:
            data = {}
            with open(self.channels_file, "r") as file:
                exec(file.read(), data)
            channels = data.get("channels", {})
            self.channels = channels
            return self.channels
        except Exception as e:
            logger.error(f"load error: {e}")
            self.channels = {}
            return {}