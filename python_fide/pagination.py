from typing import List, Optional, TypeVar

T = TypeVar('T')

class FidePagination:
    """
    Pagination class with helper methods. Generally used for pagination
    when parsing from the event and news endpoints.

    Args:
        limit (int): The maximum number of records to pull from endpoint.
    """
    def __init__(self, limit: int):
        self._limit = limit

        # Page tracking variables
        self._current_page = 1
        self._overflow_pages = None

        # Record tracking variables
        self._records_parsed = 0
        self._gathered_records: List[T] = []

    @property
    def loop_continue(self) -> bool:
        """The loop control for the pagination."""
        return self._records_parsed < self._limit and (
            self._overflow_pages is None or self._current_page <= self._overflow_pages
        )
    
    @property
    def overflow_pages(self) -> Optional[int]:
        """The total number of pages with results."""
        return self._overflow_pages
    
    @overflow_pages.setter
    def overflow_pages(self, pages: int) -> None:
        self._overflow_pages = pages

    @property
    def current_page(self) -> int:
        """The current page."""
        return self._current_page

    @property
    def records(self) -> List[T]:
        """A list of records that have been parsed."""
        return self._gathered_records[:self._limit]

    def update_status(self, record: T) -> None:
        """Update the status by appending a new recod along with adjusting the current page."""
        self._gathered_records.append(record)
        self._records_parsed += 1

        # Update current page
        self._current_page += 1