import json
import requests


def harvest_folder(source_dir, standard):
    output = {'success': False}

    data = {
        'kwargs': {
            'source_dir': source_dir,
            'standard': standard
        }
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

    output['success'] = True
    output['results'] = json.loads(response.text)
    return output


if __name__ == "__main__":
    source_dir = '/home/mike/projects/harvester/data/CBERS'
    standard = 'CBERS'
    output = harvest_folder(source_dir, standard)
    for record in output['results']['records']:
        print('{title}: Valid = {valid}, Upload = {upload_success} {upload_error}'.format(**record))
