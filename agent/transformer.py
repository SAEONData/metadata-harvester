import logging
import xml.dom.minidom as minidom
import declxml as xml

logger = logging.getLogger(__name__)

cbers_processor = xml.dictionary('root/data', [
    xml.string('productId'),
    xml.integer('sceneId')
])


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


def _get_xml_processor(settings):
    if settings['standard'] == 'CBERS':
        return cbers_processor
    return None


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

    meta = {'valid': False, 'error': None}
    title = record['title']
    meta['title'] = title
    meta['standard'] = settings['standard']
    logger.info('Parse record {}'.format(title))

    data = _clean_xml_data(record['xmlData'])
    meta['xml'] = str(data)

    xml_processor = _get_xml_processor(settings)
    if not xml_processor:
        meta['error'] = {
            'message': "Cannot transform standard {} yet".format(
                settings['standard']),
        }
        return meta

    failed = _checkXmlStructure(data)
    if failed:
        meta['error'] = {
            'message': "Invalid Xml in document {}: {}".format(
                title, failed),
        }
        return meta

    json_dict = xml.parse_from_string(xml_processor, data)
    meta['jsonData'] = json_dict

    # meta['jsonData']['additionalFields']['source_uri'] = uri
    # if len(self.getDefaultValues()) and len(meta.jsonData):
    #     self._addDefaultValues(meta)

    # if len(self.getSupplementaryValues()) and len(meta.jsonData):
    #     self._addSupplementaryValues(meta)

    # if self.doiRange != 'none' and len(meta.jsonData):
    #     self._addIdentifier(meta)

    if meta['jsonData'].get('title') and \
       meta['jsonData']['title'].strip() != "":
        # set the metadata object title to that of the xml title
        meta['title'] = meta['jsonData']['title']

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

    if kwargs.get('xmlData'):
        record['xmlData'] = kwargs.get('xmlData')
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
