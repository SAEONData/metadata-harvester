import json
import requests
import sys


def harvest_folder(source_dir, standard):
    output = {'success': False}

    data = {
        'source_dir': source_dir,
        'transport': 'FileSystem',
        'standard': standard,
        'upload_server_url': 'http://ckan.dirisa.org:9090/Institutions/webtide/sansa3/metadata'
    }
    base = 'http://localhost:8080'
    url = "{}/harvest".format(base)
    print(url)
    response = requests.post(
        url=url,
        data=data,
    )
    if response.status_code != 200:
        output['error'] = 'Request failed with return code: %s' % (
            response.status_code)
        return output

    results = json.loads(response.text)
    output['results'] = results
    output['success'] = results['success']
    return output


if __name__ == "__main__":
    # source_dir = '/home/mike/projects/harvester/data/CBERS'
    # standard = 'CBERS'
    source_dir = '/home/mike/projects/harvester/data/SPOT6'
    standard = 'SPOT6'

    output = harvest_folder(source_dir, standard)

    results = output['results']
    if not output.get('success', False):
        print('Harvest failed, reason: {}'.format(results.get('error', 'unknown')))
        sys.exit()

    print('Harvest {}'.format(output['success']))
    for record in results['records']:
        if record['valid']:
            print('{title}: Valid = {valid}, Upload = {upload_success} {upload_error}'.format(**record))
        else:
            print('{title}: Valid = {valid}, Error = {error}, Upload = {upload_success} {upload_error}'.format(**record))
