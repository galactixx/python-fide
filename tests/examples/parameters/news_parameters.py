from python_fide import (
    Date,
    FideNews,
    FideNewsCategory,
    FideNewsContent,
    FideNewsDetail,
    FideNewsTopic
)

FIDE_NEWS_DETAIL_2970 = FideNewsDetail(
    news=FideNews(
        title='FIDE Candidates: Race for first wide open as second half begins',
        news_id=2970,
        posted_at=Date(
            date_iso='2024-04-14',
            date_original='2024-04-14 05:37:05',
            date_original_format='%Y-%m-%d %H:%M:%S'
        )
    ),
    topic=FideNewsTopic(topic_id=20, topic_name='Candidates'),
    category=FideNewsCategory(category_id=1, category_name='Chess news'),
    contents=[
        FideNewsContent(
            content="After the rest day, the second half of the FIDE Candidates kicked off on April 13...",
            images=list()
        )
    ],
    created_at=Date(
        date_iso='2024-04-14',
        date_original='2024-04-14 05:49:27',
        date_original_format='%Y-%m-%d %H:%M:%S'
    ),
    updated_at=Date(
        date_iso='2024-04-14',
        date_original='2024-04-14 05:49:27',
        date_original_format='%Y-%m-%d %H:%M:%S'
    )
)

FIDE_NEWS_DETAIL_2981 = FideNewsDetail(
    news=FideNews(
        title='Four in the race for first in FIDE Candidates; Tan solely on top in Women’s event',
        news_id=2981,
        posted_at=Date(
            date_iso='2024-04-19',
            date_original='2024-04-19 05:23:57',
            date_original_format='%Y-%m-%d %H:%M:%S'
        )
    ),
    topic=FideNewsTopic(topic_id=20, topic_name='Candidates'),
    category=FideNewsCategory(category_id=1, category_name='Chess news'),
    contents=[
        FideNewsContent(
            content='The FIDE Candidates Tournament is getting more and more exciting with each and every passing day...',
            images=list()
        )
    ],
    created_at=Date(
        date_iso='2024-04-19',
        date_original='2024-04-19 05:41:42',
        date_original_format='%Y-%m-%d %H:%M:%S'
    ),
    updated_at=Date(
        date_iso='2024-04-19',
        date_original='2024-04-19 05:41:42',
        date_original_format='%Y-%m-%d %H:%M:%S'
    )
)