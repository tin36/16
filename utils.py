import json


def read_json(filename):
    '''Читаем JSON'''
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        return data
