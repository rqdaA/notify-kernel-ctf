import feedparser
import discord
import os
from dotenv import load_dotenv

load_dotenv()

COMMIT_FILE_PATH = "/workdir/kctf_commit.txt"
CHANNEL = int(os.getenv("CHANNEL", "0"))
TOKEN = os.getenv("TOKEN", "")
with open(COMMIT_FILE_PATH, "r") as f:
    LATEST_COMMIT_ID = f.read()


def send_msg(msg: discord.Embed):
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        await client.get_channel(CHANNEL).send(embed=msg)
        await client.close()

    client.run(TOKEN)


def is_new_commit(commit_id):
    return commit_id != LATEST_COMMIT_ID


def save_commit(commit_id):
    with open(COMMIT_FILE_PATH, "w") as f:
        f.write(commit_id)


def notify_new_commit(title, link):
    embed = discord.Embed(title=title, url=link)
    send_msg(embed)


def main():
    feed = feedparser.parse(
        "https://github.com/google/security-research/commits/master.atom"
    )

    for entry in feed.entries:
        commit_link = entry.link
        commit_title = entry.title
        commit_id = commit_link[commit_link.rfind("/") + 1 :]
        if not is_new_commit(commit_id):
            return

        if "kernelctf" in commit_title.lower():
            notify_new_commit(commit_title, commit_link)
            save_commit(commit_id)
            return


if __name__ == "__main__":
    main()
