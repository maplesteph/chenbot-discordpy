import discord
from discord import app_commands
import dataset

from messageevent import MessageEvent
from modules.moduleinterface import ModuleInterface

class Module(ModuleInterface):
  """
  Required Config Tags:
    [starboard]
    channel_id
    context_commands
    emoji_id
    emoji_count_threshold
  """
  def __init__(self, name, config, guild_id):
    super().__init__(name, config, guild_id)

  async def handle(self, message, message_event, client):
    match (message_event):
      case MessageEvent.on_message:
        await self.on_message(message, client)
      case MessageEvent.on_raw_reaction_add:
        await self.on_raw_reaction_add(message, client)   

  async def on_message(self, message, client):
    if message.content.startswith('!force'):
      args = message.content.split()
      await self.force_add(args[1], client)
    else:
      return

  async def on_raw_reaction_add(self, react_event, client):
    # behavior checks
    if (channel_id) == self.config.get('starboard', 'channel_id')):
      return

    react_emoji_id = str(react_event.emoji)
    channel_id = react_event.channel_id #ids are separated into individual pieces to make the add_to_starboard() function more modular
    message_id = react_event.message_id
    channel_obj = client.get_channel(channel_id)
    message_obj = await channel_obj.fetch_message(message_id)
    react_obj = await self.get_message_react_by_id(message_obj, react_emoji_id)

    # threshold check
    if (react_emoji_id == self.config['emoji_id'] and
        react_obj.count >= int(self.config['emoji_count_threshold'])
        ):
      await self.add_to_starboard(channel_id, message_id, client)
            
  async def add_to_starboard(self, channel_id, message_id, client):
    # yeah it sucks we have to get it twice blah blah fuck you i want this to be reusable code
    channel_obj = await client.fetch_channel(channel_id)
    message_obj = await channel_obj.fetch_message(message_id)
    react_obj = await self.get_message_react_by_id(message_obj, self.config['emoji_id'])

    # setup
    db = dataset.connect(f'sqlite:///guilds/{self.guild_id}/guild.db')
    table = db['starboard']
    data = table.find_one(message_id=message_id)
    starboard_channel = client.get_channel(int(self.config['channel_id']))

    # pre-existing data check
    if data == None:
      embed = await self.generate_starboard_embed(message_obj, react_obj)
      starboard_message = await starboard_channel.send(embed=embed)
      table.insert(dict(
        message_id = message_id,
        stars = react_obj.count,
        starboard_message_id = starboard_message.id))
    else:
      existing_data = table.find_one(message_id=message_id)
      embed = await self.generate_starboard_embed(message_obj, react_obj)
      starboard_message = await starboard_channel.fetch_message(existing_data['starboard_message_id'])
      new_message = await starboard_message.edit(embed=embed)
      table.upsert(dict(
          message_id = message_obj.id,
          stars = react_obj.count,
          starboard_message_id = starboard_message.id),
        ['mesage_id'])
    return
  
  async def force_add(self, args, client):
    data = args.split('/')
    # this should show up as something like:
    #   h..ps://discord.com/channels/numbers1/numbers2/numbers3
    #   we are interested in numbers2 (channel_id) and numbers3 (message_id)
    channel_id = data[-2]
    message_id = data[-1]
    await self.add_to_starboard(channel_id, message_id, client)

  async def generate_starboard_embed(self, message, react):
    # initialize embed
    embed = discord.Embed(
        description = message.content,
        color = int(hex(message.channel.id)[0:8], 16)
        )
    
    # set author and icon
    embed.set_author(name=message.author.display_name,
                     icon_url=str(message.author.avatar.url),
                     url=f'https://discordapp.com/users/{message.author.id}')
    
    # metadata setup
    fields = []
    fields.append(f'➡️ [original message]({message.jump_url}) in {message.channel.mention}')

    ## image embed
    if len(message.attachments) > 0:
      embed.set_image(url=message.attachments[0].url)
      for file in message.attachments:
        fields.append(f'📎 [{file.filename}]({file.url})')

    embed.add_field(name='\u200b',
                value='\n'.join(fields),
                inline=False)
    
    #footer
    try:
      embed.set_footer(text=f'{str(react.count)} ⭐ ({message.id}) • {message.created_at.strftime("%Y-%m-%d at %H:%M")} UTC')
    except AttributeError:
      # this only comes up when the forced message has no reacts
      embed.set_footer(text=f'**Forced** ⭐ ({message.id}) • {message.created_at.strftime("%Y-%m-%d at %H:%M")} UTC')

    return embed

  async def get_message_react_by_id(self, message, emoji_id):
    for r in message.reactions:
      if (str(r) == emoji_id):
        return r