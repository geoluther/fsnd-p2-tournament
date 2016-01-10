-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

-- create tables

CREATE TABLE players (
	id SERIAL primary key,
	player TEXT,
	byes integer default 0
	);

CREATE TABLE matches (
	match_id SERIAL primary key,
	winner integer references players(id),
	loser integer references players(id)
	);

/* VIEWS do data manipulation */

CREATE VIEW matches_wins as
		SELECT id, players.player, count(matches.winner) as wins,
		byes
        from players left join matches
        on players.id = matches.winner
        group by players.id
        order by wins desc;


CREATE VIEW matches_loss as
		SELECT id, player, count(matches.loser) as losses,
		byes
        from players left join matches
        on players.id = matches.loser
        group by players.id
        order by losses desc;


CREATE VIEW results as
SELECT matches_wins.id, matches_wins.player,
	   matches_wins.wins, matches_loss.losses,
	   matches_wins.byes, (matches_wins.wins + matches_loss.losses) as played
	   from matches_wins
	   left join matches_loss on matches_wins.id = matches_loss.id
	   order by matches_wins.wins desc;


/* rank all players by wins*/
CREATE VIEW rankings as
select row_number() over(order by wins desc) as rank,
* from matches_wins;


/* Bracket views - split rank orders to each side by odd and even ranks
   Place odd ranked players  (1, 3, 5, etc )in left bracket, even in right.
*/

CREATE VIEW bracket_right as
select row_number() over(order by wins desc) as order,
* from rankings where mod(rank, 2) = 0;


CREATE VIEW bracket_left as
select row_number() over(order by wins desc) as order,
* from rankings where mod(rank, 2) = 1;


/* Generate pairings by putting left and right bracket in adjacent columns */
CREATE VIEW pairings as
select l.order,
l.wins as lwins, l.id as id1, l.player as name1,
r.wins as rwins, r.id as id2, r.player as name2
from bracket_left as l
left join bracket_right as r on l.order = r.order;


CREATE VIEW pairings_with_byes as
select l.order,
l.wins as lwins, l.id as id1, l.player as name1, l.byes as p1_byes,
r.wins as rwins, r.id as id2, r.player as name2, r.byes as p2_byes
from bracket_left as l
left join bracket_right as r on l.order = r.order;
