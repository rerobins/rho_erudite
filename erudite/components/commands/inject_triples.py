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
                                 additional_dependencies={'rho_bot_storage_client', 'rho_bot_scheduler', })

    def post_init(self):
        self._form_plugin = self.xmpp['xep_0004']
        self._storage_client = self.xmpp['rho_bot_storage_client']
        self._scheduler = self.xmpp['rho_bot_scheduler']

    def command_start(self, request, initial_session):
        """
        Provide the configuration details back to the requester and end the command.
        :param request:
        :param initial_session:
        :return:
        """
        form = self._form_plugin.make_form()
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

        self._inject_nodes(injection_dictionary)

        session['notes'] = (('info', 'Triples imported to database',),)
        session['has_next'] = False
        session['next'] = None

        return session

    def _inject_nodes(self, data):
        """
        Create all of the nodes with the literals and resources.

        This will attempt to split up all of the work into multiple promises that will be executed serially.  The work
        is done by first storing all of the properties and the type information of the nodes into the database.  When
        the storage client returns the identifier for the node, that node will need to be stored in a mappings object
        so that on the second pass, all of the references can be put into place for the bnodes.


        :param data:
        :return:
        """
        bnode_mappings = dict()

        # Clean up some short hand for generating the promises.
        g_p_h = self._scheduler.generate_promise_handler

        promise = self._scheduler.defer(lambda: dict())

        def store_result(_result, _mappings, _uri):
            _mappings[_uri] = _result.results[0].about
            return _mappings

        def store_and_update_session(_session, _uri, _definition):
            _storage = convert_rdf_json_to_storage(_definition, store_bnodes=False)
            _promise = self._storage_client.create_node(_storage)
            return _promise.then(g_p_h(store_result, _session, _uri))

        def store_node_mappings(_session, _uri, _definition):
            _storage = convert_rdf_json_to_storage(_definition, store_properties=False, store_types=False,
                                                   bnode_mappings=bnode_mappings)
            _storage.about = bnode_mappings[_uri]
            _promise = self._storage_client.update_node(_storage)

            return _promise.then(lambda s: _session)

        for uri, node_definition in data.iteritems():
            promise = promise.then(g_p_h(store_and_update_session, uri, node_definition))

        for uri, node_definition in data.iteritems():
            promise = promise.then(g_p_h(store_node_mappings(bnode_mappings, uri, node_definition)))

        return promise


inject_triples = InjectTriples
