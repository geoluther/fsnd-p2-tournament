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
	winner integer references players(id),
	loser integer references players(id)
	);


-- this is ok
CREATE VIEW matches_wins as
		SELECT id, players.player, count(matches.winner) as wins
        from players left join matches
        on players.id = matches.winner
        group by players.id
        order by wins desc;

CREATE VIEW v_losses as
		SELECT id, players.player, count(matches.loser) as losses
        from players left join matches
        on players.id = matches.loser
        group by players.id
        order by losses desc;

-- not quite right
CREATE VIEW matches_played as
	SELECT players.id, players.player,
	count(games) as played
	from players left join matches
	on players.id  = matches.winner OR players.id = matches.loser
	group by played
	order by played desc;

--- testing ---

CREATE VIEW standings as
SELECT id, player,
	count(players.id) as played
	from players left join matches
	on players.id = matches.winner OR players.id = matches.loser
	group by players.id
	order by played desc;


CREATE VIEW matches_loss as
		SELECT id, player, count(matches.loser) as losses
        from players left join matches
        on players.id = matches.loser
        group by players.id
        order by losses desc;


CREATE VIEW win_lose as
		SELECT matches_wins.id, matches_wins.player, matches_wins.wins as wins, matches_loss.losses
        from matches_wins left join matches_loss
        on matches_wins.id = matches_loss.id
        order by wins desc;

-- this is closer, at least shows the table right
-- but grouping isn't working
 SELECT id, player, winner, loser
 	  from players left join matches
	  on id = matches.winner OR players.id = matches.loser;

-- this is good
CREATE VIEW results as
SELECT matches_wins.id, matches_wins.player,
	   matches_wins.wins, matches_loss.losses
	   from matches_wins
	   left join matches_loss on matches_wins.id = matches_loss.id;

