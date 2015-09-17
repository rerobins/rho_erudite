from rhobot.bot import RhoBot
from rhobot import configuration
import optparse

from erudite.components.commands import load_commands
from erudite.components import load_components

load_commands()
load_components()

parser = optparse.OptionParser()
parser.add_option('-c', dest="filename", help="Configuration file for the bot", default='erudite.rho')
(options, args) = parser.parse_args()

configuration.load_file(options.filename)

bot = RhoBot()

# Bot specific plugins
bot.register_plugin('knowledge_provider')
bot.register_plugin('search_handler')

# Commands
bot.register_plugin('inject_triples')
bot.register_plugin('find_owner')

# Connect to the XMPP server and start processing XMPP stanzas.
if bot.connect():
    bot.process(block=True)
else:
    print("Unable to connect.")
