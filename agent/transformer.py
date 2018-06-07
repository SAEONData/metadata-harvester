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


def transform_record(record, settings):
    """
    @summary: extract the metadata from the given xml record
    @param: record thet contains the xml metadata and settings
    """

    meta = {'valid': False, 'error': None}
    xml_name = record['name']
    meta['title'] = xml_name
    meta['standard'] = settings['standard']
    logger.info('Parse record {}'.format(xml_name))

    # Strip all non ascii character
    data = record['xmlData']
    data = data.replace('\xe2\x80\x99', "'")
    data = data.encode('utf-8', 'strict')
    meta['xml'] = str(data)

    failed = _checkXmlStructure(data)

    if failed:
        meta['error'] = {
            'eventType': 'MetadataCreate',
            'category': 'Structure: Invalid XML',
            'logType': 'Error',
            'message': "Invalid Xml in document %s: %s " % (
                xml_name, failed),
        }
        return meta

    if settings['standard'] == 'CBERS':
        json_dict = xml.parse_from_string(cbers_processor, data)
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
