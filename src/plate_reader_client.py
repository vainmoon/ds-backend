import requests


class PlateReaderClient:
    def __init__(self, host: str):
        self.host = host

    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
        )

        return res.json()

    def read_plate_number_by_id(self, img_id: int):
        res = requests.post(
            f'{self.host}/readPlateNumberById',
            json={
                'img_id': img_id,
            },
        )
        return res.json()

    def read_plate_number_by_id_list(self, img_id_list: list):
        res = requests.post(
            f'{self.host}/readPlateNumberByIdList',
            json={
                'img_id_list': img_id_list
            },
        )
        return res.json()


if __name__ == '__main__':
    client = PlateReaderClient(host='http://127.0.0.1:8080')
    print(client.read_plate_number_by_id_list([9965, 10022]))
    print(client.read_plate_number_by_id(9965))
