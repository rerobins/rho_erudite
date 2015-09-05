"""
Service that will find the most commonly used locations in events (ideally these would be the most popular) that are
defined by foursquare data and return them back.
"""

import logging
import json

from rhobot.components.storage.enums import CypherFlags

from sleekxmpp.plugins.base import base_plugin
from rhobot.namespace import WGS_84, SCHEMA, EVENT, LOCATION
from rhobot.components.storage import StoragePayload
from rhobot.components.storage.namespace import NEO4J

logger = logging.getLogger(__name__)


class SearchHandler(base_plugin):
    """
    Search the database for the content
    """
    name = 'search_handler'
    description = 'Knowledge Provider'
    dependencies = {'rho_bot_storage_client', 'rho_bot_rdf_publish', }

    type_requirements = {str(WGS_84.SpatialThing), }

    def plugin_init(self):
        pass

    def post_init(self):
        base_plugin.post_init(self)
        self.xmpp['rho_bot_rdf_publish'].add_search_handler(self._rdf_request_message)

    def _rdf_request_message(self, rdf_payload):
        """
        Find node to do work over.
        :return:
        """
        query = """MATCH (n:`%s`:`%s`)<-[r:`%s`]-(m)
                   RETURN n AS node, count(r) AS rels, n.`%s` AS name
                   ORDER BY rels DESC LIMIT 10""" % (str(WGS_84.SpatialThing),
                                                     str(LOCATION.Address),
                                                     str(EVENT.place),
                                                     str(SCHEMA.name))

        translation_key = dict()
        translation_key.update(json.loads(CypherFlags.TRANSLATION_KEY.default))
        translation_key[str(SCHEMA.name)] = 'name'
        translation_key['http://degree'] = 'rels'

        logger.debug('Executing query: %s' % query)

        payload = StoragePayload()
        payload.add_property(key=NEO4J.cypher, value=query)
        payload.add_flag(CypherFlags.TRANSLATION_KEY, json.dumps(translation_key))

        result = self.xmpp['rho_bot_storage_client'].execute_cypher(payload)

        print 'Found: %s results' % len(result.results)

        for res in result.results:
            print '  %s (%s)' % (res.get_column(str(SCHEMA.name)), res.get_column('http://degree'))

        return result, None


search_handler = SearchHandler
