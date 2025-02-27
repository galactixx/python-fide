# python-fide
![Tests](https://github.com/galactixx/python-fide/actions/workflows/continuous_integration.yaml/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/python-fide.svg)](https://pypi.org/project/python-fide/)
[![Python versions](https://img.shields.io/pypi/pyversions/python-fide.svg)](https://pypi.org/project/python-fide/)
[![License](https://img.shields.io/github/license/galactixx/python-fide.svg)](https://github.com/galactixx/python-fide/blob/main/LICENSE)
![PyPI Downloads](https://static.pepy.tech/badge/python-fide/month)
![PyPI Downloads](https://static.pepy.tech/badge/python-fide)

## 🌍 **Overview**
`python-fide` is a Python package that provides an interface for retrieving detailed information about chess players from the FIDE API. This package allows users to access data such as player details, historical ratings, game statistics, and player opponents.

## 📦 **Installation**
You can install `python-fide` using pip:
```sh
pip install python-fide
```

## 📚 **Usage**
### Importing the Client
To use the package, import the `FidePlayerClient` class and instantiate it:
```python
from python_fide.clients_sync.fide_player_client import FidePlayerClient

client = FidePlayerClient()
```

### Retrieve Player Opponents
You can retrieve a list of opponents a player has faced using their FIDE ID:
```python
from python_fide.types.core import FidePlayerID

fide_id = FidePlayerID(fide_id=123456)
opponents = client.get_opponents(fide_id)

print(opponents)
```
#### Example Output:
```python
[
    FidePlayer(fide_id=654321, name="Opponent Name", country="USA"),
    FidePlayer(fide_id=789012, name="Another Opponent", country="UK")
]
```

### Retrieve Rating Progress Chart
To get the rating progress chart of a player, use:
```python
from python_fide.enums import Period

ratings = client.get_rating_progress_chart(fide_id, period=Period.TWO_YEARS)

print(ratings)
```
#### Example Output:
```python
[
    FidePlayerRating(
        month="2023-06",
        fide_id=FidePlayerID(fide_id=123456),
        standard=FideRating(games=10, rating=2500),
        rapid=FideRating(games=5, rating=2450),
        blitz=FideRating(games=8, rating=2400)
    )
]
```

### Retrieve Game Statistics
To get game statistics for a player, optionally filtering by an opponent:
```python
stats = client.get_game_stats(fide_id)
```
To get statistics against a specific opponent:
```python
opponent_id = FidePlayerID(fide_id=654321)
stats = client.get_game_stats(fide_id, fide_id_opponent=opponent_id)
print(stats)
```
#### Example Output:
```python
FidePlayerGameStats(
    fide_id=FidePlayerID(fide_id=123456),
    opponent=FidePlayer(fide_id=654321, name="Opponent Name", country="USA"),
    white=FideGamesSet(
        standard=FideGames(games_total=30, games_won=15, games_draw=10, games_lost=5),
        rapid=FideGames(games_total=20, games_won=10, games_draw=5, games_lost=5),
        blitz=FideGames(games_total=25, games_won=12, games_draw=8, games_lost=5)
    ),
    black=FideGamesSet(
        standard=FideGames(games_total=28, games_won=14, games_draw=9, games_lost=5),
        rapid=FideGames(games_total=18, games_won=9, games_draw=5, games_lost=4),
        blitz=FideGames(games_total=22, games_won=11, games_draw=7, games_lost=4)
    )
)
```

## 🔍 **API Reference**

| Method | Description | Arguments | Returns |
|--------|-------------|------------|----------|
| `get_opponents(fide_player: FidePlayerID) -> List[FidePlayer]` | Retrieves a list of opponents a player has faced. | `fide_player` (FidePlayerID): The FIDE ID of the player. | `List[FidePlayer]`: A list of FIDE players the given player has faced. |
| `get_rating_progress_chart(fide_id: FidePlayerID, period: Optional[Period] = None) -> List[FidePlayerRating]` | Retrieves the rating progress chart for a player. | `fide_id` (FidePlayerID): The FIDE ID of the player. `period` (Optional[Period]): The period to filter the rating history. | `List[FidePlayerRating]`: A list of rating history data. |
| `get_game_stats(fide_id: FidePlayerID, fide_id_opponent: Optional[FidePlayerID] = None) -> FidePlayerGameStats` | Retrieves game statistics for a player. | `fide_id` (FidePlayerID): The FIDE ID of the player. `fide_id_opponent` (Optional[FidePlayerID]): The FIDE ID of an opponent to filter game statistics. | `FidePlayerGameStats`: The game statistics for the given player. |

## 🤝 **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 📞 **Contact**

If you have any questions or need support, feel free to reach out by opening an issue on the [GitHub repository](#).

