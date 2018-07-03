from .standards.cbers_mux import transform_to_datacite as transform_cbers_mux
from .standards.cbers_mux import xml_processor as cbers_mux_processor
from .standards.cbers_p5m import transform_to_datacite as transform_cbers_p5m
from .standards.cbers_p5m import xml_processor as cbers_p5m_processor
from .standards.spot6 import transform_to_datacite as transform_spot6
from .standards.spot6 import xml_processor as spot6_processor


def transform_to_datacite(settings, meta):
    standard = settings.get('standard')
    if not standard:
        return {'datacite': None, 'errors': ['Standard not provided', ]}
    if standard == 'CBERS_MUX':
        return transform_cbers_mux(settings, meta)
    elif standard == 'CBERS_P5M':
        return transform_cbers_p5m(settings, meta)
    elif standard == 'SPOT6':
        return transform_spot6(settings, meta)
    return {'datacite': None,
            'errors': ['Unknown standard "{}"'.format(standard)]}


def get_xml_processor(settings):
    if settings['standard'] == 'CBERS_MUX':
        return cbers_mux_processor
    elif settings['standard'] == 'CBERS_P5M':
        return cbers_p5m_processor
    elif settings['standard'] == 'SPOT6':
        return spot6_processor
    return None
