from typing import List

from pydantic import BaseModel, field_validator

from python_fide.constants.rating_cat import RatingCategory

class TopPlayersConfig(BaseModel):
    """
    """
    categories: List[RatingCategory]

    @field_validator('categories', mode='after')
    @classmethod
    def extract_categories(
        cls,
        categories: List[RatingCategory]
    ) -> List[RatingCategory]:
        return list(set(categories))