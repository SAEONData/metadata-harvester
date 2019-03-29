import argparse
import json
import requests
from pathlib import Path


def harvest_folder(settings):
    output = {'success': False}

    data = {
        'source_dir': settings.get('source_dir'),
        'standard': settings.get('standard'),
        'upload_server_url': settings.get('upload_server_url'),
        'upload_user': settings.get('upload_user'),
        'upload_password': settings.get('upload_password'),
        'transport': 'FileSystem',
        'upload_method': settings.get('upload_method'),
        'upload_org_name': settings.get('upload_org_name'),
        'upload_collection': settings.get('upload_collection'),
    }
    if settings.get('upload_index'):
        data['upload_index'] = settings['upload_index']

    base = 'http://localhost:8080'
    url = "{}/harvest".format(base)
    try:
        response = requests.post(
            url=url,
            data=data,
        )
    except Exception as e:
        output['results'] = {
            'error': 'Request to {} failed with {}'.format(url, e)}
        return output

    if response.status_code != 200:
        output['results'] = {
            'error': 'Request to {} failed with code {}'.format(
                url, response.status_code)}
        return output

    results = json.loads(response.text)
    output['results'] = results
    output['success'] = results['success']
    return output


def _harvest_sources(filename):
    sources_file = Path(filename)
    if not sources_file.is_file():
        return "Sources file {} doesn't exist".format(filename)

    with open(sources_file) as sources_data:
        try:
            sources = json.load(sources_data)
        except Exception as e:
            return str(e)

    all_good = True
    for source in sources:
        output = harvest_folder(source)

        if not output.get('success', False):
            error = output.get('results', 'unknown')
            if isinstance(error, dict):
                error = error.get('error', 'unknown')
            print('Harvest failed, reason: {}'.format(error))
            all_good = False
            continue

        results = output['results']
        print('Harvest success {} : dir {}, num {}'.format(
            output['success'],
            source.get('source_dir'),
            len(results['records'])))
        for record in results['records']:
            if not record['valid']:
                print('{title}: Transform = {valid}, Error = {error}'.format(**record))
                all_good = False
                continue
            if not record['upload_success']:
                print('{title}: Upload = {upload_success} {upload_error}'.format(**record))
                all_good = False
                continue
            # if not record['validation_success']:
            #     print('{title}: Validation = {validation_success} {validation_errors}'.format(**record))
            #     all_good = False
            #     continue

    if all_good:
        return 'Tests completed successfully'
    else:
        return 'Tests complete - see issues above'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Harvest provided sources.')
    parser.add_argument(
        '--sources',
        help='Filename that contains the list of sources')

    args = vars(parser.parse_args())
    sources = args['sources']
    if sources is None:
        sources = 'tests/sources.json'

    result = _harvest_sources(sources)
    print(result)
