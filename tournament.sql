-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

CREATE TABLE players (
	id SERIAL primary key,
	player TEXT
	);


CREATE TABLE matches (
	match_id SERIAL primary key,
-- just need winner, loser?
	winner_p integer references players(id),
	loser_p integer references players(id)
	);


'''
select player_id, count(matches) as matches_played
       from matches as a, matches as b
 where a.building = b.building
   and a.room = b.room
   and a.id < b.id
 order by a.building, a.room;
'''


