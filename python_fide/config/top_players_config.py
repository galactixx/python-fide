from typing import List, Optional

from pydantic import BaseModel, field_validator

from python_fide.enums import RatingCategory

class TopPlayersConfig(BaseModel):
    """
    Simple configuration for the top ten standard endpoint from the
    FideTopPlayersClient.

    Args:
        limit (int): An integer of the maximum number of events to parse
            and return, cannot be more than 10.
        categories (List[RatingCategory]): A list of RatingCategory values each
            representing a chess category (OPEN, WOMEN, JUNIORS, GIRLS).
    """
    limit: int
    categories: List[RatingCategory]

    @field_validator('limit', mode='before')
    @classmethod
    def validate_limit(cls, limit: Optional[int]) -> int:
        """Validation for limit parameter."""
        assert limit <= 10, 'limit argument cannot exceed ten'
        return limit or 10

    @field_validator('categories', mode='before')
    @classmethod
    def extract_categories(
        cls,
        categories: Optional[List[RatingCategory]]
    ) -> List[RatingCategory]:
        """
        Validation for the categories parameter.
        
        Args:
            categories (List[RatingCategory] | None): A list of RatingCategory values each
                representing a chess category (OPEN, WOMEN, JUNIORS, GIRLS). If no category is
                specified, all categories will be included.

        Returns:
            List[RatingCategory]: A list of RatingCategory values each representing a
                chess category (OPEN, WOMEN, JUNIORS, GIRLS).
        """
        if categories is None:
            return [category for category in RatingCategory]
        else:
            return list(set(categories))