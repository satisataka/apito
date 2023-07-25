import requests
import logging

from http.cookiejar import MozillaCookieJar

logger = logging.getLogger(__name__)

BASE_URL = "https://m.avito.ru/api"
KEY = "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"
USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"


class Api:
    def __init__(self, cookies_file="cookies.txt"):
        self._base_url = BASE_URL
        self._key = KEY
        self._session = requests.Session()

        self._session.headers.update({"User-Agent": USER_AGENT})

        cookies = MozillaCookieJar(filename=cookies_file)
        try:
            cookies.load()
        except FileNotFoundError:
            pass

        self._session.cookies = cookies

        if len(cookies) == 0:
            # "set default cookies"
            self._session.get("https://m.avito.ru/profile")

    def set_cookies(self, cookies: MozillaCookieJar):
        self._session.cookies = cookies

    def export_cookies(self, filename=None, ignore_discard=False, ignore_expires=False):
        cookies: MozillaCookieJar = self._session.cookies
        cookies.save(filename, ignore_discard, ignore_expires)

    def _url(self, path: str):
        return "%s/%s" % (self._base_url.rstrip('/'), path.lstrip('/'))

    def request(self, method: str, url: str, **kwargs):
        response = self._session.request(method, url, **kwargs)

        try:
            response.raise_for_status()
        except (Exception, ):
            logger.error(f"method: {method}, url: {url}, kwargs: {kwargs}, response data: {response.text}")
            raise

        # self.export_cookies()
        return response.json()

    def get(self, path: str, params: dict = None) -> dict:
        if params is None:
            params = {}

        params.update({"key": self._key})

        return self.request('GET', self._url(path), params=params)

    def post(self, path, data: dict = None, json: dict = None):
        if data is not None:
            data.update(key=self._key)
        elif json is not None:
            json.update(key=self._key)
        else:
            data = {"key": self._key}

        return self.request('POST', self._url(path), data=data, json=json)
