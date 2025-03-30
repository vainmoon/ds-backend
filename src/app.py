import logging
from flask import Flask, request
from models.plate_reader import PlateReader, InvalidImage
from image_provider_client import ImageProviderClient, ImageLoadingError
import io

app = Flask(__name__)
plate_reader = PlateReader.load_from_file(
    './model_weights/plate_reader_model.pth')
image_provider_client = ImageProviderClient('http://89.169.157.72:8080/images')


@app.route('/readPlateNumberById', methods=['POST'])
def read_plate_number_by_id():
    if not request.is_json:
        return {'error': 'request must be json', 'code': 400}
    if 'img_id' not in request.json:
        return {'error': 'field "img_id" not found', 'code': 400}

    img_id = request.json['img_id']

    if not isinstance(img_id, int) or img_id <= 0:
        return {'error': 'img_id must be positive integer', 'code': 400}

    try:
        img = image_provider_client.get_img(img_id)
    except ImageLoadingError as e:
        logging.error(e.message)
        return {'error': e.message, 'code': e.code}

    try:
        res = plate_reader.read_text(img)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image', 'code': 400}

    return {'plate_number': res, 'code': 200}


@app.route('/readPlateNumberByIdList', methods=['POST'])
def read_plate_number_by_id_list():
    if not request.is_json:
        return {'error': 'request must be json', 'code': 400}
    if 'img_id_list' not in request.json:
        return {'error': 'field "img_id_list" not found', 'code': 400}

    img_id_list = request.json['img_id_list']
    if not isinstance(img_id_list, list) or not img_id_list:
        return {'error': 'img_id_list must be non-empty list', 'code': 400}

    res_list = []
    for img_id in img_id_list:
        try:
            if not isinstance(img_id, int) or img_id <= 0:
                return {'error': 'img_id must be positive integer',
                        'code': 400}

            img = image_provider_client.get_img(img_id)

        except ImageLoadingError as e:
            logging.error(e.message)
            return {'error': e.message, 'code': e.code}

        try:
            res = plate_reader.read_text(img)
        except InvalidImage:
            logging.error('invalid image')
            return {'error': 'invalid image', 'code': 400}

        res_list.append(res)
    return {'plate_number_list': res_list, 'code': 200}


@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    img = request.get_data()
    img = io.BytesIO(img)

    try:
        res = plate_reader.read_text(img)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image', 'code': 400}

    return {'plate_number': res, 'code': 200}


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
