# import json
import requests


def harvest_folder(xml_data, title, standard):
    output = {'success': False}

    data = {
        'xmlData': xml_data,
        'title': title,
        'standard': standard
    }
    base = 'http://localhost:8080'
    url = "{}/transform".format(base)
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
    output['results'] = response.text
    return output


if __name__ == "__main__":
    xml_data = """
<root>
    <data>
        <sceneId>1234</sceneId>
        <productId>4567</productId>
    </data>
</root>
    """
    title = 'Test1'
    standard = 'CBERS'
    output = harvest_folder(xml_data, title, standard)
    print(output)
