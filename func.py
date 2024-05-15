import requests
import json
import re


def get_object_ids(url):
    """Получает список идентификаторов объектов из заданного URL."""
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text
        json_data = re.search(r'\{.*}', data).group()
        parsed_data = json.loads(json_data)
        object_id = []

        for feature in parsed_data['features']:
            if feature['type'] == 'Cluster':
                for i in feature["properties"]['ids']:
                    object_id.append(i)
            elif feature['type'] == 'Feature':
                object_id.append(feature['properties']['id'])
        return object_id

    else:
        print("Error:", response.status_code)
        return []


def fetch_data(object_ids):
    """Получает данные для каждого идентификатора объекта из списка.
    Если первый запрос не удался, она делает повторный запрос на другой слой."""
    all_data = []  # Список для хранения всех данных

    for ids in object_ids:
        layer = 1
        scrap_url = (
            f'https://publicfs-api.reo.ru/reo-fs-public-map-api/api/v2/sidebar/'
            f'object?id={ids}&layer={layer}'
            )
        response2 = requests.get(scrap_url)

        if response2.status_code == 200:
            data_2 = response2.json()

        else:
            layer = 0
            scrap_url = (
                f"https://publicfs-api.reo.ru/reo-fs-public-map-api/api/v2/sidebar/"
                f"object?id={ids}&layer={layer}"
            )
            response2 = requests.get(scrap_url)
            data_2 = response2.json()

        all_data.append(data_2)

    return all_data


def save_data_to_json(data, filename):
    """Сохраняет данные в формате JSON"""
    with open(filename, "w", encoding='UTF-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
