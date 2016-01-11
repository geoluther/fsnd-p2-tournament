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

    If odd numbers of players are given, last player gets
    automatic win, unless already has a bye.

    If so, give bye to next player above without a bye, swap
    that player's opponent with the last player.
    """
    pairs = swissPairings();
    last_pair = pairs[-1]

    # check last pair for odd players
    odd_players = oddPair(last_pair)

    # if odd players, and last player had a bye
    # generate pairs, could be implemented without
    # need for swissPairings() above tho...
    if odd_players and hasBye(last_pair[0]):
        pairs = regenPairs()

    for players in pairs:
        # ID indexes in pairs: p1 = players[0], p2 = players[2]
        # if rand = 1 or no p2, p1 wins, gets bye
        if (oddPair(players)):
            # odd players, p1 gets a win and a bye
            winner = players[0]
            loser = players[2]
            giveBye(players[0])
        elif (random.randint(0, 1) == 1):
            # p1 wins by random
            winner = players[0]
            loser = players[2]
        else: # p2 gets win
            winner = players[2]
            loser = players[0]

        reportMatch(winner, loser)


def giveBye(id):
    """Give a bye to player with id"""
    db, cur = connect()

    query = "UPDATE players SET byes = byes + 1 WHERE id = %s;"
    data = (id,)

    cur.execute(query, data)
    db.commit()
    cur.close()
    db.close()


### will use rankings_with_byes, not swiss pair funct
def regenPairs():
    """ regen pairings accounting for byes
        Swiss Pairing generated by python, not from psql view.
    """
    db, cur = connect()

    # fields in rankings_with_byes: rank, id, player, wins, byes
    query = "SELECT id, player, wins, byes from rankings_with_byes;"
    cur.execute(query)
    rankings = cur.fetchall()

    cur.close()
    db.close()

    # don't we already know if odd and needs resorting?
    # if odd and hasBye(rankings[-1]):
    rankings = re_sort(rankings)

    # build left and right sides of pairs
    left, right = [], []

    for i in range(len(rankings)):
        if i % 2 == 0:
            left.append(rankings[i])
        else:
            right.append(rankings[i])

    # append nulls if odd to right pair
    # although they should be odd anyway...
    if len(right) == len(left) - 1:
        right.append((None, None, None, None))

    # combine left and right sides of pairings
    pairings = [ (left[i] + right[i]) for i in xrange(len(left)) ]

    # reformat pairings to what playGames() expects
    # return [ (id1, name1, id1, name2), ... ]
    pairs = [(i[0], i[1], i[4], i[5]) for i in pairings]
    return pairs


def re_sort(rank_file):
    # don't change rank_file
    ranks =  list(rank_file)
    last_player = ranks.pop()
    ranks.reverse()

    for i in range(len(ranks)):
        if ranks[i][-1] == 0:
            # swap player with a bye to one without
            give_bye = ranks[i]
            ranks[i] = last_player
            break

    ranks.reverse()
    ranks.append(give_bye)

    return ranks


def oddPair(pair):
    """ return true if only 1 player i pair"""
    return pair[-1] == None


def hasBye(id):
    """returns True if player ID has a bye, otherwise False"""
    db, cur = connect()

    query = "SELECT id, byes from players where id = %s;"
    data = (id,)

    cur.execute(query, data)
    result = cur.fetchone()
    cur.close()

    byes = result[1]
    return byes > 0


def showRWB():
    """utility function for testing and data verification only"""
    db, cur = connect()

    # fields in rankings_with_byes: rank, id, player, wins, byes
    query = "SELECT rank, id, player, wins, byes from rankings_with_byes;"
    cur.execute(query)
    rankings = cur.fetchall()

    cur.close()
    db.close()

    return rankings


