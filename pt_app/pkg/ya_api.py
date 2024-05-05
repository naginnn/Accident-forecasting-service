import os
import requests

def get_weather():
    acs_key = os.environ.get('YA_WEATHER_KEY')
    hdr = {
        'X-Yandex-Weather-Key': acs_key
    }
    r = requests.get('https://api.weather.yandex.ru/v2/forecast?lat=55.635416&lon=37.541000',
                     headers=hdr)
    print(r.json())


def get_one_coordinate(adr: str):
    pos = None
    try:
        acs_key = os.environ.get('YA_MAPS_KEY')
        r = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={acs_key}&&results=1&geocode={adr}&format=json')
        r = r.json()
        pos = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        pos = f"{pos.split(' ')[1]} {pos.split(' ')[0]}"
    finally:
        return pos


def get_coordinates(adr: str):
    res = {}
    adr = f"Москва, {adr}"
    try:
        acs_key = os.environ.get('YA_MAPS_KEY')
        r = requests.get(f'https://geocode-maps.yandex.ru/1.x/?apikey={acs_key}&&results=1&geocode={adr}&format=json')
        r = r.json()
        pos = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        res['pos'] = f"{pos.split(' ')[1]} {pos.split(' ')[0]}"
        r = requests.get(
            f'https://geocode-maps.yandex.ru/1.x/?kind=district&apikey={acs_key}&&results=1&geocode={pos}&format=json')
        r = r.json()
        full_address = r['response']['GeoObjectCollection']['featureMember'][0] \
            ['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']

        for idx, adr in enumerate(full_address.split(',')):
            adr = adr.strip()
            match idx:
                case 0:
                    res['country'] = adr
                case 1:
                    res['city'] = adr
                case 2:
                    res['district'] = adr
                case 3:
                    res['area'] = adr
                # case 4:
                #     res['area'] += ", " + adr
    finally:
        return res
