#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def executeNonQuery(nonQuery, data = None):
    """
    abstracts the common database operations so that
    any non read operation doesn't require a lot of boilerplate. 
    The same could be done of reads, but it's a bit overkill
    for this project.
     """
    conn = connect()
    cur = conn.cursor()
    if data is not None:
        cur.execute(nonQuery, data)
    else:
        cur.execute(nonQuery)
    conn.commit()
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    executeNonQuery("truncate table matches;")

def deletePlayers():
    """Remove all the player records from the database."""
    executeNonQuery("TRUNCATE TABLE players CASCADE;")

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM players")
    players = int(cur.fetchone()[0])
    conn.commit()
    conn.close()
    return players
    
def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    sql = "INSERT INTO players (name) VALUES (%s)"
    data = [name]
    executeNonQuery(sql, data)

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
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM standings;")
    standings = cur.fetchall()
    conn.commit()
    conn.close()
    # Convert long values to integers
    ps = lambda x: (x[0], x[1], int(x[2]), int(x[3])) 
    return map(ps, standings) 

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    executeNonQuery("INSERT INTO matches (winner, loser) VALUES (%s, %s);", (winner,loser))

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
    standings = playerStandings()
    if not standings:
        raise Exception("no players have registered")
    elif len(standings)%2 != 0:
        raise Exception("there are an odd number of players registered." +
            "Please register an even number")
    evenStandings = standings[::2]
    oddStandings = standings[1::2]
    pairings = zip(evenStandings, oddStandings)
    # remove unnecessary info from standings and create necessary pairings formatting
    pairings = map(lambda x: (x[0][0], x[0][1], x[1][0], x[1][1]),pairings)
    return pairings
