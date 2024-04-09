# from python_fide.clients.search_client import FideSearchClient

# client = FideSearchClient()

# events = client.get_news(
#     query='world cadet', limit=100
# )

# print(len(events))
# print(events[0].news_url)


from python_fide.parsing.profile_parsing import profile_charts_parsing

print(
    profile_charts_parsing(
        response=[
    {
        "date_2": "2003-Apr",
        "id_number": None,
        "rating": "2300",
        "period_games": "0",
        "rapid_rtng": None,
        "rapid_games": None,
        "blitz_rtng": None,
        "blitz_games": None,
        "name": "Magnusson, Jorgen",
        "country": "SWE"
    },
    {
        "date_2": "2003-Jul",
        "id_number": None,
        "rating": "2300",
        "period_games": "0",
        "rapid_rtng": None,
        "rapid_games": None,
        "blitz_rtng": None,
        "blitz_games": None,
        "name": "Magnusson, Jorgen",
        "country": "SWE"
    }
            ]
    )
)