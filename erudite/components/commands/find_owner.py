"""
Command that will allow for a user to inject triples into a database.
"""
from rhobot.components.commands.base_command import BaseCommand
from rdflib.namespace import FOAF, RDF
from rhobot.namespace import RHO
from rhobot.components.storage import ResultPayload, ResultCollectionPayload
import logging

logger = logging.getLogger(__name__)

class FindOwner(BaseCommand):

    def initialize_command(self):
        super(FindOwner, self).initialize_command()

        logger.info('Initialize Command')
        self._initialize_command(identifier='find_owner', name='Find Owner',
                                 additional_dependencies={'rho_bot_storage_client'})

    def command_start(self, request, initial_session):
        """
        Provide the configuration details back to the requester and end the command.
        :param request:
        :param initial_session:
        :return:
        """

        storage = self.xmpp['rho_bot_storage_client'].create_payload()
        storage.add_type(FOAF.Person, RHO.Owner)

        results = self.xmpp['rho_bot_storage_client'].find_nodes(storage)

        initial_session['payload'] = results._populate_payload()
        initial_session['next'] = None
        initial_session['has_next'] = False

        return initial_session

find_owner = FindOwner
