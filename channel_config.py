import os
from channels import channels


class channel_config:
    def __init__(self):
        self.channels = {}
        self.channels_file = "channels.py"
        self.load()

    def load(self):
        try:
            print("Loading channels...")
            if not os.path.exists(self.channels_file):
                print("Error: File missing. Creating new file.")
                self.channels = {}
                self.save()
                return
            else:
                self.channels = channels
        except (FileNotFoundError, IndexError, SyntaxError) as e:
            print(f"Error loading channels: {e}")

    def save(self):
        try:
            with open(self.channels_file, "w") as file:
                file.write(f"channels = {repr(self.channels)}\n")
            print("Channels saved.")
        except Exception as e:
            # TODO return false, handle error in main
            print(f"Error saving channels: {e}")

    def get(self, channel_name):
        #print(f"Getting channel {channel_name}")
        return self.channels.get(channel_name)

    def set(self, channel_name, channel_id):
        print(f"Setting {channel_name} to {channel_id}")
        # TODO catch bad entries
        self.channels[channel_name] = int(channel_id)
        self.save()