from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl

class _MetaAdapter(BaseModel):
    page_current: int = Field(..., validation_alias='current_page')
    page_last: int = Field(..., validation_alias='last_page')
    url_path: str = Field(..., validation_alias='path')
    results_per_page: int = Field(..., validation_alias='per_page')
    results_num_start: Optional[int] = Field(..., validation_alias='from')
    results_num_end: Optional[int] = Field(..., validation_alias='to')
    results_total: int = Field(..., validation_alias='total')


class _LinksAdapter(BaseModel):
    first_link: HttpUrl = Field(..., validation_alias='first')
    last_link: HttpUrl = Field(..., validation_alias='last')
    prev_link: Optional[HttpUrl] = Field(..., validation_alias='prev')
    next_link: Optional[HttpUrl] = Field(..., validation_alias='next')


class HolisticAdapter(BaseModel):
    data: List[dict]
    links: _LinksAdapter
    meta: _MetaAdapter


class PartialDictAdapter(BaseModel):
    data: Dict[str, Any]


class PartialListAdapter(BaseModel):
    data: List[dict]

    @classmethod
    def from_minimal_adapter(cls, response: List[dict]) -> 'PartialListAdapter':
        adapter = cls.model_validate({'data': response})
        return adapter

    @property
    def num_observations(self) -> int:
        return len(self.data)

    @property
    def extract(self) -> Dict[str, Any]:
        return self.data[0]


class TopPlayersAdapter(BaseModel):
    open: List[dict]
    girls: List[dict]
    juniors: List[dict]
    women: List[dict]