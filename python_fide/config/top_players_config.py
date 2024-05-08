from typing import List, Optional

from pydantic import BaseModel, field_validator

from python_fide.enums import RatingCategory

class TopPlayersConfig(BaseModel):
    """
    """
    limit: int
    categories: List[RatingCategory]

    @field_validator('limit', mode='before')
    @classmethod
    def validate_limit(cls, limit: Optional[int]) -> int:
        """
        """
        return limit or 10

    @field_validator('categories', mode='before')
    @classmethod
    def extract_categories(
        cls,
        categories: Optional[List[RatingCategory]]
    ) -> List[RatingCategory]:
        """
        """
        if categories is None:
            return [category for category in RatingCategory]
        else:
            return list(set(categories))