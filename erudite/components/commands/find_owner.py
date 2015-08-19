"""
Command that will allow for a user to inject triples into a database.
"""
from rhobot.components.commands.base_command import BaseCommand
from rdflib.namespace import FOAF, RDF
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
        storage.add_type(FOAF.Person, 'rho::owner')

        results = self.xmpp['rho_bot_storage_client'].find_nodes(storage)

        form = self.xmpp['xep_0004'].make_form()
        form.add_reported(var='uri', ftype='text-single', label='Result URI')

        for uri in results['command']['form'].get_items():
            form.add_item(dict(uri=uri[str(RDF.about)]))

        initial_session['payload'] = form
        initial_session['next'] = None
        initial_session['has_next'] = False

        return initial_session

find_owner = FindOwner
