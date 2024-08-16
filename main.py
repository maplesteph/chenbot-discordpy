import getopt
import sys
import time

import configparser

from modulardiscordbot import ModularDiscordBot

# Startup
def main(argv):
  CONFIG_FILE = 'config.ini'
  config = configparser.ConfigParser()
  config.read(CONFIG_FILE)
  token = config.get('discord', 'default_token')
    
  debug = False
  short_opts = 'dhl'
  long_opts = ['debug', 'help', 'lumi']

  try:
    opts, args = getopt.getopt(argv[1:], short_opts, long_opts)
  except getopt.error as err:
    print(str(err))
    sys.exit(1)
    
  for opt, arg in opts:
    if opt in ('-d', '--debug'):
      debug = True
      token = config.get('discord', 'debug_token')
    elif opt in ('-h', '--help'):
      #print_help()
      return
    elif opt in ('-l', '--lumi'):
      token = config.get('discord', 'lumi_token')

  bot = ModularDiscordBot(config, debug)
  bot.run(token)

def print_help():
  print("    d, debug        Run as ChenTest")
  print("    l, lumi         Run as Lumi")

main(sys.argv)
