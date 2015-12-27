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
	winner integer references players(id),
	loser integer references players(id)
	);

-- get rid of name
CREATE VIEW matches_played as
		SELECT id, count(*) as played
        from players left join matches
        on players.id = matches.winner OR players.id = matches.loser
        group by players.id
        order by played desc;


