"""
Command that will allow for a user to inject triples into a database.
"""
from rhobot.components.commands.base_command import BaseCommand
from rdflib.namespace import FOAF
from rhobot.namespace import RHO
from rhobot.components.storage import StoragePayload
import logging

logger = logging.getLogger(__name__)


class FindOwner(BaseCommand):

    name = 'find_owner'
    description = 'Find Owner'
    dependencies = BaseCommand.default_dependencies.union({'rho_bot_storage_client', })

    def post_init(self):
        """
        Clean up fetching of dependency plugins.
        :return:
        """
        super(FindOwner, self).post_init()
        self._storage_client = self.xmpp['rho_bot_storage_client']

    def command_start(self, request, initial_session):
        """
        Provide the configuration details back to the requester and end the command.
        :param request:
        :param initial_session:
        :return:
        """

        storage = StoragePayload()
        storage.add_type(FOAF.Person, RHO.Owner)

        promise = self._storage_client.find_nodes(storage)

        def find_nodes_processor(results):
            """
            Process the results and place the payload into the initial session value.
            :param results:
            :return: the initial session value.
            """
            initial_session['payload'] = results.populate_payload()

            return initial_session

        # Finish populating the rest of initial_session values.
        initial_session['next'] = None
        initial_session['has_next'] = False

        return promise.then(find_nodes_processor)


find_owner = FindOwner
