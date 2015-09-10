"""
Knowledge provider that will respond to requests made by the rdf publisher or another bot.
"""
from sleekxmpp.plugins.base import base_plugin
from rhobot.components.storage.client import StoragePayload
from rhobot.components.stanzas.rdf_stanza import RDFStanzaType
from rdflib.namespace import FOAF
from rhobot.namespace import RHO
import logging

logger = logging.getLogger(__name__)


class KnowledgeProvider(base_plugin):
    name = 'knowledge_provider'
    description = 'Knowledge Provider'
    dependencies = {'rho_bot_storage_client', 'rho_bot_rdf_publish', }

    type_requirements = {str(FOAF.Person), str(RHO.Owner), }

    def plugin_init(self):
        """
        Does nothing.
        :return:
        """
        pass

    def post_init(self):
        """
        Configure the pointer helpers and add this handler to the request handler of the rdf publisher.
        """
        base_plugin.post_init(self)

        self._storage_client = self.xmpp['rho_bot_storage_client']
        self._rdf_publish = self.xmpp['rho_bot_rdf_publish']

        self._rdf_publish.add_request_handler(self._rdf_request_message)

    def _rdf_request_message(self, rdf_payload):
        """
        Handler that will determine if the provider can provide details for the requested values.
        :param rdf_payload:
        :return:
        """
        logger.debug('Looking up knowledge')

        form = rdf_payload['form']

        payload = StoragePayload(form)

        # This will limit the data that this provider will return to requests that are looking for
        # FOAF.Person and RHO.Owner
        intersection = self.type_requirements.intersection(set(payload.types))

        if len(intersection) == len(payload.types):
            promise = self._storage_client.find_nodes(payload).then(self._process_find_nodes)
        else:
            promise = None

        return promise

    def _process_find_nodes(self, results):
        """
        Process the results of the find nodes and return the results if there are values present.  Otherwise returns
        None.
        :param results:
        :return:
        """
        if len(results.results):
            rdf_data = self._rdf_publish.create_rdf(mtype=RDFStanzaType.SEARCH_RESPONSE, payload=results)
            return rdf_data

        return None

knowledge_provider = KnowledgeProvider
