import json
import requests


def transform_record(input_data, title, standard):
    output = {'success': False}

    data = {
        'input_data': input_data,
        'title': title,
        'standard': standard
    }
    base = 'http://localhost:8080'
    url = "{}/transform".format(base)
    # print(url)
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
    sources = [
        {
            'source_file': './agent/tests/cbers_mux/CBERS_MUX_sample.xml',
            'standard': 'CBERS_MUX',
        }, {
            'source_file': './agent/tests/cbers_p5m/cbers_p5m_sample.xml',
            'standard': 'cbers_p5m',
        }, {
            'source_file': './agent/tests/cbers_p10/cbers_p10_sample.xml',
            'standard': 'cbers_p10',
        }, {
            'source_file': './agent/tests/spot6/SPOT6_sample.xml',
            'standard': 'SPOT6',
        }, {
            'source_file': './agent/tests/landsat8/landsat8_sample.txt',
            'standard': 'LANDSAT8',
        }
    ]
    all_good = True
    for source in sources:
        title = 'Test1'
        standard = source['standard']
        with open(source['source_file']) as afile:
            input_data = afile.read()

        output = transform_record(input_data, title, standard)
        results = output['results']
        if not results.get('valid'):
            all_good = False
            print('Success: False, Error: {}'.format(results['error']))
        # else:
        #     print('Success: {}, Valid: {}'.format(
        #         output['success'], results['valid']))
        #     print('DataCite Record: {}'.format(results['datacite_data']))
    if all_good:
        print('Tests completed successfully ')
    else:
        print('Tests complete - see issues above')
