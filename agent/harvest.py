import json
import logging
import os
import requests
from agent import config
from .transformer import transform_record

logger = logging.getLogger(__name__)


def _upload_record(result, settings):

    result['upload_error'] = None
    result['upload_success'] = False
    data = {
        'jsonData': json.dumps(result['datacite_data']),
        'metadataType': 'DataCite'
    }
    url = "{}/jsonCreateMetadataAsJson".format(settings['upload_server_url'])
    if settings.get('upload_user'):
        response = requests.post(
            url=url,
            data=data,
            auth=requests.auth.HTTPBasicAuth(
                settings['upload_user'], settings['upload_password']),
        )
    else:
        response = requests.post(
            url=url,
            data=data
        )
    if response.status_code != 200:
        result['upload_error'] = 'Request failed with return code: %s' % (
            response.status_code)
        print('Uploader: {upload_success}: {upload_error}'.format(**result))
        return result

    upload_result = json.loads(response.text)
    if upload_result.get('status') == 'failed':
        result['upload_error'] = upload_result('msg', 'Unknown')
        print('Uploader: {upload_success}: {upload_error}'.format(**result))
        return result

    result['upload_success'] = True
    print('Uploader: {upload_success}'.format(**result))
    return result


def _get_xml_records(settings):
    records = None
    standard = settings['standard']
    transport = settings['transport']
    if transport == "FTP":
        ftp = FTPTransport(settings.url, settings.username, settings.password)
        if ftp.message:
            error_message = ftp.message
            raise RuntimeError('%s\n%s' % (ftp.message, settings.getUrl()))
        records = ftp.getFiles()

    elif transport in ['CSW', 'CSW-NEW', 'CSW-SANSA']:
        csw = CSWTransport(settings.getUrl(), "", settings.username, settings.password, standard, transport=transport)
        if csw.message:
            error_message = csw.message
            raise RuntimeError('%s\n%s' % (csw.message, settings.getUrl()))
        records = csw.getRecords()

    elif transport in ['OAI', 'OAI-Metacat']:
        oai = OAITransport(url=settings.getUrl(), standard=standard, transport=transport, substitutionUrl=settings.substitutionUrl)
        if oai.message:
            error_message = oai.message
            raise RuntimeError('%s\n%s' % (oai.message, settings.getUrl()))
        records = oai.getRecords()

    elif transport == "HTTP":
        http = HTTPTransport(settings.url, settings.username, settings.password)
        if http.message:
            error_message = http.message
            raise RuntimeError('%s\n%s' % (http.message, settings.getUrl()))
        records = http.files

    elif transport == "FileSystem":
        files = []
        for afile in os.listdir(settings['source_dir']):
            if afile.lower().endswith('xml'):
                files.append(afile)
        logger.info('About to process {} files'.format(len(files)))

        records = []
        messages = []
        for filename in files:
            print('Process file {}'.format(filename))
            fullpath = os.path.join(settings['source_dir'], filename)
            if not os.path.isfile(fullpath):
                messages.append('Item {} is not a file'.format(filename))
                continue

            afile = open(fullpath)
            records.append({'title': filename, 'xml_data': afile.read()})
            afile.close()

        if messages:
            raise RuntimeError(', '.join(messages))

    else:
        msg = 'Harvester transport protocol "%s" not found' % transport or 'Unknown'
        error_message = msg
        raise RuntimeError(
            '%s\n%s' % (error_message, settings.getUrl()))

    return records


def _harvest_records(settings):
    """
    @summary: does the harvesting for the given type and url
    """
    output = {'success': False, 'records': []}

    logger.info('Harvesting: %s' % settings)
    records = _get_xml_records(settings)

    if records is None or len(records) == 0:
        output['error'] = 'No record found'
        return output

    logger.info('Harvester: %s records found in file' % len(records))

    for record in records:
        result = transform_record(record, settings)
        result = _upload_record(result, settings)
        output['records'].append(result)

    output['success'] = True
    return output


def harvest(kwargs):
    output = {'success': False}
    settings = {}

    settings['source_dir'] = config.source_dir
    if kwargs.get('source_dir'):
        settings['source_dir'] = kwargs.get('source_dir')

        if not os.path.exists(settings['source_dir']):
            output['error'] = 'source_dir {} does not exists'.format(
                settings['source_dir'])
            return output

        if os.listdir(settings['source_dir']) == []:
            output['error'] = 'source_dir {} is empty'.format(
                settings['source_dir'])
            return output

    settings['transport'] = config.transport
    if kwargs.get('transport'):
        settings['transport'] = kwargs.get('transport')

    settings['standard'] = config.standard
    if kwargs.get('standard'):
        settings['standard'] = kwargs.get('standard')

    settings['upload_server_url'] = config.upload_server_url
    if kwargs.get('upload_server_url'):
        settings['upload_server_url'] = kwargs.get('upload_server_url')

    settings['upload_user'] = config.upload_user
    if kwargs.get('upload_user'):
        settings['upload_user'] = kwargs.get('upload_user')

    settings['upload_password'] = config.upload_password
    if kwargs.get('upload_password'):
        settings['upload_password'] = kwargs.get('upload_password')

    results = _harvest_records(settings)

    return results
