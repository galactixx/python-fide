from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional, 
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field, 
    field_validator,
    model_validator
)

from python_fide.exceptions import InvalidFideIDError
from python_fide.enums import RatingCategory
from python_fide.utils.pydantic import from_player_model
from python_fide.utils.general import build_url
from python_fide.types.annotated import (
    DateISO,
    DateTime,
    DateYear,
    DateYearMonth
)
from python_fide.types.base import (
    BaseRecordPaginationModel,
    FideEventDetailRaw,
    FideNewsCategory,
    FideNewsContent,
    FideNewsDetailRaw,
    FideNewsTopic,
    FidePlayerBasicRaw,
    FidePlayerDetailRaw,
    FidePlayerGameBlackStatsRaw,
    FidePlayerGameWhiteStatsRaw,
    FidePlayerRaw,
    FidePlayerRatingRaw,
    FideTopPlayerRaw
)

class ClientNotFound(BaseModel):
    """Model for an error JSON response."""
    message: Literal['Not Found']
    status: Literal[404]


class FidePlayerName(BaseModel):
    """
    Represents the name of a chess player with a Fide rating. While
    both arguments are required, the matching by the Fide API is done
    by last name and then first name. Thus, it is highly advised to not
    include a last name as a blank string.

    Args:
        first_name (str): The string first name of a player.
        last_name (str): The string last name of a player.
    """
    first_name: str
    last_name: str

    @model_validator(mode='after')
    def validate_names(self) -> 'FidePlayerName':
        """Validate the first and last name."""
        assert self.first_name.isalpha()
        assert self.last_name.isalpha()

        return self


class FideBaseID(BaseModel):
    """
    Base model for all Fide ID models (FidePlayerID, FideNewsID,
    FideEventID).

    Args:
        entity_id (int): An integer representing a Fide ID.
    """
    entity_id: int

    @field_validator('entity_id', mode='before')
    @classmethod
    def cast_to_int(cls, entity_id: Union[str, int]) -> int:
        """Validate and cast entity_id to an integer type."""
        if isinstance(entity_id, str):
            if not entity_id.isdigit():
                raise InvalidFideIDError(
                    "invalid Fide ID entered, must be an integer (as str in int type)"
                )
            
            if entity_id.startswith('0'):
                raise InvalidFideIDError("invalid Fide ID entered, cannot start with a zero")

            try:
                entity_id_cast = int(entity_id)
            except ValueError:
                raise InvalidFideIDError(
                    "invalid Fide ID entered, must be an equivalent integer"
                )
            else:
                return entity_id_cast
        else:
            return entity_id
    

class FidePlayerID(FideBaseID):
    """Model for a player Fide ID."""
    pass


class FideNewsID(FideBaseID):
    """Model for a news Fide ID."""
    pass


class FideEventID(FideBaseID):
    """Model for an event Fide ID."""
    pass


class FidePlayerBasic(BaseModel):
    """
    A slightly less detailed model than the FidePlayer model. Thus,
    it is referred to as a "basic" version of FidePlayer.

    Args:
        player_id (int): An integer representing the Fide ID of the player.
        name (str): The string full name.
        first_name (str): The string first name.
        last_name (str | None): The string last name . Can also be None if
            the last name could not reliably be detected.
        country (str): The country that the player represents.
    """
    player_id: int
    name: str
    first_name: str
    last_name: Optional[str]
    country: str

    @classmethod
    def from_validated_model(cls, player: Dict[str, Any]) -> 'FidePlayerBasic':
        """
        Creates an instance of FidePlayerBasic based on a dictionary
        pulled from the API response.

        Args:
            player (Dict[str, Any]): A dictionary representing a player.

        Returns:
            FidePlayerBasic: A new FidePlayerBasic instance.
        """
        first_name, last_name, model = from_player_model(
            player=player, fide_player_model=FidePlayerBasicRaw,
        )
        return cls(
            first_name=first_name, last_name=last_name, **model
        )


class FidePlayer(BaseModel):
    """
    A model containing information for a specific player who has 
    registered with Fide.
    
    Args:
        player_id (int): An integer representing the Fide ID of
            the player.
        name (str): The string full name.
        first_name (str): The string first name.
        last_name (str | None): The string last name. Can also be None if
            the last name could not reliably be detected.
        title (str | None): The chess Fide title (GM, IM, ...). Can be
            None if the player has no title.
        country (str): The country that the player represents.
    """
    player_id: int
    name: str
    first_name: str
    last_name: Optional[str]
    title: Optional[str]
    country: str

    @classmethod
    def from_validated_model(cls, player: Dict[str, Any]) -> 'FidePlayer':
        """
        Creates an instance of FidePlayer based on a dictionary pulled
        from the API response.

        Args:
            player (Dict[str, Any]): A dictionary representing a player.

        Returns:
            FidePlayer: A new FidePlayer instance.
        """
        first_name, last_name, model = from_player_model(
            player=player, fide_player_model=FidePlayerRaw,
        )
        return cls(
            first_name=first_name, last_name=last_name, **model
        )


class FideTopPlayer(BaseModel):
    """
    A more detailed model than the FidePlayer model, and containing
    fields that are only included in the top player response. Thus,
    it is separate from the FidePlayer model. In addition, the 'title'
    field is not included in the raw response, so the core player
    attributes are represented as a FidePlayerBasic object rather than
    a FidePlayer object.

    Args:
        player (FidePlayerBasic): A FidePlayerBasic object with all
            general player fields.
        category (RatingCategory): The category that the player belongs
            to (OPEN, WOMEN, JUNIORS, GIRLS).
        ranking (int): The ranking of the player.
        period (DateISO): The period of reporting.
        birthday (DateISO): The birthday of the player.
        sex (Literal['M', 'F']): The sex of the player.
        rating_standard (int | None): The current standard rating.
        rating_rapid (int | None): The current rapid rating.
        rating_blitz (int | None): The current blitz rating.
    """
    model_config = ConfigDict(use_enum_values=True)

    player: FidePlayerBasic
    category: RatingCategory
    ranking: int
    period: DateISO
    birthday: DateISO
    sex: Literal['M', 'F']
    rating_standard: Optional[int]
    rating_rapid: Optional[int]
    rating_blitz: Optional[int]

    @classmethod
    def from_validated_model(
        cls,
        player: Dict[str, Any],
        category: RatingCategory
    ) -> 'FideTopPlayer':
        """
        Creates an instance of FideTopPlayer based on a dictionary
        pulled from the API response and a specified RatingCategory.

        Args:
            player (Dict[str, Any]): A dictionary representing a player.
            category (RatingCategory): A RatingCategory representing a
                chess category (OPEN, WOMEN, JUNIORS, GIRLS).

        Returns:
            FideTopPlayer: A new FideTopPlayer instance.
        """
        fide_player = FidePlayerBasic.from_validated_model(player=player)
        fide_top_player = FideTopPlayerRaw.model_validate(player)
        return cls(
            player=fide_player, category=category, **fide_top_player.model_dump()
        )
    

class FidePlayerDetail(BaseModel):
    """
    A model representing additional detail for a player beyond
    what is provided in the generic FidePlayer model.

    Args:
        player (FidePlayer): A FidePlayer object with all general player fields.
        sex (Literal['M', 'F']): The sex of the player.
        birth_year (DateYear): The birth year of the player.
        rating_standard (int | None): The current standard rating.
        rating_rapid (int | None): The current rapid rating.
        rating_blitz (int | None): The current blitz rating.
    """
    player: FidePlayer
    sex: Literal['M', 'F']
    birth_year: DateYear
    rating_standard: Optional[int]
    rating_rapid: Optional[int]
    rating_blitz: Optional[int]

    @classmethod
    def from_validated_model(cls, player: Dict[str, Any]) -> 'FidePlayerDetail':
        """
        Creates an instance of FidePlayerDetail based on a
        dictionary pulled from the API response.

        Args:
            player (Dict[str, Any]): A dictionary representing a player detail.

        Returns:
            FidePlayerDetail: A new FidePlayerDetail instance.
        """
        fide_player = FidePlayer.from_validated_model(player=player)
        fide_player_detail = FidePlayerDetailRaw.model_validate(player)
        return cls(
            player=fide_player, **fide_player_detail.model_dump()
        )


class FideEvent(BaseRecordPaginationModel):
    """
    A model containing information for a specific Fide event.

    Args:
        name (str): The string name of the event.
        event_id (int): An integer representing a Fide ID for the event.
    """
    name: str = Field(..., validation_alias='name')
    event_id: int = Field(..., validation_alias='id')

    @property
    def event_url(self) -> str:
        """The event URL from the Fide webiste."""
        return build_url(
            base='https://fide.com/calendar/', segments=self.event_id
        )
    
    @classmethod
    def from_validated_model(cls, record: Dict[str, Any]) -> 'FideEvent':
        """
        Creates an instance of FideEvent based on a dictionary
        pulled from the API response.

        Args:
            record (Dict[str, Any]): A dictionary representing a Fide event.

        Returns:
            FideEvent: A FideEvent instance.
        """
        return FideEvent.model_validate(record)


class FideNewsBasic(BaseRecordPaginationModel):
    """
    A slightly less detailed model than the FideNews model. Thus,
    it is referred to as a "basic" version of FideNews.

    Args:
        title (str): The string title of the news story.
        news_id (int): An integer representing a Fide ID for the news story.
    """
    title: str = Field(..., validation_alias='name')
    news_id: int = Field(..., validation_alias='id')

    @property
    def news_url(self) -> str:
        """The new URL from the Fide webiste."""
        return build_url(
            base='https://fide.com/news/', segments=self.news_id
        )
    
    @classmethod
    def from_validated_model(cls, record: Dict[str, Any]) -> 'FideNewsBasic':
        """
        Creates an instance of FideNewsBasic based on a dictionary
        pulled from the API response.

        Args:
            record (Dict[str, Any]): A dictionary representing a Fide
                news story.

        Returns:
            FideNewsBasic: A FideNewsBasic instance.
        """
        return FideNewsBasic.model_validate(record)
    

class FideNews(BaseRecordPaginationModel):
    """
    A model containing information for a specific news story
    published by Fide.

    Args:
        title (str): The string title of the news story.
        news_id (int): An integer representing a Fide ID for the news story.
        posted_at (DateTime): The datetime of posting.
    """
    title: str = Field(..., validation_alias='name')
    news_id: int = Field(..., validation_alias='id')
    posted_at: DateTime

    @classmethod
    def from_validated_model(cls, record: Dict[str, Any]) -> 'FideNews':
        """
        Creates an instance of FideNews based on a dictionary pulled
        from the API response.

        Args:
            record (Dict[str, Any]): A dictionary representing a Fide
                news story.

        Returns:
            FideNews: A FideNews instance.
        """
        return FideNews.model_validate(record)


class FideEventDetail(BaseRecordPaginationModel):
    """
    A model representing additional detail for a Fide event beyond
    what is provided in the generic FideEvent model.

    event (FideEvent): A FideEvent object with all general event fields.
    city (str | None): The city in which the country is taking place.
    country (str | None): The country in which the event is taking place.
    start_date (DateTime | None): The expected start date of the event.
    end_date (DateTime | None): The expected end date of the event.
    game_format (str): The game format.
    tournament_type (str | None): The tournament system (i.e. Swiss).
    time_control (str | None): The time control.
    time_control_desc (str | None): The description of the time control.
    rounds (str | None): The number of rounds.
    players (str | None): The number of players expected to attend.
    telephone (str | None): The telephone number associated with the event.
    website (str | None): The website.
    organizer (str | None): The organizer.
    chief_arbiter (str | None): The chief arbiter.
    chief_organizer (str | None): The chief organizer.
    """
    event: FideEvent
    city: Optional[str]
    country: Optional[str]
    start_date: Optional[DateTime]
    end_date: Optional[DateTime]
    game_format: str
    tournament_type: Optional[str]
    time_control: Optional[str]
    time_control_desc: Optional[str]
    rounds: Optional[str]
    players: Optional[str]
    telephone: Optional[str]
    website: Optional[str]
    organizer: Optional[str]
    chief_arbiter: Optional[str]
    chief_organizer: Optional[str]

    @classmethod
    def from_validated_model(cls, record: Dict[str, Any]) -> 'FideEventDetail':
        """
        Creates an instance of FideEventDetail based on a dictionary
        pulled from the API response.

        Args:
            record (Dict[str, Any]): A dictionary representing detail
                of an event.

        Returns:
            FideEventDetail: A new FideEventDetail instance.
        """
        fide_event = FideEvent.model_validate(record)
        fide_event_detail = FideEventDetailRaw.model_validate(record)
        return cls(
            event=fide_event, **fide_event_detail.model_dump()
        )


class FideNewsDetail(BaseModel):
    """
    A model representing additional detail for a Fide news story
    beyond what is provided in the generic FideNews model.

    news (FideNews): A FideNews object with all general news story fields.
    topic (FideNewsTopic): A FideNewsTopic object representing the news topic.
    category (FideNewsCategory): A FideNewsCategory object representing the
        news category.
    contents (List[FideNewsContent]): A list of FideNewsContent objects
        each representing content included in the news story (HTML, images, ...).
    created_at (DateTime): The datetime of creation.
    updated_at (DateTime): The datetime of the last update.
    """
    news: FideNews
    topic: FideNewsTopic
    category: FideNewsCategory
    contents: List[FideNewsContent]
    created_at: DateTime
    updated_at: DateTime

    @classmethod
    def from_validated_model(cls, news: Dict[str, Any]) -> 'FideNewsDetail':
        """
        Creates an instance of FideNewsDetail based on a dictionary
        pulled from the API response.

        Args:
            news (Dict[str, Any]): A dictionary representing detail of
                a news story.

        Returns:
            FideNewsDetail: A new FideNewsDetail instance.
        """
        fide_news = FideNews.model_validate(news)
        fide_news_detail = FideNewsDetailRaw.model_validate(news)
        return cls(
            news=fide_news, **fide_news_detail.model_dump()
        )


class FideRating(BaseModel):
    """
    Model that represents a rating for a specific game format at the
    end of a month, along with the number of games played in that month.

    Args:
        games (int): The number of games played in a month.
        rating (int | None): The rating at the end of the month.
    """
    games: int
    rating: Optional[int]


class FidePlayerRating(BaseModel):
    """
    Model that represents a set of ratings at the end of a specific
    month. Includes end-of-month ratings for all formats (standard,
    rapid, blitz).

    Args:
        month (DateYearMonth): A specific month.
        player (FidePlayer): A FidePlayer object with all general 
            player fields.
        standard (FideRating): A FideRating object representing the
            standard rating at end-of-month.
        rapid (FideRating): A FideRating object representing the rapid
            rating at end-of-month.
        blitz (FideRating): A FideRating object representing the blitz
            rating at end-of-month.
    """
    month: DateYearMonth
    player: FidePlayer
    standard: FideRating
    rapid: FideRating
    blitz: FideRating
    
    @classmethod
    def from_validated_model(
        cls,
        player: FidePlayer, 
        rating: Dict[str, Any]
    ) -> 'FidePlayerRating':
        """
        Creates an instance of FidePlayerRating based on a dictionary
        pulled from the API response.

        Args:
            player (FidePlayer): A FidePlayer object with all general
                player fields.
            rating (Dict[str, Any]): A dictionary representing all
                ratings for a given month.

        Returns:
            FidePlayerRating: A new FidePlayerRating instance.
        """
        fide_rating = FidePlayerRatingRaw.model_validate(rating)

        # Decompose the raw models into structured models
        standard_rating = FideRating(
            games=fide_rating.games_standard, rating=fide_rating.rating_standard
        )
        rapid_rating = FideRating(
            games=fide_rating.games_rapid, rating=fide_rating.rating_rapid
        )
        blitz_rating = FideRating(
            games=fide_rating.games_blitz, rating=fide_rating.rating_blitz
        )

        return cls(
            player=player,
            month=fide_rating.month,
            standard=standard_rating,
            rapid=rapid_rating,
            blitz=blitz_rating
        )


class FideGames(BaseModel):
    """
    A model that represents all game statistics for a specific game
    format. Included is the total games won, drawn and lost.

    Args:
        games_total (int): The total number of games played.
        games_won (int): The number of games won.
        games_draw (int): The number of games drawn.
        games_lost (int): The number of games lost.
    """
    games_total: int = Field(..., description='Number of total games played')
    games_won: int = Field(..., description='Number of games won')
    games_draw: int = Field(..., description='Number of games drawn')
    games_lost: int = Field(default=0, description='Number of games lost')

    @model_validator(mode='after')
    def validate_parameters(self) -> 'FideGames':
        """Calculates the number of games lost."""
        self.games_lost = (
            self.games_total - self.games_won - self.games_draw
        )
        return self
    

class FideGamesSet(BaseModel):
    """
    A model that represents a set of game statistics for all game
    formats (standard, rapid, blitz).

    Args:
        standard (FideGames): A FideGames object representing the
            games stats for the standard game format.
        rapid (FideGames): A FideGames object representing the games
            stats for the rapid game format.
        blitz (FideGames): A FideGames object representing the games
            stats for the blitz game format.
    """
    standard: FideGames
    rapid: FideGames
    blitz: FideGames


class FidePlayerGameStats(BaseModel):
    """
    A model that represents all game statistics for a specific player,
    partitioned by when playing with both black and white pieces. If
    the 'opponent' attribute is not None, then the game stats are filtered
    by games played against this player, otherwise the entire game history
    is included.

    Args:
        player (FidePlayer): A FidePlayer object with all general player fields.
        opponent (FidePlayer | None): A FidePlayer object with all general
            player fields. Can be None if not specified.
        white (FideGamesSest): The game statistics for all game formats when
            playing with the white pieces.
        black (FideGames Set): The game statistics for all game formats when
            playing with the black pieces.
    """
    player: FidePlayer
    opponent: Optional[FidePlayer]
    white: FideGamesSet
    black: FideGamesSet

    @classmethod
    def from_validated_model(
        cls,
        fide_player: FidePlayer,
        fide_player_opponent: Optional[FidePlayer], 
        stats: Dict[str, Any]
    ) -> 'FidePlayerGameStats':
        """
        Creates an instance of FidePlayerGameStats based on a dictionary
        pulled from the API response.

        Args:
            fide_player (FidePlayer): A FidePlayer object with all general
                player fields.
            fide_player_opponent (FidePlayer): A FidePlayer object with all
                general player fields. Can be None if not specified.
            stats (Dict[str, Any]): A dictionary representing all games stats
                for a given player.

        Returns:
            FidePlayerGameStats: A new FidePlayerGameStats instance.
        """
        def decompose_raw_stats(
            fide_stats: Union[
                FidePlayerGameBlackStatsRaw,
                FidePlayerGameWhiteStatsRaw
            ]
        ) -> FideGamesSet:
            """
            Generates a FideGamesSet object from the white or black raw
            stats model.
            """
            return FideGamesSet(
                standard=FideGames(
                    games_total=fide_stats.standard,
                    games_won=fide_stats.standard_win, 
                    games_draw=fide_stats.standard_draw
                ),
                rapid=FideGames(
                    games_total=fide_stats.rapid,
                    games_won=fide_stats.rapid_win, 
                    games_draw=fide_stats.rapid_draw
                ),
                blitz=FideGames(
                    games_total=fide_stats.blitz,
                    games_won=fide_stats.blitz_win, 
                    games_draw=fide_stats.blitz_draw
                )
            )

        # Validate both white and black models
        stats_white = FidePlayerGameWhiteStatsRaw.model_validate(stats)
        stats_black = FidePlayerGameBlackStatsRaw.model_validate(stats)

        # Decompose the raw models into structured models
        stats_white_decomposed = decompose_raw_stats(fide_stats=stats_white)
        stats_black_decomposed = decompose_raw_stats(fide_stats=stats_black)

        return FidePlayerGameStats(
            player=fide_player,
            opponent=fide_player_opponent,
            white=stats_white_decomposed,
            black=stats_black_decomposed
        )