import json
import requests
import sys


def harvest_folder(source_dir, standard, upload_server_url=None):
    output = {'success': False}

    if upload_server_url is None:
        upload_server_url = 'http://ckan.dirisa.org:9090/Institutions/webtide/sansa4/metadata'

    data = {
        'source_dir': source_dir,
        'transport': 'FileSystem',
        'standard': standard,
        'upload_server_url': upload_server_url,
        'upload_method': 'jsonCreateMetadataAsJson',
    }
    base = 'http://localhost:8080'
    url = "{}/harvest".format(base)
    print(url)
    # print(data)
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


if __name__ == "__main__":

    sources = [
        {
            'source_dir': '/home/mike/projects/harvester/data/CBERS_MUX',
            'standard': 'CBERS_MUX',
            'upload_server_url': 'http://ckan.dirisa.org:9090/Institutions/webtide/cbers_mux/metadata',
        }, {
            'source_dir': '/home/mike/projects/harvester/data/CBERS_P5M',
            'standard': 'CBERS_P5M',
            'upload_server_url': 'http://ckan.dirisa.org:9090/Institutions/webtide/cbers_p5m/metadata',
        },
        {
            'source_dir': '/home/mike/projects/harvester/data/SPOT6',
            'standard': 'SPOT6',
            'upload_server_url': 'http://ckan.dirisa.org:9090/Institutions/webtide/spot6/metadata',
        }
    ]
    for source in sources:
        output = harvest_folder(
            source['source_dir'],
            source['standard'],
            source.get('upload_server_url', None))

        if not output.get('success', False):
            error = output.get('results', 'unknown')
            if isinstance(error, dict):
                error = error.get('error', 'unknown')
            print('Harvest failed, reason: {}'.format(error))
            sys.exit()

        print('Harvest {}'.format(output['success']))
        results = output['results']
        for record in results['records']:
            if record['valid']:
                print('{title}: Valid = {valid}, Upload = {upload_success} {upload_error}'.format(**record))
            else:
                print('{title}: Valid = {valid}, Error = {error}, Upload = {upload_success} {upload_error}'.format(**record))
