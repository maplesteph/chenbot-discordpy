import configparser

config = configparser.ConfigParser()
config.read('./182996941339099136/config.ini')
print(dict(config['config']))