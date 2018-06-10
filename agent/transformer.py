import logging
import xml.dom.minidom as minidom
import declxml as xml
from agent.standard import get_xml_processor
from agent.standard import transform_to_datacite

logger = logging.getLogger(__name__)


def _checkXmlStructure(data):
    """
    @summary: checks the structure of the xml to check if it is valid xml
    @param data: can be an xml string
    """
    try:
        d = minidom.parseString(data)
        d = str(d.toxml())
        return None
    except Exception as e:
        return str(e)


def _clean_xml_data(data):
    # Strip all non ascii character
    data = data.replace('\xe2\x80\x99', "'")
    data = data.encode('utf-8', 'strict')
    return data


def transform_record(record, settings):
    """
    @summary: extract the metadata from the given xml record
    @param: record thet contains the xml metadata and settings
    """

    meta = {'valid': False, 'error': None,
            'upload_success': False, 'upload_error': 'No attempt'}
    title = record['title']
    meta['title'] = title
    meta['standard'] = settings['standard']
    logger.info('Parse record {}'.format(title))

    xml_data = _clean_xml_data(record['xml_data'])
    meta['xml_data'] = str(xml_data)

    failed = _checkXmlStructure(xml_data)
    if failed:
        meta['error'] = {
            'message': "Invalid Xml in document {}: {}".format(
                title, failed),
        }
        return meta

    xml_processor = get_xml_processor(settings)
    if not xml_processor:
        meta['error'] = {
            'message': "Cannot transform standard {} yet".format(
                settings['standard']),
        }
        return meta

    try:
        json_data = xml.parse_from_string(xml_processor, xml_data)
    except xml.MissingValue as e:
        meta['error'] = {
            'message': "{}".format(e)
        }
        return meta
    meta['json_data'] = json_data

    datacite = transform_to_datacite(settings, meta)
    meta['datacite_data'] = datacite

    # meta['json_data']['additionalFields']['source_uri'] = uri
    # if len(self.getDefaultValues()) and len(meta.json_data):
    #     self._addDefaultValues(meta)

    # if len(self.getSupplementaryValues()) and len(meta.json_data):
    #     self._addSupplementaryValues(meta)

    # if self.doiRange != 'none' and len(meta.json_data):
    #     self._addIdentifier(meta)

    if meta['json_data'].get('title') and \
       meta['json_data']['title'].strip() != "":
        # set the metadata object title to that of the xml title
        meta['title'] = meta['json_data']['title']

    msg = {
        'eventType': "MetadataCreate",
        'category': "Record Created",
        'logType': 'Success',
        'message': "Created document {title}".format(**meta),
    }
    print(msg)
    meta['valid'] = True
    return meta


def transform(kwargs):
    output = {'success': False}
    source_settings = {}

    record = {}
    if kwargs.get('title'):
        record['title'] = kwargs.get('title')
    else:
        output['error'] = {'message': 'record title is required'}
        return output

    if kwargs.get('xml_data'):
        record['xml_data'] = kwargs.get('xml_data')
    else:
        output['error'] = {'message': 'xml data is required'}
        return output

    if kwargs.get('standard'):
        source_settings['standard'] = kwargs.get('standard')
    else:
        output['error'] = {'message': 'metadata standard is required'}
        return output

    results = transform_record(record, source_settings)

    return results
