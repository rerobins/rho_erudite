"""
Utilities for the Erudite bot.
"""
from rhobot.components.storage import StoragePayload
from rdflib.namespace import RDF
import logging


logger = logging.getLogger(__name__)


def convert_rdf_json_to_storage(definition, store_types=True, store_properties=True, store_bnodes=True,
                                bnode_mappings=None):
    """
    Convert RDF JSON values into a storage payload.
    :param definition:  dictionary containing the json data.
    :param store_types: should store the type values of the definition.
    :param store_properties: should store the property values of the definition.
    :param store_bnodes: should store the bnodes of the definition.
    :param bnode_mappings: dictionary containing a translation key for the bnodes.
    :return: newly created storage payload object.
    """
    if not bnode_mappings:
        bnode_mappings = {}

    result = StoragePayload()

    for node_uri, values in definition.iteritems():

        if node_uri == str(RDF.type):
            if store_types:
                for value in values:
                    result.add_type(value['value'])
        else:
            for value in values:
                if store_properties and value['type'] == 'literal':
                    result.add_property(node_uri, value['value'])
                elif store_bnodes and value['type'] == 'bnode':
                    if value['value'] in bnode_mappings:
                        result.add_reference(node_uri, bnode_mappings[value['value']])
                    else:
                        logger.error('Couldn\'t find bnode mapping for: %s' % value['value'])

    return result

