import discord
import configparser
from importlib import import_module

from messageevent import MessageEvent
from guilds.guildinterface import GuildInterface

class Guild(GuildInterface):
  # Handlers
  async def handle(self, message, message_event, client):
    match (message_event):
      # Event Unmapping
      case MessageEvent.on_message:
        await self.on_message(message, message_event, client)
      case MessageEvent.on_raw_message_delete:
        await self.on_raw_message_delete(message, message_event, client)
      case MessageEvent.on_raw_message_edit:
        await self.on_raw_message_edit(message, message_event, client)
      case MessageEvent.on_raw_reaction_add:
        await self.on_raw_reaction_add(message, message_event, client)

  async def on_message(self, message, message_event, client):
    return

  async def on_raw_message_delete(self, message, message_event, client):
    return
  
  async def on_raw_message_edit(self, message, message_event, client):
    return

  async def on_raw_reaction_add(self, message, message_event, client):
    return