import discord
import configparser
from importlib import import_module
import os
from messageevent import MessageEvent

class GuildInterface:
  # Constructor
  def __init__(self, alias, id):
    # metadata setup
    self.alias = alias
    self.id = id

    # configuration
    config_path = f'guilds/{self.id}/config.ini'
    self.config = configparser.ConfigParser()
    self.config.read(config_path)
    
    # module declaration
    modules = dict(self.config['config'])['modules'].split(',')
    self.modules = dict()
    try:
      for m in modules:
        if m == '':
          continue
        module_class = getattr(import_module(f'modules.{m}'), 'Module')
        self.modules[m] = module_class(m, dict(self.config[m]), self.id) #idk something like this
    except ModuleNotFoundError as e:
      print("An error occurred while import guild modules!")
      quit()

  # Class Meta Helpers
  def __eq__(self, other):
    return self.id == other.id

  def __repr__(self):
    return f'{self.id}:{self.alias}'

  # Handlers - to be implemented per guild
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