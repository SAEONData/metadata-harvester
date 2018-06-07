# import json
import requests
from agent import config


def clear_metadata():
    output = {'success': False}

    data = {
        # 'jsonData': json.dumps(record),
        # 'metadataType': 'DataCite'
    }
    base = 'http://ckan.dirisa.org:9090'
    url = "{}/jsonContent".format(base)
    print(url)
    if config.upload_user:
        response = requests.post(
            url=url,
            data=data,
            auth=requests.auth.HTTPBasicAuth(
                config.upload_user, config.upload_password),
        )
    else:
        response = requests.get(
            url=url,
        )
    if response.status_code != 200:
        output['error'] = 'Request failed with return code: %s' % (
            response.status_code)
        return output

    output['success'] = True
    output['results'] = response.text
    return output


if __name__ == "__main__":
    output = clear_metadata()
    print(output)
