## FSND Project 2: tournament pairings

### Usage:

In order to first create the database and its schema please execute the following commands from your system's command line: `$ psql -f tournament.sql`

To test functions, run `$ python tournament_test.py`

### Xtra Credit - Odd Number of Players

in *tournament.py*

`addMultiple()` : adds 31 players to the touranment DB

`playGames()` : Runs games pairing all players in tournament, giving the player ranked last a bye and win if there are an odd number of players.