import logging
import xml.dom.minidom as minidom
import declxml
from agent.standard import get_processor
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
    # data = data.encode('utf-8', 'strict')
    return data


def transform_record(record, settings):
    """
    @summary: extract the metadata from the given record
    @param: record thet contains the xml metadata and settings
    """

    meta = {'valid': False, 'error': None, 'title': 'Unknown',
            'upload_success': False, 'upload_error': 'No attempt'}
    standard = settings.get('standard')
    if not standard:
        meta['error'] = {
            'message': "Stardard not provided"
        }
        return meta
    meta['standard'] = standard
    title = record['title']
    meta['title'] = title
    logger.info('Parse record {}'.format(title))

    meta['input_data'] = record['input_data']

    processor = get_processor(settings)
    if not processor:
        meta['error'] = {
            'message': "Cannot transform standard {} yet".format(
                settings['standard']),
        }
        return meta

    if standard in ('CBERS_MUX', 'CBERS_P5M', 'CBERS_P10', 'SPOT6'):
        input_data = _clean_xml_data(record['input_data'])
        meta['input_data'] = str(input_data)

        failed = _checkXmlStructure(input_data)
        if failed:
            meta['error'] = {
                'message': "Invalid Xml in document {}: {}".format(
                    title, failed),
            }
            return meta

        try:
            json_data = declxml.parse_from_string(processor, input_data)
        except declxml.MissingValue as e:
            meta['error'] = {
                'message': "{}".format(e)
            }
            return meta
    else:
        try:
            json_data = processor(meta, record['input_data'])
        except declxml.MissingValue as e:
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
        'category': "Record Transformed",
        'logType': 'Success',
        'message': "Transform document {title}".format(**meta),
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

    if kwargs.get('input_data'):
        record['input_data'] = kwargs.get('input_data')
    else:
        output['error'] = {'message': 'input data is required'}
        return output

    if kwargs.get('standard'):
        source_settings['standard'] = kwargs.get('standard')
    else:
        output['error'] = {'message': 'metadata standard is required'}
        return output

    results = transform_record(record, source_settings)

    results['success'] = results.get('valid', False)

    return results
