from __future__ import annotations

from typing import Any, Dict, Optional, Union

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from python_fide._exceptions import InvalidFideIDError
from python_fide.types._annotated import DateYearMonth


class BaseFideModel(BaseModel):
    """
    Base model for all types. Sets model configuration and basic
    field validation.
    """

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    @field_validator("*", mode="before")
    @classmethod
    def remove_null_strings(cls, value: Union[str, int]) -> Optional[Union[str, int]]:
        """Validation to replace any null strings with None."""
        if value == "":
            return None
        return value


class FidePlayerRatings(BaseFideModel):
    """An intermediate model used in validating the `FidePlayerRating` model."""

    month: str = Field(..., validation_alias="date_2")
    rating_standard: Optional[int] = Field(..., validation_alias="rating")
    rating_rapid: Optional[int] = Field(..., validation_alias="rapid_rtng")
    rating_blitz: Optional[int] = Field(..., validation_alias="blitz_rtng")
    games_standard: Optional[int] = Field(..., validation_alias="period_games")
    games_rapid: Optional[int] = Field(..., validation_alias="rapid_games")
    games_blitz: Optional[int] = Field(..., validation_alias="blitz_games")

    @field_validator("games_standard", "games_rapid", "games_blitz", mode="after")
    @classmethod
    def override_none(cls, value: Optional[int]) -> int:
        """Validator to return a 0 if the value is None."""
        return value or 0


class FidePlayerGameWhiteStats(BaseFideModel):
    """
    An intermediate model used in validating the white game stats fields
    in the `FidePlayerGameStats` model.
    """

    total: int = Field(..., validation_alias="white_total")
    total_win: int = Field(..., validation_alias="white_win_num")
    total_draw: int = Field(..., validation_alias="white_draw_num")
    standard: int = Field(..., validation_alias="white_total_std")
    standard_win: int = Field(..., validation_alias="white_win_num_std")
    standard_draw: int = Field(..., validation_alias="white_draw_num_std")
    rapid: int = Field(..., validation_alias="white_total_rpd")
    rapid_win: int = Field(..., validation_alias="white_win_num_rpd")
    rapid_draw: int = Field(..., validation_alias="white_draw_num_rpd")
    blitz: int = Field(..., validation_alias="white_total_blz")
    blitz_win: int = Field(..., validation_alias="white_win_num_blz")
    blitz_draw: int = Field(..., validation_alias="white_draw_num_blz")

    @field_validator("*", mode="before")
    @classmethod
    def override_none(cls, value: Optional[int]) -> int:
        """Validator to return a 0 if the value is None."""
        return value or 0


class FidePlayerGameBlackStats(BaseFideModel):
    """
    An intermediate model used in validating the black game stats fields
    in the `FidePlayerGameStats` model.
    """

    total: int = Field(..., validation_alias="black_total")
    total_win: int = Field(..., validation_alias="black_win_num")
    total_draw: int = Field(..., validation_alias="black_draw_num")
    standard: int = Field(..., validation_alias="black_total_std")
    standard_win: int = Field(..., validation_alias="black_win_num_std")
    standard_draw: int = Field(..., validation_alias="black_draw_num_std")
    rapid: int = Field(..., validation_alias="black_total_rpd")
    rapid_win: int = Field(..., validation_alias="black_win_num_rpd")
    rapid_draw: int = Field(..., validation_alias="black_draw_num_rpd")
    blitz: int = Field(..., validation_alias="black_total_blz")
    blitz_win: int = Field(..., validation_alias="black_win_num_blz")
    blitz_draw: int = Field(..., validation_alias="black_draw_num_blz")

    @field_validator("*", mode="before")
    @classmethod
    def override_none(cls, value: Optional[int]) -> int:
        """Validator to return a 0 if the value is None."""
        return value or 0


class FidePlayerID(BaseModel):
    """
    A simple `pydantic` model used to validate an represent a Fide ID.

    Args:
        fide_id (int): An integer representing a valid Fide ID.
    """

    fide_id: int

    @field_validator("fide_id", mode="before")
    @classmethod
    def cast_to_int(cls, fide_id: Union[str, int]) -> int:
        """Validate and cast fide_id to an integer type."""
        if isinstance(fide_id, str):
            if not fide_id.isdigit():
                raise InvalidFideIDError(
                    "invalid Fide ID entered, must be an integer (as str in int type)"
                )

            if fide_id.startswith("0"):
                raise InvalidFideIDError(
                    "invalid Fide ID entered, cannot start with a zero"
                )

            try:
                entity_id_cast = int(fide_id)
            except ValueError:
                raise InvalidFideIDError(
                    "invalid Fide ID entered, must be an equivalent integer"
                )
            else:
                return entity_id_cast
        else:
            return fide_id


class FidePlayer(BaseModel):
    """
    A model containing information for a specific player who has
    registered with Fide.

    Args:
        fide_id (int): An integer representing the Fide ID of
            the player.
        name (str): The string full name.
        country (str): The country that the player represents.
    """

    fide_id: int = Field(..., validation_alias=AliasChoices("fide_id", "id_number"))
    name: str = Field(..., validation_alias="name")
    country: str


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
        month (`DateYearMonth`): A `DateYearMonth` object representing a
            specific year and month.
        player (`FidePlayerID`): A `FidePlayerID` object.
        standard (`FideRating`): A `FideRating` object representing the
            standard rating at end-of-month.
        rapid (`FideRating`): A `FideRating` object representing the rapid
            rating at end-of-month.
        blitz (`FideRating`): A `FideRating` object representing the blitz
            rating at end-of-month.
    """

    month: DateYearMonth
    fide_id: FidePlayerID
    standard: FideRating
    rapid: FideRating
    blitz: FideRating

    @classmethod
    def from_validated_model(
        cls, fide_id: FidePlayerID, rating: Dict[str, Any]
    ) -> FidePlayerRating:
        """
        Creates an instance of `FidePlayerRating` based on a dictionary
        pulled from the API response.

        Args:
            player (`FidePlayer`): A `FidePlayer` object with all general
                player fields.
            rating (Dict[str, Any]): A dictionary representing all
                ratings for a given month.

        Returns:
            `FidePlayerRating`: A new `FidePlayerRating` instance.
        """
        fide_rating = FidePlayerRatings.model_validate(rating)

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
            fide_id=fide_id,
            month=fide_rating.month,
            standard=standard_rating,
            rapid=rapid_rating,
            blitz=blitz_rating,
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

    games_total: int = Field(..., description="Number of total games played")
    games_won: int = Field(..., description="Number of games won")
    games_draw: int = Field(..., description="Number of games drawn")
    games_lost: int = Field(default=0, description="Number of games lost")

    @model_validator(mode="after")
    def validate_parameters(self) -> FideGames:
        """Calculates the number of games lost."""
        self.games_lost = self.games_total - self.games_won - self.games_draw
        return self


class FideGamesSet(BaseModel):
    """
    A model that represents a set of game statistics for all game
    formats (standard, rapid, blitz).

    Args:
        standard (`FideGames`): A `FideGames` object representing the
            games stats for the standard game format.
        rapid (`FideGames`): A `FideGames` object representing the games
            stats for the rapid game format.
        blitz (`FideGames`): A `FideGames` object representing the games
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
        fide_id (`FidePlayerID`): A `FidePlayerID` object.
        opponent (`FidePlayerID` | None): A `FidePlayerID` object.Can be
            None if not specified.
        white (`FideGamesSet`): The game statistics for all game formats when
            playing with the white pieces.
        black (`FideGamesSet`): The game statistics for all game formats when
            playing with the black pieces.
    """

    fide_id: FidePlayerID
    opponent: Optional[FidePlayerID]
    white: FideGamesSet
    black: FideGamesSet

    @classmethod
    def from_validated_model(
        cls,
        fide_id: FidePlayerID,
        fide_id_opponent: Optional[FidePlayerID],
        stats: Dict[str, Any],
    ) -> FidePlayerGameStats:
        """
        Creates an instance of `FidePlayerGameStats` based on a dictionary
        pulled from the API response.

        Args:
            fide_player (`FidePlayerID`): A `FidePlayerID` object.
            fide_player_opponent (`FidePlayerID`): A `FidePlayerID` object.
                Can be None if not specified.
            stats (Dict[str, Any]): A dictionary representing all games stats
                for a given player.

        Returns:
            `FidePlayerGameStats`: A new `FidePlayerGameStats` instance.
        """

        def decompose_raw_stats(
            fide_stats: Union[FidePlayerGameBlackStats, FidePlayerGameWhiteStats]
        ) -> FideGamesSet:
            """
            Generates a `FideGamesSet` object from the white or black raw
            stats model.
            """
            return FideGamesSet(
                standard=FideGames(
                    games_total=fide_stats.standard,
                    games_won=fide_stats.standard_win,
                    games_draw=fide_stats.standard_draw,
                ),
                rapid=FideGames(
                    games_total=fide_stats.rapid,
                    games_won=fide_stats.rapid_win,
                    games_draw=fide_stats.rapid_draw,
                ),
                blitz=FideGames(
                    games_total=fide_stats.blitz,
                    games_won=fide_stats.blitz_win,
                    games_draw=fide_stats.blitz_draw,
                ),
            )

        # Validate both white and black models
        stats_white = FidePlayerGameWhiteStats.model_validate(stats)
        stats_black = FidePlayerGameBlackStats.model_validate(stats)

        # Decompose the raw models into structured models
        stats_white_decomposed = decompose_raw_stats(fide_stats=stats_white)
        stats_black_decomposed = decompose_raw_stats(fide_stats=stats_black)

        return FidePlayerGameStats(
            fide_id=fide_id,
            opponent=fide_id_opponent,
            white=stats_white_decomposed,
            black=stats_black_decomposed,
        )
