from erudite.components.knowledge_provider import knowledge_provider
from erudite.components.search_handler import search_handler

from sleekxmpp.plugins.base import register_plugin


def load_components():
    register_plugin(knowledge_provider)
    register_plugin(search_handler)
