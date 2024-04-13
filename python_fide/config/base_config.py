from abc import ABC, abstractmethod

from pydantic import BaseModel

class BaseConfig(ABC, BaseModel):
    """
    """
    @property
    @abstractmethod
    def parameterize(self) -> dict:
        pass

    class Config:
        populate_by_name = True
        use_enum_values = True