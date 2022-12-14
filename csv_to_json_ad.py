import json
import csv


def csv_to_json(filename):
    # gets .csv filename and returns json
    with open(filename, encoding='utf8') as f:
        data = csv.reader(f)
        keys = []
        result = []
        model_name = 'ads.Ad'
        for row in data:
            if not keys:
                keys = row  # первая строчка -- это ключи
            else:
                dct = {}
                dct = dict(zip(keys, row))
                dct['author_id'] = int(dct['author_id'])
                dct['price'] = int(dct['price'])
                dct['category_id'] = int(dct['category_id'])
                dct['is_published'] = dct['is_published'] == 'TRUE'
                pk = int(dct.pop('Id'))
                result.append({
                    "model": model_name,
                    "pk": pk,
                    "fields": dct
                })
        with open('ad.json', 'w', encoding='utf8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        return json.dumps(result, ensure_ascii=False)


csv_to_json('./datasets/ad.csv')


