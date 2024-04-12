import prettyprinter as pp
from python_fide.clients.top_players import get_top_standard_players
from python_fide.constants.rating_cat import RatingCategory

pp.install_extras(include=['dataclasses'])

pp.pprint(
    get_top_standard_players(
        categories=[RatingCategory.OPEN],
        limit=1
    )
)