"""
Set up the bot for execution.
"""
from rhobot.application import Application
from erudite.components.commands import load_commands
from erudite.components import load_components


application = Application()

# Register all of the components that are defined in this application.
application.pre_init(load_commands)
application.pre_init(load_components)

@application.post_init
def register_plugins(bot):
    # Bot specific plugins
    bot.register_plugin('knowledge_provider')
    bot.register_plugin('search_handler')

    # Commands
    bot.register_plugin('inject_triples')
    bot.register_plugin('find_owner')
