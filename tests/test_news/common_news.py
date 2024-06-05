from python_fide import (
    Date,
    FideNews,
    FideNewsCategory,
    FideNewsContent,
    FideNewsDetail,
    FideNewsID,
    FideNewsTopic
)

FIDE_NEWS_DETAIL_CANDIDATES_ONE = FideNewsDetail(
    topic=FideNewsTopic(topic_id=20, topic_name='Candidates'),
    category=FideNewsCategory(category_id=1, category_name='Chess news'),
    contents=[
        FideNewsContent(
            content="After the rest day, the second half of the FIDE Candidates kicked off on April 13...",
            images=list()
        )
    ],
    created_at=Date.from_date_format(date='2024-04-14 05:49:27', date_format='%Y-%m-%d %H:%M:%S'),
    updated_at=Date.from_date_format(date='2024-04-14 05:49:27', date_format='%Y-%m-%d %H:%M:%S'),
    news=FideNews(
        title='FIDE Candidates: Race for first wide open as second half begins',
        news_id=2970,
        posted_at=Date.from_date_format(date='2024-04-14 05:37:05', date_format='%Y-%m-%d %H:%M:%S')
    )
)

FIDE_NEWS_DETAIL_CANDIDATES_TWO = FideNewsDetail(
    topic=FideNewsTopic(topic_id=20, topic_name='Candidates'),
    category=FideNewsCategory(category_id=1, category_name='Chess news'),
    contents=[
        FideNewsContent(
            content='The FIDE Candidates Tournament is getting more and more exciting with each and every passing day...',
            images=list()
        )
    ],
    created_at=Date.from_date_format(date='2024-04-19 05:41:42', date_format='%Y-%m-%d %H:%M:%S'),
    updated_at=Date.from_date_format(date='2024-04-19 05:41:42', date_format='%Y-%m-%d %H:%M:%S'),
    news=FideNews(
        title='Four in the race for first in FIDE Candidates; Tan solely on top in Women’s event',
        news_id=2981,
        posted_at=Date.from_date_format(date='2024-04-19 05:23:57', date_format='%Y-%m-%d %H:%M:%S')
    )
)

FIDE_NEWS_PARAMETERS_CANDIDATES_ONE = [
    FideNewsID(entity_id='2970'),
    FideNewsID(entity_id=2970),
    FIDE_NEWS_DETAIL_CANDIDATES_ONE.news
]

FIDE_NEWS_PARAMETERS_CANDIDATES_TWO = [
    FideNewsID(entity_id='2981'),
    FideNewsID(entity_id=2981),
    FIDE_NEWS_DETAIL_CANDIDATES_TWO.news
]