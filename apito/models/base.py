from abc import ABC
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..api import Api


class Model(BaseModel, ABC):
    model_config = ConfigDict(extra='allow')

    _api: Optional[Api]

    def __init__(self, api=None, **data):
        super().__init__(**data)

        self._api = api
