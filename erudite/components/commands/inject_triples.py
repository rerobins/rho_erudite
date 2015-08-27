"""
Command that will allow for a user to inject triples into a database.
"""
from rhobot.components.commands.base_command import BaseCommand
from erudite.components.utilities import convert_rdf_json_to_storage
import logging
import json

logger = logging.getLogger(__name__)

class InjectTriples(BaseCommand):

    def initialize_command(self):
        super(InjectTriples, self).initialize_command()

        logger.info('Initialize Command')
        self._initialize_command(identifier='inject_triples', name='Inject Triples',
                                 additional_dependencies={'rho_bot_storage_client', })

    def command_start(self, request, initial_session):
        """
        Provide the configuration details back to the requester and end the command.
        :param request:
        :param initial_session:
        :return:
        """
        form = self.xmpp['xep_0004'].make_form()
        form.add_field(var='json_data', ftype='text-multi', label='RDF Content (JSON)')

        initial_session['payload'] = form
        initial_session['next'] = self.store_results
        initial_session['has_next'] = False

        return initial_session

    def store_results(self, request, session):
        """
        Store the contents of the json_data field into the database.
        :param request: request
        :param session: session value.
        :return: updated session value
        """
        injection_dictionary = json.loads(request['values']['json_data'])

        self.inject_nodes(injection_dictionary)

        session['notes'] = (('info', 'Triples imported to database',),)
        session['has_next'] = False
        session['next'] = None

        return session

    def inject_nodes(self, data):
        """
        Create all of the nodes with the literals and resources.
        :param data:
        :return:
        """
        bnode_mappings = dict()

        for uri, node_definition in data.iteritems():
            storage = convert_rdf_json_to_storage(node_definition, store_bnodes=False)
            result = self.xmpp['rho_bot_storage_client'].create_node(storage)
            bnode_mappings[uri] = result.results[0].about

        for uri, node_definition in data.iteritems():
            storage = convert_rdf_json_to_storage(node_definition, store_properties=False, store_types=False,
                                                  bnode_mappings=bnode_mappings)
            storage.about = bnode_mappings[uri]
            self.xmpp['rho_bot_storage_client'].update_node(storage)

        return bnode_mappings


inject_triples = InjectTriples
