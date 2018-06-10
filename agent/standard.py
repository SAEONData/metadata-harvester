from standards.cbers import transform_to_datacite as transform_cbers
from standards.cbers import cbers_processor


def transform_to_datacite(settings, meta):
    if settings['standard'] == 'CBERS':
        return transform_cbers
    return None


def get_xml_processor(settings):
    if settings['standard'] == 'CBERS':
        return cbers_processor
    return None
