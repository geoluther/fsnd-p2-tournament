#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # return psycopg2.connect("dbname=tournament")

    try:
        db = psycopg2.connect("dbname={}".format("tournament"))
        cursor = db.cursor()
        return db, cursor
    except:
        print("error, could not connect to db")



def deleteMatches():
    """Remove all the match records from the database."""
    db, cur = connect()

    query = "DELETE FROM matches"
    cur.execute(query)

    db.commit()
    cur.close()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cur = connect()

    query = "DELETE FROM players;"
    cur.execute(query)
    db.commit()
    cur.close()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cur = connect()
    query = "SELECT count(*) as num FROM players;"
    cur.execute(query)

    # fetchone, since query returns just one row
    players = cur.fetchone()
    count = players[0]
    cur.close()
    db.close()

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db, cur = connect()

    # use string formatting for query params
    query = "INSERT INTO players (player) VALUES (%s)"
    data = (name, )

    cur.execute(query, data)
    db.commit()

    cur.close()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, cur = connect()

    # results from VIEW
    query = "SELECT id, player, wins, played from results order by wins desc;"

    cur.execute(query)
    players = cur.fetchall()

    cur.close()
    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, cur = connect()

    # use string formatting for query params
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    data = (winner, loser, )

    cur.execute(query, data)
    db.commit()

    cur.close()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    db, cur = connect()

    # use pairings VIEW to get pairings
    query = "SELECT id1, name1, id2, name2 from pairings;"

    cur.execute(query)
    pairings = cur.fetchall()

    cur.close()
    return pairings


# xtra credit

# add many players to db
def addMultiple():
    """31 players in this list"""

    players = ( ['Oneida Guajardo', 'Arvilla Cesario',
    'Heriberto Samora', 'Ethyl Moshier', 'Glenna Belford',
    'Krissy Rainey', 'Hertha Bence', 'Verlie Christofferso',
    'Paula Jenson', 'Carlee Merriam', 'Krystin Critchlow',
    'Marcela Aziz', 'Joseph Hooton', 'Marylouise Liechty',
    'Colette Kistner', 'Marita Simonsen', 'Nella Hutcheson',
    'Almeta Gonsalves', 'Vanda Barber', 'Mariano Rooney',
    'Buffy Mcpeak', 'Flossie Borey', 'Iraida Moudy',
    'Valene Boan', 'Valery Holahan', 'Eugenie Hackney',
    'Kimbery Spaeth', 'Ali Shelby', 'Kassandra Smock',
    'Galina Swart', 'Odd Man Out'] )

    for player in players:
        registerPlayer(player)


def playGames():
    """Choose a random winner in each pairing

    If odd numbers of players are given, the last player
    is always given automatic win.
    """
    pairs = swissPairings();
    last_pair = pairs[-1]
    print last_pair

    # check last pair for odd players
    # odd_players = (pair[-1] == None)

    odd_players = oddPair(last_pair)
    print "Odd Players: ", odd_players

    # odd_players = False

    # ucomment later
    # better: if odd and odd player has bye...
    # if true, regenerate pairs accounting for byes
    # if odd_players:
    #     pairs = regenPairs(last_pair)

    for players in pairs:
        # ID indexes in pairs: p1 = players[0], p2 = players[2]
        # if rand = 1 or no p2, p1 wins, gets bye
        if (oddPair(players)):
            # odd players, p1 gets a win and a bye
            print "i'm in a last pair!"
            winner = players[0]
            loser = players[2]
            print "Winner: ", winner
            print "Loser: ", loser
            giveBye(players[0])
        elif (random.randint(0, 1) == 1):
            # p1 wins by random
            winner = players[0]
            loser = players[2]
        else: # p2 gets win
            winner = players[2]
            loser = players[0]

        reportMatch(winner, loser)



"""
UPDATE byes
   SET byes_played = byes_played + 1
WHERE id = 'bill';
"""

def giveBye(id):
    """Give a bye to player with id"""
    db, cur = connect()

    query = "UPDATE players SET byes = byes + 1 WHERE id = %s;"
    data = (id,)

    cur.execute(query, data)
    db.commit()
    cur.close()
    db.close()


def regenPairs(last_pair, pairs):
    #  get player id
    p = pairs
    odd_player = last_pair[0]
    if hasBye(odd_player):
        # resort pairs
        p = resort(pairs)

        return p
    else:
        return p

def resort():
    """takes a tuple of pairs, resorts by byes, returns a tuple
    do i need to even pass pairs?

    """
    # fields: id1, name1, p1_byes, id2, name2, p2_byes
    pairs = swissWithByes()
    p = [list(i) for i in pairs]

    last = p.pop()
    pid = last[0]
    p_byes last[2]

    p.reverse()


    # return expects player id in [0] and [2]



def hasBye(id):
    """returns True if player ID has a bye, otherwise False"""
    db, cur = connect()

    query = "SELECT id, byes from players where id = %s;"
    data = (id,)

    cur.execute(query, data)
    result = cur.fetchone()
    cur.close()

    byes = result[2]
    return byes > 0


def oddPair(pair):
    return pair[-1] == None


def swissWithByes():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains
      (id1, name1, , id1_byes, id2, name2, id2_byes)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db, cur = connect()

    # uses pairings_with_byes VIEW
    query = "SELECT id1, name1, p1_byes, id2, name2, p2_byes from pairings_with_byes;"
    cur.execute(query)
    pairings = cur.fetchall()
    cur.close()
    return pairings




