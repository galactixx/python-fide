from typing import Any, Dict

from pydantic import BaseModel, ConfigDict


class BaseEndpointConfig(BaseModel):
    """
    Base abstract parameter configuration used in any endpoint
    configurations that contain parameters to be used in the
    request.
    """

    model_config = ConfigDict(
        populate_by_name=True, use_enum_values=True, extra="forbid"
    )

    @property
    def parameterize(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True)
