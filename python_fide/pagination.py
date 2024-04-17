from typing import List, Optional, TypeVar

from python_fide.utils.general import validate_limit

T = TypeVar('T')

class FidePagination:
    """
    """
    def __init__(self, limit: int):
        self._limit = validate_limit(limit=limit)

        # Page tracking variables
        self._current_page = 1
        self._overflow_pages = None

        # Record tracking variables
        self._records_parsed = 0
        self._gathered_records: List[T] = []

    @property
    def loop_continue(self) -> bool:
        return self._records_parsed < self._limit and (
            self._overflow_pages is None or self._current_page <= self._overflow_pages
        )
    
    @property
    def overflow_pages(self) -> Optional[int]:
        return self._overflow_pages
    
    @overflow_pages.setter
    def overflow_pages(self, pages: int) -> None:
        self._overflow_pages = pages

    @property
    def current_page(self) -> int:
        return self._current_page

    @property
    def records(self) -> List[T]:
        return self._gathered_records[:self._limit]

    def update_status(self, record: T) -> None:
        self._gathered_records.append(record)
        self._records_parsed += 1

        # Update current page
        self._current_page += 1