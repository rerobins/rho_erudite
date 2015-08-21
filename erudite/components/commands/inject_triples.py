"""
Command that will allow for a user to inject triples into a database.
"""
from rhobot.components.commands.base_command import BaseCommand
from rdflib.namespace import RDF
import logging
import json

logger = logging.getLogger(__name__)

class InjectTriples(BaseCommand):

    def initialize_command(self):
        super(InjectTriples, self).initialize_command()

        logger.info('Initialize Command')
        self._initialize_command(identifier='inject_triples', name='Inject Triples',
                                 additional_dependencies={'rho_bot_storage_client'})

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

        injection_dictionary = json.loads(request['values']['json_data'])

        logger.info('Going to inject data: %s' % injection_dictionary)

        # This needs to go through and create all the nodes with the URI's and literals, then go through
        # and add all of the bnodes after all of the nodes have been inserted.
        self.create_nodes(injection_dictionary)

        logger.info('Finished')

        session['notes'] = (('info', 'Triples imported to database',),)
        session['has_next'] = False
        session['next'] = None

        return session

    def create_nodes(self, data):
        """
        Create all of the nodes with the literals and resources.
        :param data:
        :return:
        """
        bnode_mappings = dict()

        for uri, node_definition in data.iteritems():
            result = self.process_node_definition(uri, node_definition)
            bnode_mappings[uri] = result

        for uri, node_definition in data.iteritems():

            storage = self.xmpp['rho_bot_storage_client'].create_payload()
            storage.about = bnode_mappings[uri]

            for node_uri, values in node_definition.iteritems():

                for value in values:
                    if value['type'] == 'bnode':
                        storage.add_reference(node_uri, bnode_mappings[value['value']])

            result = self.xmpp['rho_bot_storage_client'].update_node(storage)

        return bnode_mappings

    def process_node_definition(self, uri, definition,):
        logger.info('Processing: %s %s' % (uri, definition))

        storage = self.xmpp['rho_bot_storage_client'].create_payload()

        for node_uri, values in definition.iteritems():

            if node_uri == str(RDF.type):
                for value in values:
                    storage.add_type(value['value'])
            else:
                for value in values:
                    if value['type'] == 'literal':
                        storage.add_property(node_uri, value['value'])

        result = self.xmpp['rho_bot_storage_client'].create_node(storage)

        logger.info('Retrieved back result: %s %s' % (uri, result))

        return result

inject_triples = InjectTriples
