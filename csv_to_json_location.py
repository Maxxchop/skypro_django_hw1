import json
import csv


def csv_to_json(filename):
    # gets .csv filename and returns json
    with open(filename, encoding='utf8') as f:
        data = csv.reader(f)
        keys = []
        result = []
        model_name = 'authentication.Location'
        for row in data:
            if not keys:
                keys = row  # первая строчка -- это ключи
            else:
                dct = {}
                dct = dict(zip(keys, row))
                dct['lat'] = float(dct['lat'])
                dct['lng'] = float(dct['lng'])
                pk = int(dct.pop('id'))
                result.append({
                    "model": model_name,
                    "pk": pk,
                    "fields": dct
                })
        with open('location.json', 'w', encoding='utf8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return json.dumps(result, ensure_ascii=False)


csv_to_json('./datasets/location.csv')


