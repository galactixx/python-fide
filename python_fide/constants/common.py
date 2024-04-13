# Fide Search API Endpoint
FIDE_SEARCH_URL = 'https://app.fide.com/api/v1/client/search?'

# Fide Profile API Endpoints
FIDE_PROFILE_CHARTS_URL = 'https://ratings.fide.com/a_chart_data.phtml?'
FIDE_PROFILE_STATS_URL = 'https://ratings.fide.com/a_data_stats.php?'
FIDE_PLAYERS_URL = 'https://app.fide.com/api/v1/client/players/'
FIDE_OPPONENTS_URL = 'https://ratings.fide.com/a_data_opponents.php?'

# Fide News API Endpoints
FIDE_EVENTS_DETAIL_URL = 'https://app.fide.com/api/v1/client/events/'

# Fide News/Events URLs
FIDE_NEWS_URL = 'https://fide.com/news/'
FIDE_CALENDER_URL = 'https://fide.com/calendar/'

# Fide Headers
FIDE_HEADERS = {
    'Accept-Encoding': 'gzip, deflate'
}
FIDE_RATINGS_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9,bg;q=0.8",
    "X-Requested-With": "XMLHttpRequest"
}