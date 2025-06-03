import json
import logging
import os


logger = logging.getLogger(__name__)
default = {
    "channels": {"download": None, "error": None, "main": None},
    "paths": {"video_download": None, "image_download": None}
}

class ChannelConfig:
    """ Inbetween for channel commands and handling json files """
    # TODO this needs to be more flexible and have more validations
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChannelConfig, cls).__new__(cls)
            cls._instance._init_config()
        return cls._instance

    def _init_config(self):
#   def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.config = self.load()
        self.channels = self.config.get("channels", {})
        self.paths = self.config.get("paths", {})

    def getchannel(self, channel_name):
        return self.channels.get(channel_name)

    def setchannel(self, channel_name, channel_id):
        logger.info(f"Setting {channel_name} to {channel_id}")
        self.channels[channel_name] = int(channel_id)
        self.save()

    def getpath(self, path_name):
        return self.paths.get(path_name)
    
    def setpath(self, path_name, new_path):
        logger.info(f"Setting {path_name} to {new_path}")
        self.paths[path_name] = new_path
        self.save()

    def save(self):
        logger.info("Attempting to save channels and paths.")
        try:
            self.config["channels"] = self.channels
            self.config["paths"] = self.paths
            with open(self.config_file, "w") as file:
                json.dump(self.config, file, indent=2)
            return "Config saved."
        except Exception as e:
            logger.error(f"Error saving channels: {e}")
            return f"Error saving channels: {e}"

    def load(self):
        logger.info("Loading channels...")
        if not os.path.exists(self.config_file):
            logger.error("Error: File missing. Creating new file.")
            with open(self.config_file, "w") as file:
                json.dump(default, file, indent=4)
            return default
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"load error: {e}")
            return default

channel_config = ChannelConfig()