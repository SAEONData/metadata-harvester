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
    upload_method = settings.get(
        'upload_method', 'jsonCreateMetadataAsJson')

    # data = {
    #     'jsonData': json.dumps(result['datacite_data']),
    #     'metadataType': 'datacite'
    # }
    data = {
        'owner_org': 'webtide',
        'metadata_collection_id': 'unittest1',
        'metadata_standard_id': 'datacite-4-2',
        'metadata_json': json.dumps(result['datacite_data']),
        # 'infrastructures': [{'id': 'sansa'}],
        'deserialize_json': 'true',
        # '__ac_name': settings['upload_user'],
        # '__ac_password': 'mike01',  # settings['upload_password'],
    }
    headers = {
        'Authorization': settings['upload_password'],
    }
    url = "{}/{}".format(settings['upload_server_url'], upload_method)
    print(url)
    print(data)
    print(headers)
    try:
        # CKAN create_metadata(self, institution, repository, **kwargs)

        if False:  # settings.get('upload_user'):
                response = requests.post(
                    url=url,
                    data=data,
                    auth=requests.auth.HTTPBasicAuth(
                        settings['upload_user'], settings['upload_password']),
                )
        else:
            response = requests.post(
                url=url,
                data=data,
                headers=headers
            )
    except Exception as e:
        print(response.text)
        result['upload_error'] = 'Request failed with exception {}.'.format(e)
        print('Uploader: {upload_success}: {upload_error}'.format(**result))
        return result
    if response.status_code != 200:
        print(response.text)
        result['upload_error'] = 'Request failed with return code: %s' % (
            response.status_code)
        print('Uploader: {upload_success}: {upload_error}'.format(**result))
        return result

    upload_result = json.loads(response.text)
    if upload_result.get('status') == 'failed':
        result['upload_error'] = upload_result.get('msg', 'Unknown')
        print('Uploader: {upload_success}: {upload_error}'.format(**result))
        return result

    result['upload_success'] = True
    print('Uploader: {upload_success}'.format(**result))
    return result


def _get_metadata_records(settings):
    result = {'records': [], 'errors': []}
    records = None
    transport = settings.get('transport')
    if transport == "FileSystem":
        files = []
        for afile in os.listdir(settings['source_dir']):
            files.append(afile)
        logger.info('About to process {} files'.format(len(files)))

        if len(files) == 0:
            result['errors'] = \
                'No files in dir {}'.format(settings['source_dir'])
            return result
        records = []
        messages = []
        for filename in files:
            print('Process file {}'.format(filename))
            fullpath = os.path.join(settings['source_dir'], filename)
            if not os.path.isfile(fullpath):
                messages.append('Item {} is not a file'.format(filename))
                continue

            afile = open(fullpath)
            records.append({'title': filename, 'input_data': afile.read()})
            afile.close()

        if messages:
            result['errors'] = messages
            return result

    else:
        msg = 'Harvester transport protocol "{}" not found'.format(transport)
        result['errors'].append(msg)
        return result

    result['records'] = records
    return result


def _harvest_records(settings):
    """
    @summary: does the harvesting for the given type and url
    """
    output = {'success': False, 'records': []}

    logger.info('Harvesting: %s' % settings)
    result = _get_metadata_records(settings)

    records = result['records']
    if records is None or len(records) == 0:
        output['error'] = result['errors']
        return output

    logger.info('Harvester: %s records found in file' % len(records))

    for record in records:
        result = transform_record(record, settings)
        if result['valid']:
            result = _upload_record(result, settings)
        else:
            logger.info('Harvester: Invalid record')
        output['records'].append(result)

    output['success'] = True
    return output


def harvest(kwargs):
    output = {'success': False}
    settings = {}

    if hasattr(config, 'source_dir'):
        settings['source_dir'] = config.source_dir
    if kwargs.get('source_dir'):
        settings['source_dir'] = kwargs.get('source_dir')

        if not os.path.exists(settings['source_dir']):
            output['error'] = 'source_dir {} does not exists'.format(
                settings['source_dir'])
            return output

        files = os.listdir(settings['source_dir'])
        if len(files) == 0:
            output['error'] = 'source_dir {} is empty'.format(
                settings['source_dir'])
            return output

    if hasattr(config, 'transport'):
        settings['transport'] = config.transport
    if kwargs.get('transport'):
        settings['transport'] = kwargs.get('transport')

    if hasattr(config, 'standard'):
        settings['standard'] = config.standard
    if kwargs.get('standard'):
        settings['standard'] = kwargs.get('standard')

    if hasattr(config, 'upload_server_url'):
        settings['upload_server_url'] = config.upload_server_url
    if kwargs.get('upload_server_url'):
        settings['upload_server_url'] = kwargs.get('upload_server_url')

    if hasattr(config, 'upload_user'):
        settings['upload_user'] = config.upload_user
    if kwargs.get('upload_user'):
        settings['upload_user'] = kwargs.get('upload_user')

    if hasattr(config, 'upload_password'):
        settings['upload_password'] = config.upload_password
    if kwargs.get('upload_password'):
        settings['upload_password'] = kwargs.get('upload_password')

    if hasattr(config, 'upload_method'):
        settings['upload_method'] = config.upload_method
    if kwargs.get('upload_method'):
        settings['upload_method'] = kwargs.get('upload_method')

    results = _harvest_records(settings)

    return results
