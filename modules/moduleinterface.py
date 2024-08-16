import discord
import configparser
from importlib import import_module

from messageevent import MessageEvent

class ModuleInterface:
  # Constructor
  def __init__(self, name, config, guild_id):
    self.name = name
    self.config = dict(config)
    self.guild_id = guild_id # id of the connected guild
  
  # Class Meta Helpers
  def __eq__(self, other):
    return

  def __repr__(self):
    return
  
  # Handlers - to be implemented per module
  async def handle(self, message, message_event, client):
    """Handles all the mapping from inputted command to proper event type"""
    pass

  async def on_message(self, message, message_event, client):
    pass

  async def on_raw_message_delete(self, message, message_event, client):
    pass
  
  async def on_raw_message_edit(self, message, message_event, client):
    pass

  async def on_raw_reaction_add(self, message, message_event, client):
    pass