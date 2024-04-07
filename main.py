from python_fide.clients.search_client import FideSearchClient

client = FideSearchClient()

events = client.get_news(
    query='world cadet', limit=100
)

print(len(events))
print(events[0].news_url)