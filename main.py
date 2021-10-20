import requests
import os
from datetime import datetime
from urllib.parse import urlsplit, unquote

from environs import Env


def parse_url_file_ext(url):
    path = unquote(urlsplit(url).path)
    filename = os.path.basename(path)
    return os.path.splitext(filename)[1]


def download_image(url, src_name, image_name):
    response = requests.get(url)
    response.raise_for_status()
    ext = parse_url_file_ext(url)
    os.makedirs(f'images/{src_name}', exist_ok=True)
    with open(f'images/{src_name}/{image_name}{ext}', 'wb') as file:
        return file.write(response.content)


def parse_spacex(flight_id):
    spacex_api_url = f'https://api.spacexdata.com/v4/launches/{flight_id}'
    response = requests.get(spacex_api_url)
    response.raise_for_status()
    return response.json()


def fetch_spacex_one_launch_images(flight_id):
    images_url_list = parse_spacex(flight_id)['links']['flickr']['original']
    for image_id, image_url in enumerate(images_url_list):
        src_name = 'space'
        image_name = f'{src_name}_{image_id}'
        download_image(image_url, src_name, image_name)
    return


def parse_nasa_apod(api_key, image_count):
    url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': image_count
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def fetch_nasa_apod_images(api_key, image_count=''):
    for image_id, res_obj in enumerate(parse_nasa_apod(api_key, image_count)):
        src_name = 'nasa_apod'
        image_name = f'{src_name}_{image_id}'
        if 'hdurl' in res_obj:
            url = res_obj['hdurl']
        else:
            url = res_obj['url']
        download_image(url, src_name, image_name)
    return


def parse_nasa_epic(api_key):
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': api_key,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def format_url_image_date(src_image_date):
    image_date = datetime.fromisoformat(src_image_date)
    return image_date.date().strftime('%Y/%m/%d')


def fetch_nasa_epic_images(api_key):
    for image_id, image_obj in enumerate(parse_nasa_epic(api_key)):
        src_name = 'nasa_epic'
        image_name = f'{src_name}{image_id}'
        src_image_name = image_obj['image']
        src_image_date = format_url_image_date(image_obj['date'])
        url = (
            'https://api.nasa.gov/EPIC/archive/natural/'
            f'{src_image_date}/png/{src_image_name}.png'
            f'?api_key={api_key}'
        )
        download_image(url, src_name, image_name)


def main():
    env = Env()
    env.read_env()
    flight_id = env('FLIGHT_ID')
    nasa_api_token = env('NASA_API_TOKEN')

    os.makedirs('images', exist_ok=True)
    # fetch_spacex_one_launch_images(flight_id)
    # fetch_nasa_apod_images(nasa_api_token, 30)
    fetch_nasa_epic_images(nasa_api_token)


if __name__ == '__main__':
    main()