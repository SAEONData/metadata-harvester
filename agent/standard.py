from .cbers import transform_to_datacite as transform_cbers
from .cbers import xml_processor as cbers_processor
from .spot6 import transform_to_datacite as transform_spot6
from .spot6 import xml_processor as spot6_processor


def transform_to_datacite(settings, meta):
    if settings['standard'] == 'CBERS':
        return transform_cbers(settings, meta)
    elif settings['standard'] == 'SPOT6':
        return transform_spot6(settings, meta)
    return None


def get_xml_processor(settings):
    if settings['standard'] == 'CBERS':
        return cbers_processor
    elif settings['standard'] == 'SPOT6':
        return spot6_processor
    return None
