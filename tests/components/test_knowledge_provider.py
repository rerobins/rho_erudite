import unittest
from erudite.components import knowledge_provider
from rhobot.components.stanzas.rdf_stanza import RDFStanzaType
from rhobot.components.storage import StoragePayload, ResultCollectionPayload, ResultPayload
from rdflib.namespace import FOAF
from rhobot.namespace import RHO
import mock


class KnowledgeProviderTestCase(unittest.TestCase):

    def setUp(self):
        self.knowledge_provider = knowledge_provider(None, None)

    def test_handling(self):

        payload = StoragePayload()
        payload.add_type(FOAF.Person, RHO.Owner)

        self.assertTrue(self.knowledge_provider._process_payload(payload))

        payload.add_type(FOAF.Agent)
        self.assertTrue(self.knowledge_provider._process_payload(payload))

    def test_shouldnt_handle(self):

        payload = StoragePayload()
        payload.add_type(FOAF.Person)

        self.assertFalse(self.knowledge_provider._process_payload(payload))

        payload = StoragePayload()
        payload.add_type(FOAF.Agent)

        self.assertFalse(self.knowledge_provider._process_payload(payload))

        payload = StoragePayload()
        payload.add_type(RHO.Owner)

        self.assertFalse(self.knowledge_provider._process_payload(payload))

        payload = StoragePayload()
        self.assertFalse(self.knowledge_provider._process_payload(payload))

    def test_process_handler(self):
        """
        This is a method that should receive a collection of results, package them in a rdf payload to be sent off
        :return:
        """
        knowledge_provider._rdf_publish = mock.MagicMock(**{'create_rdf.return': True})

        payload = ResultCollectionPayload()

        result = self.knowledge_provider._process_find_nodes(payload)
        self.assertIsNone(result)

        payload.append(ResultPayload(about='uri:valid', types=[FOAF.Person, RHO.Owner]))
        result = self.knowledge_provider._process_find_nodes(payload)
        self.assertTrue(result)

        args, kwargs = knowledge_provider._rdf_publish.create_rdf.call_args

        self.assertEqual(kwargs['mtype'], RDFStanzaType.SEARCH_RESPONSE)
        self.assertIs(kwargs['payload'], payload)


