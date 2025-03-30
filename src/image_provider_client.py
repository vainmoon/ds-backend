import requests
import io


class ImageLoadingError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code
        super().__init__(f'message: {self.message}, code: {self.code}')


class ImageProviderClient:
    def __init__(self, service_url: str):
        self.service_url = service_url

    def get_img(self, img_id: int) -> io.BytesIO:
        url = f'{self.service_url}/{img_id}'

        try:
            response = requests.get(url, timeout=(5, 10))
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            raise ImageLoadingError(f'Image {img_id} loading timeout: {e}',
                                    408)
        except requests.exceptions.HTTPError as e:
            raise ImageLoadingError(f'Http error: {e}',
                                    e.response.status_code)

        img = io.BytesIO(response.content)
        return img
