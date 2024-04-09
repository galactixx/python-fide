from typing import Union

from pydantic import Field

from python_fide.constants.periods import Period
from python_fide.endpoint.base_endpoint import BaseConfig

class ProfileChartsConfig(BaseConfig):
    fide_id: Union[str, int] = Field(..., alias='event')
    period: Period = Field(..., alias='period')

    @property
    def parameterize(self) -> dict:
        pass


class ProfileStatsConfig(BaseConfig):
    fide_id: Union[str, int] = Field(..., alias='id1')
    opponent_fide_id: Union[str, int] = Field(..., alias='id2')

    @property
    def parameterize(self) -> dict:
        pass