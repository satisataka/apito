from typing import TypeVar, Generic, List, Optional, Union

from ..api import Api

T = TypeVar('T')


class BaseResource(Generic[T]):
    def __init__(self, version, path: str, api: Api, **kwargs):
        self._version = version
        self._path: str = path
        self._api: Optional[Api] = api
        self._data: Union[None, T, List[T]] = None
        self._kwargs: dict = kwargs
