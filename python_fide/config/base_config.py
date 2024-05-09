from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict

class PaginationConfig(BaseModel):
    """
    Simple configuration for page number, used in pagination.
    """
    page: int


class BaseParameterConfig(ABC, BaseModel):
    """
    Base abstract parameter configuration used in any endpoint configurations
    that contain parameters to be used in the request.
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
        Updates and sets the page parameter for endpoints that require pagination.

        Args:
            page (int): The current page number.
            parameters (Dict[str, Any]): A dictionary of all parameters required for request.

        Returns:
            Dict[str, Any]: An updated dictionary of all parameters required for request.
        """
        pagination_config = PaginationConfig(page=page)
        return (
            parameters | pagination_config.model_dump()
        )


class ParameterAliasConfig(BaseParameterConfig):
    @property
    def parameterize(self) -> Dict[str, Any]:
        """Serializes pydantic model by alias."""
        return self.model_dump(by_alias=True)


class ParameterConfig(BaseParameterConfig):
    @property
    def parameterize(self) -> Dict[str, Any]:
        """Serializes pydantic model."""
        return self.model_dump()


class ParameterNullConfig(BaseParameterConfig):
    @property
    def parameterize(self) -> Dict[str, Any]:
        """Returns an empty dictionary."""
        return dict()


class BaseEndpointConfig(ABC, BaseModel):
    """
    Base abstract endpoint configuration used in any endpoint configurations
    that dont contain parameters but instead require the building of a URL.
    """
    @abstractmethod
    def endpointize(self) -> Dict[str, Any]:
        pass