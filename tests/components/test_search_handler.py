import unittest
from erudite.components import search_handler
from rhobot.components.storage import StoragePayload, ResultCollectionPayload, ResultPayload
from rdflib.namespace import FOAF
from rhobot.namespace import RHO, WGS_84
import mock


class SearchHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.search_handler = search_handler(None, None)

    def test_handling(self):

        payload = StoragePayload()
        payload.add_type(WGS_84.SpatialThing)

        self.assertTrue(self.search_handler._process_payload(payload))

        payload.add_type(FOAF.Agent)
        self.assertTrue(self.search_handler._process_payload(payload))

    def test_shouldnt_handle(self):

        payload = StoragePayload()
        payload.add_type(FOAF.Person)

        self.assertFalse(self.search_handler._process_payload(payload))

        payload = StoragePayload()
        payload.add_type(FOAF.Agent)

        self.assertFalse(self.search_handler._process_payload(payload))

        payload = StoragePayload()
        payload.add_type(RHO.Owner)

        self.assertFalse(self.search_handler._process_payload(payload))

        payload = StoragePayload()
        self.assertFalse(self.search_handler._process_payload(payload))

    def test_process_handler(self):
        """
        This is a method that should receive a collection of results, package them in a rdf payload to be sent off
        :return:
        """
        search_handler._rdf_publish = mock.MagicMock(**{'create_rdf.return': True})

        payload = ResultCollectionPayload()

        result = self.search_handler._handle_results(payload)
        self.assertTrue(result)

        payload.append(ResultPayload(about='uri:valid', types=[WGS_84.SpatialThing]))

        result = self.search_handler._handle_results(payload)
        self.assertTrue(result)



