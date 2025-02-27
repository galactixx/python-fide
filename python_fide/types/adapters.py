from typing import Any, Dict, List

from pydantic import BaseModel


class PartialListAdapter(BaseModel):
    """
    General response structure whose value is a list of
    dictionaries.
    """

    data: List[dict]

    @classmethod
    def from_minimal_adapter(cls, response: List[dict]) -> "PartialListAdapter":
        """
        Creates an instance of PartialListAdapter for responses
        that dont have the valid key.
        """
        adapter = cls.model_validate({"data": response})
        return adapter

    @property
    def num_observations(self) -> int:
        """The number of observations (dictionaries) in response."""
        return len(self.data)

    @property
    def extract(self) -> Dict[str, Any]:
        """Returns the first record in the list response."""
        return self.data[0]
