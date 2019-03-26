import json
import requests


def harvest_folder(settings):
    output = {'success': False}

    data = {
        'source_dir': settings.get('source_dir', '/agent/tests/cbers_mux'),
        'standard': settings.get('standard', 'CBERS_MUX'),
        'upload_server_url': settings.get('upload_server_url'),
        'upload_user': settings.get('upload_user'),
        'upload_password': settings.get('upload_password'),
        'transport': 'FileSystem',
        'upload_method': settings.get('upload_method', 'jsonCreateMetadataAsJson'),
    }
    base = 'http://localhost:8080'
    url = "{}/harvest".format(base)
    # print(url)
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
            # 'source_dir': '/home/mike/projects/harvester/data/CBERS_MUX',
            'source_dir': './agent/tests/cbers_mux',
            'standard': 'CBERS_MUX',
            # 'upload_server_url': 'https://ckan.sansa.saeoss.org/organization/webtide/metadata_collection/unittest1/metadata',
            'upload_server_url': 'https://ckan.sansa.saeoss.org',
            'upload_user': 'mikemets',
            'upload_password': '64a84482-5af9-4854-ac51-5de996c91653',
            'upload_method': 'api/action/metadata_record_create',
        }, {
            'source_dir': './agent/tests/cbers_p5m',
            'standard': 'CBERS_P5M',
            'upload_server_url': 'https://ckan.sansa.saeoss.org',
            'upload_user': 'mikemets',
            'upload_password': '64a84482-5af9-4854-ac51-5de996c91653',
            'upload_method': 'api/action/metadata_record_create',
        },
        {
            'source_dir': './agent/tests/spot6',
            'standard': 'SPOT6',
            'upload_server_url': 'https://ckan.sansa.saeoss.org',
            'upload_user': 'mikemets',
            'upload_password': '64a84482-5af9-4854-ac51-5de996c91653',
            'upload_method': 'api/action/metadata_record_create',
        },
        {
            'source_dir': './agent/tests/landsat8',
            'standard': 'LANDSAT8',
            'upload_server_url': 'https://ckan.sansa.saeoss.org',
            'upload_user': 'mikemets',
            'upload_password': '64a84482-5af9-4854-ac51-5de996c91653',
            'upload_method': 'api/action/metadata_record_create',
        }
    ]
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

        # print('Harvest {}'.format(output['success']))
        results = output['results']
        for record in results['records']:
            if record['valid']:
                pass
                # print('{title}: Valid = {valid}, Upload = {upload_success} {upload_error}'.format(**record))
            else:
                print('{title}: Valid = {valid}, Error = {error}, Upload = {upload_success} {upload_error}'.format(**record))
                all_good = False
                continue

    if all_good:
        print('Tests completed successfully ')
    else:
        print('Tests complete - see issues above')
