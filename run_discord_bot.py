from conductor_discord.bot import client
import os

if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))
