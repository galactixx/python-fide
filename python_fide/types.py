from dataclasses import dataclass
from typing import Optional

from python_fide.utils import create_url
from python_fide.constants import (   
    FIDE_CALENDER_URL,
    FIDE_NEWS_URL
)

@dataclass
class Player:
    first_name: str
    last_name: str
    player_id: str
    title: Optional[str]
    country: str

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    

@dataclass
class Event:
    name: str
    event_id: str

    @property
    def event_url(self) -> str:
        return create_url(
            base=FIDE_CALENDER_URL, segments=self.event_id
        )


@dataclass
class News:
    title: str
    news_id: str

    @property
    def news_url(self) -> str:
        return create_url(
            base=FIDE_NEWS_URL, segments=self.news_id
        )