import prettyprinter as pp
from python_fide.clients.news import FideNews
from python_fide.types import FideNewsID

pp.install_extras(include=['dataclasses'])

news_client = FideNews()

pp.pprint(
    news_client.get_news_detail(
        fide_news=FideNewsID(entity_id='2963')
    )
)