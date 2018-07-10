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


XML_DATA = """
<root>
<data>
    <productId>19603</productId>
    <sceneId>18803</sceneId>
    <satelliteId>CB04</satelliteId>
    <sensorId>MUX</sensorId>
    <recStationId>SAC</recStationId>
    <productDate>2015-10-23 09:18:04</productDate>
    <productLevel>LEVEL2</productLevel>
    <pixelSpacing>20.000</pixelSpacing>
    <productType>Standard</productType>
    <sceneCount>1</sceneCount>
    <sceneShift>0</sceneShift>
    <overallQuality>9</overallQuality>
    <satPath>58</satPath>
    <satRow>115</satRow>
    <satPathbias></satPathbias>
    <satRowbias></satRowbias>
    <scenePath>58</scenePath>
    <sceneRow>115</sceneRow>
    <scenePathbias></scenePathbias>
    <sceneRowbias></sceneRowbias>
    <direction>D</direction>
    <sunElevation>66.954</sunElevation>
    <sunAzimuthElevation>267.523</sunAzimuthElevation>
    <sceneDate>2015-10-23 07:14:07.66</sceneDate>
    <sceneTime>372669247.667328</sceneTime>
    <instrumentMode>IMGMODE</instrumentMode>
    <imagingStartTime>2015-10-23 07:13:58.75</imagingStartTime>
    <imagingStopTime>2015-10-23 07:14:16.58</imagingStopTime>
    <gain>1.590000,1.590000,1.590000,1.590000</gain>
    <satOffNadir>0.000</satOffNadir>
    <mirrorOffNadir>0.000</mirrorOffNadir>
    <bands>1,2,3,4</bands>
    <absCalibType>(gain2,Labdata,L=DN*g,W*m^(-2)*sr^(-1)*um^(-1))B1: 0.626647, B2:0.653898, B3: 0.647728, B4: 0.498509</absCalibType>
    <mtfcProMode>None</mtfcProMode>
    <radioMatricMethod>StatData</radioMatricMethod>
    <addWindow>Bartlett</addWindow>
    <correctPhase>MertZ</correctPhase>
    <reconstructProcess>FFT</reconstructProcess>
    <earthModel>WGS_84</earthModel>
    <mapProjection>UTM</mapProjection>
    <resampleTechnique>BL</resampleTechnique>
    <productOrientation>MAP</productOrientation>
    <ephemerisData>GPS</ephemerisData>
    <attitudeData>AOCS</attitudeData>
    <sceneCenterLat>-13.678494</sceneCenterLat>
    <sceneCenterLong>47.874427</sceneCenterLong>
    <zone>38S</zone>
    <dataUpperLeftLat>-13.079004</dataUpperLeftLat>
    <dataUpperLeftLong>47.438452</dataUpperLeftLong>
    <dataUpperRightLat>-13.249301</dataUpperRightLat>
    <dataUpperRightLong>48.544165</dataUpperRightLong>
    <dataLowerLeftLat>-14.106054</dataLowerLeftLat>
    <dataLowerLeftLong>47.201428</dataLowerLeftLong>
    <dataLowerRightLat>-14.277147</dataLowerRightLat>
    <dataLowerRightLong>48.312252</dataLowerRightLong>
    <productUpperLeftLat>-13.081215</productUpperLeftLat>
    <productUpperLeftLong>47.191982</productUpperLeftLong>
    <productUpperRightLat>-13.066228</productUpperRightLat>
    <productUpperRightLong>48.541532</productUpperRightLong>
    <productLowerLeftLat>-14.290001</productLowerLeftLat>
    <productLowerLeftLong>47.203206</productLowerLeftLong>
    <productLowerRightLat>-14.273575</productLowerRightLat>
    <productLowerRightLong>48.559638</productLowerRightLong>
    <dataUpperLeftX>764417.300955</dataUpperLeftX>
    <dataUpperLeftY>8552853.647206</dataUpperLeftY>
    <dataUpperRightX>884167.620662</dataUpperRightX>
    <dataUpperRightY>8532569.028593</dataUpperRightY>
    <dataLowerLeftX>737676.378744</dataLowerLeftX>
    <dataLowerLeftY>8439431.376552</dataLowerLeftY>
    <dataLowerRightX>857435.925756</dataLowerRightX>
    <dataLowerRightY>8419072.275198</dataLowerRightY>
    <productUpperLeftX>737676.378744</productUpperLeftX>
    <productUpperLeftY>8552853.647206</productUpperLeftY>
    <productUpperRightX>884167.620662</productUpperRightX>
    <productUpperRightY>8552853.647206</productUpperRightY>
    <productLowerLeftX>737676.378744</productLowerLeftX>
    <productLowerLeftY>8419072.275198</productLowerLeftY>
    <productLowerRightX>884167.620662</productLowerRightX>
    <productLowerRightY>8419072.275198</productLowerRightY>
    <isSimulateData>N</isSimulateData>
    <dataFormatDes>GEOTIFF</dataFormatDes>
    <delStatus>0</delStatus>
    <dataTempDir>/DPS/ProData/MUX/LEVEL2/19603/</dataTempDir>
    <dataArchiveDir></dataArchiveDir>
    <browseArchiveDir></browseArchiveDir>
    <browseDirectory></browseDirectory>
    <browseFileLocation></browseFileLocation>
</data>
</root>
"""

if __name__ == "__main__":
    input_data = XML_DATA
    title = 'Test1'
    standard = 'CBERS_MUX'
    output = transform_record(input_data, title, standard)
    results = output['results']
    if not results.get('valid'):
        print('Success: False, Error: {}'.format(results['error']))
    else:
        print('Success: {}, Valid: {}'.format(
            output['success'], results['valid']))
        print('DataCite Record: {}'.format(results['datacite_data']))
