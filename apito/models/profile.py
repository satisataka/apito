from pydantic import Field
from typing import Dict, List, Optional
from pydantic import model_validator

from .base import Model
from ..exceptions import InvalidData


class Phone(Model):
    phone: str
    verified: bool
    verificationInProgress: bool
    itemsCount: int
    locked: bool
    protection: bool


class DetailProfile(Model):
    info: 'Profile'
    phones: List[Phone]

    @model_validator(mode='before')
    def pre_root(cls, data: Dict) -> Dict:
        elements = data.pop("elements", [])

        new_data = {}
        for el in elements:
            field = el.get("type")
            body = el.get("body")

            if "list" in body:
                body = body.get("list", [])

            new_data[field] = body

        return new_data


class Profile(Model):
    id: int
    name: str
    email: str
    phone: str
    type: str
    avatar: dict
    is_pro: Optional[bool] = Field(alias='isPro', default=None)
    is_legal_person: Optional[bool] = Field(alias='isLegalPerson', default=None)

    @model_validator(mode='before')
    def pre_root(cls, data: dict) -> dict:
        if isinstance(data["type"], dict):
            data["type"] = data["type"].get("code")

        return data

    def detail(self):
        data = self._api.get(path="16/profile/info")

        if data["status"] == "ok":
            return DetailProfile(api=self._api, **data.get("result", {}))

        else:
            # TODO: raise
            raise


class Tfa(Model):
    flow: str
    phone: str = None

    def request(self) -> None:
        self._api.post(
            "1/tfa/request",
            data={
                "phone": self.phone,
            }
        )
        return

    def auth(self, code) -> Profile:
        data = self._api.post(
            "2/tfa/auth",
            data={
                "flow": self.flow,
                "code": code,
            }
        )

        if data["status"] == "incorrect-data":
            raise InvalidData(messages=data.get("result"))

        return Profile(api=self._api, **data.get("result", {}).get("user", {}))



