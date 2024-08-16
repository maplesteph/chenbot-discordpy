import discord
from importlib import import_module

from messageevent import MessageEvent

class ModularDiscordBot(discord.Client):
  def __init__(self, config, debug):
    super().__init__(intents = discord.Intents.all())
    self.config = config
    self.debug = debug
    self.owner = int(config.get('discord', 'owner_id'))
    
    self.guild_list = dict()
    try:
      for key in self.config['guilds']:
        guild_id = self.config['guilds'][key]
        guild_class = getattr(import_module(f'guilds.{self.config["guilds"][key]}.guild_main'), 'Guild') 
        self.guild_list[self.config['guilds'][key]] = guild_class(alias=key, id=guild_id)
    except ModuleNotFoundError as e:
      print("An error occurred while importing guilds!")
      print(e)
      print(f"Module Not Found: {key}")
      quit()
    
    #self.guild_cooldowns = []
    #self.guild_rate_limit = int(config.get('discord', 'guild_rate_limit'))

  # Setup and Logging
  async def on_ready(self):
    if (self.debug):
      print("Now dreaming...")
    else:
      print("Up and working!")

  # Command/Event Mapping
  async def on_message(self, message):
    if message.author.bot:
      # ignore other bots (and self)
      return
        
    if (message.guild == None):
      if (message.author.id == self.owner):
        if (message.content == "die"):
            # global shutdown command
          await self.close()
      else:
        return
    
    #if not self.on_cooldown(message.guild.id):
    await self.handle(message, MessageEvent.on_message)

  async def on_raw_message_delete(self, message):
    await self.handle(message, MessageEvent.on_raw_message_delete)

  async def on_raw_message_edit(self, message):
    await self.handle(message, MessageEvent.on_raw_message_edit)

  async def on_raw_reaction_add(self, message):
    await self.handle(message, MessageEvent.on_raw_reaction_add)

  async def handle(self, message, message_event: MessageEvent):
    try:
      guild_id = str(message.guild.id)
    except AttributeError:
      guild_id = str(message.guild_id)

    await self.guild_list[guild_id].handle(message, message_event, self)