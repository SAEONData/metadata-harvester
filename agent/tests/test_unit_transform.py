import unittest
from agent.transformer import transform


class TransformerTest(unittest.TestCase):

    def test_01_transform_no_record(self):
        output = transform(kwargs={})
        self.assertEqual(output.get('success'), False)
        self.assertEqual(
            output['error']['message'],
            'record title is required')

    def test_02_transform_no_xml_data(self):
        settings = {
            'title': 'TestRecord1'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), False)
        self.assertEqual(
            output['error']['message'],
            'xml data is required')

    def test_03_transform_no_standard(self):
        settings = {
            'title': 'TestRecord1',
            'xml_data': 'Hello'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), False)
        self.assertEqual(
            output['error']['message'],
            'metadata standard is required')

    def test_04_transform_invalid_xml(self):
        settings = {
            'title': 'TestRecord1',
            'xml_data': """
<root>
    <data>
        <productId>19603</productId>
</root>
""",
            'standard': 'Hello'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), False)
        self.assertIn(
            'Invalid Xml in document',
            output['error']['message'])

    def test_05_transform_unknown_standard(self):
        settings = {
            'title': 'TestRecord1',
            'xml_data': '<root> <data> <productId>19603</productId> </data> </root>',
            'standard': 'Hello'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), False)
        self.assertEqual(
            output['error']['message'],
            'Cannot transform standard Hello yet')

    def test_06_transform_missing_fields(self):
        settings = {
            'title': 'TestRecord1',
            'xml_data': """
<root>
    <data>
        <dummy>19603</dummy>
    </data>
</root>
""",
            'standard': 'CBERS_MUX'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), False)
        self.assertIn(
            'Missing required element',
            output['error']['message'])

    def test_07_transform_valid(self):
        settings = {
            'title': 'TestRecord1',
            'xml_data': """
<root>
    <data>
        <productId>19603</productId>
        <productType>Standard</productType>
        <productLevel>LEVEL2</productLevel>
        <productDate>2015-10-23 09:18:04</productDate>
        <sceneId>18803</sceneId>
        <satelliteId>CB04</satelliteId>
        <sensorId>MUX</sensorId>
        <imagingStartTime>2015-10-23 07:13:58.75</imagingStartTime>
        <imagingStopTime>2015-10-23 07:14:16.58</imagingStopTime>
        <dataFormatDes>GEOTIFF</dataFormatDes>
        <earthModel>WGS_84</earthModel>
        <mapProjection>UTM</mapProjection>
        <dataLowerLeftLat>-14.106054</dataLowerLeftLat>
        <dataLowerLeftLong>47.201428</dataLowerLeftLong>
        <dataUpperRightLat>-13.249301</dataUpperRightLat>
        <dataUpperRightLong>48.544165</dataUpperRightLong>
    </data>
</root>
""",
            'standard': 'CBERS_MUX'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), True)
        self.assertEqual(output.get('valid'), True)
        self.assertIn(
            {'subject': 'MUX Sensor Type'},
            output['datacite_data']['subjects'])

    def test_08_transform_spot_6(self):
        with open('./agent/tests/SPOT6_sample.xml') as afile:
            xml_data = afile.read()

        settings = {
            'title': 'TestRecord1',
            'xml_data': xml_data,
            'standard': 'SPOT6'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), True)
        self.assertEqual(output.get('valid'), True)
        self.assertIn(
            {'subject': 'SPOT 6'},
            output['datacite_data']['subjects'])

    def test_09_transform_cbers_mux(self):
        with open('./agent/tests/CBERS_MUX_sample.xml') as afile:
            xml_data = afile.read()

        settings = {
            'title': 'TestRecord1',
            'xml_data': xml_data,
            'standard': 'CBERS_MUX'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), True)
        self.assertEqual(output.get('valid'), True)
        self.assertIn(
            {'subject': 'MUX Sensor Type'},
            output['datacite_data']['subjects'])

    def test_10_transform_cbers_p5m(self):
        with open('./agent/tests/CBERS_P5M_sample.xml') as afile:
            xml_data = afile.read()

        settings = {
            'title': 'TestRecord1',
            'xml_data': xml_data,
            'standard': 'CBERS_P5M'
        }
        output = transform(kwargs=settings)
        self.assertEqual(output.get('success'), True)
        self.assertEqual(output.get('valid'), True)
        self.assertIn(
            {'subject': 'P5M Sensor Type'},
            output['datacite_data']['subjects'])


if __name__ == '__main__':
    unittest.main()
