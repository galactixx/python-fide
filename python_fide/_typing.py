import sys
from typing import Union

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from python_fide.types._core import FidePlayer, FidePlayerID

FidePlayerLike: TypeAlias = Union[FidePlayer, FidePlayerID]
