import json
import requests


def harvest_folder(source_dir, standard):
    output = {'success': False}

    data = {
        'source_dir': source_dir,
        'standard': standard
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
    # source_dir = '/home/mike/projects/harvester/data/CBERS'
    # standard = 'CBERS'
    source_dir = '/home/mike/projects/harvester/data/SPOT6'
    standard = 'SPOT6'
    output = harvest_folder(source_dir, standard)
    print(source_dir)
    for record in output['results']['records']:
        if record['valid']:
            print('{title}: Valid = {valid}, Upload = {upload_success} {upload_error}'.format(**record))
        else:
            print('{title}: Valid = {valid}, Error = {error}, Upload = {upload_success} {upload_error}'.format(**record))
