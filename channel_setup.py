import json


class channel_config:
    def __init__(self):
        self.channels = {}
        self.load()

    def load(self):
        try:
            print("Loading channels...")
            with open("config.json", "r") as file:
                self.channels = json.load(file)
        except FileNotFoundError:
            print("Missing config.json!")
        except json.JSONDecodeError as e:
            print(f"Error: {e}")

    def save(self):
        with open("config.json", "w") as file:
            json.dump(self.channels, file, indent=4)

    def get(self, channel_name):
        print("Getting channel...")
        return self.channels.get(channel_name)

    def set(self, channel_name, channel_id):
        print("Setting new channel id...")
        self.channels[channel_name] = channel_id
        self.save()