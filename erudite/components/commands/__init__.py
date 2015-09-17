from erudite.components.commands.inject_triples import inject_triples
from erudite.components.commands.find_owner import find_owner

from sleekxmpp.plugins.base import register_plugin


def load_commands():
    register_plugin(inject_triples)
    register_plugin(find_owner)
