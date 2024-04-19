from typing import List, Optional

from pydantic import BaseModel, field_validator

from python_fide.enums import RatingCategory

class TopPlayersConfig(BaseModel):
    """
    """
    categories: Optional[List[RatingCategory]]

    @field_validator('categories', mode='after')
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