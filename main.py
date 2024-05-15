from func import get_object_ids, fetch_data, save_data_to_json

if __name__ == '__main__':
    url = ("https://publicfs-api.reo.ru/reo-fs-public-map-api/api/v2/map/"
           "tile?bbox=30.9375,51.8051,45.0000,55.9552&z=8&filterId=2557bc47-ee06-416d-b1ee-a5e66b1ba548"
           "&callback=id_171570313840962236808")
    sorted_ids = get_object_ids(url)
    all_data = fetch_data(sorted_ids)
    save_data_to_json(all_data, "data.json")
