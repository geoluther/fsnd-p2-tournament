#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()

    query = "DELETE FROM matches"
    cur.execute(query)

    db.commit()
    cur.close()
    db.close()


    def deletePlayers():
        """Remove all the player records from the database."""
        db = connect()
        cur = db.cursor()

        query = "DELETE FROM players;"
        cur.execute(query)
        db.commit()
        cur.close()
        db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    query = "SELECT count(*) as num FROM players;"
    cur.execute(query)

    players = cur.fetchall()
    count = players[0][0]
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

    db = connect()
    cur = db.cursor()

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

    db = connect()
    cur = db.cursor()

    # results from VIEW
    query = "SELECT id, player, wins, played from results;"

    cur.execute(query)
    players = cur.fetchall()
    # print players

    cur.close()
    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
    winner:  the id number of the player who won
    loser:  the id number of the player who lost
    """

    db = connect()
    cur = db.cursor()

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

    db = connect()
    cur = db.cursor()

    # pairings VIEW
    query = "SELECT id1, name1, id2, name2 from pairings;"

    cur.execute(query)
    pairings = cur.fetchall()
    # print pairings

    cur.close()
    return pairings



def pair_odd():
    # take odd list of players, give one player a bye
    # use python generate pairs, not DB.
    # which table
    db = connect()
    cur = db.cursor()

    # pairings VIEW
    query = "SELECT id1, name1, id2, name2 from pairings;"

    cur.execute(query)
    pairings = cur.fetchall()
    # print pairings

    cur.close()
    return

def addMultiple():
    ''' 30 players in this list '''
    players = ['Oneida Guajardo', 'Arvilla Cesario', \
    'Heriberto Samora', 'Ethyl Moshier', 'Glenna Belford', \
    'Krissy Rainey', 'Hertha Bence', 'Verlie Christofferso', \
    'Paula Jenson', 'Carlee Merriam', 'Krystin Critchlow', \
    'Marcela Aziz', 'Joseph Hooton', 'Marylouise Liechty', \
    'Colette Kistner', 'Marita Simonsen', 'Nella Hutcheson', \
    'Almeta Gonsalves', 'Vanda Barber', 'Mariano Rooney', \
    'Buffy Mcpeak', 'Flossie Borey', 'Iraida Moudy', \
    'Valene Boan', 'Valery Holahan', 'Eugenie Hackney', \
    'Kimbery Spaeth', 'Ali Shelby', 'Kassandra Smock', 
    'Galina Swart', 'Odd Man Out']

    for player in players:
        registerPlayer(player)


def playGames():
    """ pick on random winner in a pair
    we only care about ID indexes p1: 0, p2: 2
    if true, leave pair as is, swap if false

    if odd numbers of players are given, the last player
    gets automatic win.
    """
    pairs = swissPairings();
    print pairs

    for players in pairs:
        print [players[0], players[2]]

        if (random.randint(0, 1) == 1) or (players[2] == ''):
            winner = players[0]
            loser = players[2]
        else:
            winner = players[2]
            loser = players[0]
        
        print [winner, loser]
        reportMatch(winner, loser)


