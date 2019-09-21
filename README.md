# minecraft-server-status-discord
A Discord bot to display the server status of Minecraft servers in a channel. Tested on Python 3.7.4.

## How to use:
* Install Python >=3.6
* Install required Python packages, e.g using `pip install -r requirements.txt`
* Rename `.env.example` to `.env` and replace the example values
  * Multiple servers need to be separated by commas
* This bot should be used in a separate channel as it edits its own messages periodically
* Launch `status-bot.py`

## Example:
![Example Screenshot](https://user-images.githubusercontent.com/7430908/65376513-e1a3d780-dca0-11e9-8c5d-3d138c64a8d9.png)

## TODO:
* Improve error handling
* Handle program exit (delete messages, disconnect, etc.)
* Implement MOTD handling
* Add the server icon as a thumbnail (if available)