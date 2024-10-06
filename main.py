# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os

import discord

from keep_alive import keep_alive


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
        
        # try to record the message in a file
        try:
            with open("messages.txt", "a") as f:
                f.write(f"{message.author}: {message.content}\n")
        except Exception as e:
            print(f"Error writing to file: {e}")
            await message.channel.send("Error writing to file")
    
    # add a command to read the messages from the file
    if message.content.startswith('$read'):
        try:
            with open("messages.txt", "r") as f:
                messages = f.readlines()
                await message.channel.send("".join(messages))
        except Exception as e:
            print(f"Error reading from file: {e}")
            await message.channel.send("Error reading from file")


try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token to the Secrets pane.")
  keep_alive()
  client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e