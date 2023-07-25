from .api import Api
from .models import Model
from .models.profile import Tfa, Profile
from .exceptions import WrongCredentials, InvalidData


class Apito:
    def __init__(self) -> None:
        self._api = Api()

    def export_cookies(self, filename=None, ignore_discard=False, ignore_expires=False):
        self._api.export_cookies(filename, ignore_discard, ignore_expires)

    def auth(self, login: str, password: str) -> Model:
        data = self._api.post(
            "11/auth",
            data={
                "login": login,
                "password": password,
            }
        )

        if data["status"] == "incorrect-data":
            raise InvalidData(data.get("result"))
        elif data["status"] == "wrong-credentials":
            raise WrongCredentials()
        elif data["status"] == "tfa-check":
            return Tfa(api=self._api, **data.get("result"))

        # status == "ok"
        return Profile(api=self._api, **data.get("result", {}).get("user", {}))

    def profile(self):
        data = self._api.get("4/profile")
        return Profile(api=self._api, **data)


