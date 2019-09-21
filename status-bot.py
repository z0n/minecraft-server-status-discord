#!/usr/bin/env python

import asyncio
import discord
import os
from dotenv import load_dotenv
from mcstatus import MinecraftServer
from socket import gaierror, timeout

load_dotenv()
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL"))
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MINECRAFT_SERVERS = [server.strip() for server in os.getenv("MINECRAFT_SERVERS").split(',')]

client = discord.Client(activity=discord.Game(name="Minecraft"))
status_message = {}

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, id=DISCORD_SERVER_ID)
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    print(
        f"{client.user} is connected to the following server:\n"
        f"{guild.name}(id: {guild.id})\n"
        f"Posting messages to channel {channel.name}"
    )

    # Delete all messages of the bot from the channel:
    async for message in channel.history():
        if message.author == client.user:
            await message.delete()

    # Main loop for updating the status:
    while not client.is_closed():
        for server_address in MINECRAFT_SERVERS:
            server = MinecraftServer.lookup(server_address)
            # favicon = None
            try:
                server.status(retries=1)
                skip_check = False
                server.query(retries=1)
                use_query = True
            except timeout:
                use_query = False
            except (ConnectionRefusedError, gaierror):
                skip_check = True

            if skip_check:
                num_players = 0
                max_players = 0
                player_names = ""
                # motd = "N/A"
                version = "N/A"
                ping = "N/A"
                online_color = discord.Colour.red()
                online_status = "Offline ⭕"
            else:
                server_status = server.status()
                if use_query:
                    server_query = server.query()
                    # :TODO: Convert to image and set as thumbnail.
                    # favicon = server_status.favicon
                    num_players = server_query.players.online
                    max_players = server_query.players.max
                    player_names = str(server_query.players.names).join("\n")
                    # :TODO: Handle all crazy types of MOTD.
                    # motd = server_query.motd
                    version = server_query.software.version
                else:
                    num_players = server_status.players.online
                    max_players = server_status.players.max
                    player_names = ""
                    # :TODO: Handle all crazy types of MOTD.
                    # motd = server_status.description["text"]
                    version = server_status.version.name
                try:
                    ping = f"{int(server.ping())} ms"
                except IOError:
                    ping = "N/A"
                online_color = discord.Colour.green()
                online_status = "Online ✅"

            embed = discord.Embed()
            embed.colour = online_color
            embed.description = f"**Status:** {online_status}\n\n**Version:** {version}\n**Ping:** {ping}\n**Players connected:** {num_players}/{max_players}\n\n{player_names}"
            embed.set_author(name=server_address)
            try:
                await status_message[server_address].edit(embed=embed)
            except KeyError:
                status_message[server_address] = await channel.send(embed=embed)
        await asyncio.sleep(CHECK_INTERVAL)

client.run(DISCORD_TOKEN)