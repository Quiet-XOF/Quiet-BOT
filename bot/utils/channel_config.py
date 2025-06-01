import os


class ChannelConfig:
    def __init__(self):
        self.channels_file = os.path.join(os.path.dirname(__file__), "channels.py")
        self.channels = self.load()

    def get(self, channel_name):
        return self.channels.get(channel_name)

    def set(self, channel_name, channel_id):
        print(f"Setting {channel_name} to {channel_id}")
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
        print("Loading channels...")
        if not os.path.exists(self.channels_file):
            print("Error: File missing. Creating new file.")
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
            print(f"load error: {e}")
            self.channels = {}
            return {}