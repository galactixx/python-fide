from typing import Optional

from python_fide.utils.general import validate_limit

class SearchPagination:
    """
    """
    def __init__(self, limit: Optional[int]):
        self._limit = validate_limit(limit=limit)

        # Page tracking variables
        self._current_page = 1
        self._overflow_pages = None

        # Record tracking variables
        self._records_parsed = 0
        self._gathered_records: list = []

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
    def records(self) -> list:
        return self._gathered_records[:self._limit]

    def update_status(self, records: list) -> None:
        self._gathered_records.extend(records)
        self._records_parsed += len(records)

        # Update current page
        self._current_page += 1
