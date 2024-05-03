from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict

class PaginationConfig(BaseModel):
    """
    """
    page: int


class BaseParameterConfig(ABC, BaseModel):
    """
    """
    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    @property
    @abstractmethod
    def parameterize(self) -> Dict[str, Any]:
        pass

    def add_pagination_to_params(
        self,
        page: int,
        parameters: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """
        """
        pagination_config = PaginationConfig(page=page)
        return (
            parameters | pagination_config.model_dump()
        )


class ParameterAliasConfig(BaseParameterConfig):
    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)


class ParameterConfig(BaseParameterConfig):
    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump()


class ParameterNullConfig(BaseParameterConfig):
    @property
    def parameterize(self) -> Dict[str, Any]:
        return dict()


class BaseEndpointConfig(ABC, BaseModel):
    """
    """
    @abstractmethod
    def endpointize(self) -> Dict[str, Any]:
        pass