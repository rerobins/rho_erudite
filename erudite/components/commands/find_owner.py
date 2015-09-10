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

    def initialize_command(self):
        super(FindOwner, self).initialize_command()

        logger.info('Initialize Command')
        self._initialize_command(identifier='find_owner', name='Find Owner',
                                 additional_dependencies={'rho_bot_storage_client', 'rho_bot_scheduler', })

    def post_init(self):
        """
        Clean up fetching of dependency plugins.
        :return:
        """
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
