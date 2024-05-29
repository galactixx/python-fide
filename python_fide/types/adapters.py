from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl

class PartialDictAdapter(BaseModel):
    """
    General response structure whose value is a dictionary.
    """
    data: Dict[str, Any]


class PartialListAdapter(BaseModel):
    """
    General response structure whose value is a list of
    dictionaries.
    """
    data: List[dict]

    @classmethod
    def from_minimal_adapter(cls, response: List[dict]) -> 'PartialListAdapter':
        """
        Creates an instance of PartialListAdapter for responses
        that dont have the valid key.
        """
        adapter = cls.model_validate({'data': response})
        return adapter

    @property
    def num_observations(self) -> int:
        """The number of observations (dictionaries) in response."""
        return len(self.data)

    @property
    def extract(self) -> Dict[str, Any]:
        """Returns the first record in the list response."""
        return self.data[0]


class TopPlayersAdapter(BaseModel):
    """
    Response structure for the top ten standard players endpoint.
    """
    open: List[dict]
    girls: List[dict]
    juniors: List[dict]
    women: List[dict]


class _MetaAdapter(BaseModel):
    """Response structure for the pagination fields."""
    page_current: int = Field(..., validation_alias='current_page')
    page_last: int = Field(..., validation_alias='last_page')
    url_path: str = Field(..., validation_alias='path')
    results_per_page: int = Field(..., validation_alias='per_page')
    results_num_start: Optional[int] = Field(..., validation_alias='from')
    results_num_end: Optional[int] = Field(..., validation_alias='to')
    results_total: int = Field(..., validation_alias='total')


class _LinksAdapter(BaseModel):
    """Response structure for the pagination links."""
    first_link: HttpUrl = Field(..., validation_alias='first')
    last_link: HttpUrl = Field(..., validation_alias='last')
    prev_link: Optional[HttpUrl] = Field(..., validation_alias='prev')
    next_link: Optional[HttpUrl] = Field(..., validation_alias='next')


class HolisticAdapter(BaseModel):
    """
    Response structure for the complete response containing
    pagination information.
    """
    data: List[dict]
    links: _LinksAdapter
    meta: _MetaAdapter