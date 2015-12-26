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
--  p1, p2, winner match player id
	player1 integer references players(id),
	player2 integer references players(id),
	p1_score integer,
	p2_score integer,
	winner integer
	);



