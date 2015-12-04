-- Table definitions for the tournament project.  --
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament; 

CREATE DATABASE tournament;
\c tournament;
CREATE TABLE players (
	pid        SERIAL PRIMARY KEY, 
	name       varchar(MAX) NOT NULL
);

INSERT INTO players (pid, name) VALUES (1, 'BYE');

CREATE TABLE matches (
	winner INTEGER NOT NULL,
	loser INTEGER NOT NULL,
	FOREIGN KEY (winner) references players (pid), 
	FOREIGN KEY (loser) references players (pid)
);

CREATE VIEW standings AS
SELECT p.pid, p.name, coalesce(w.wincount, 0) AS cwincount, coalesce(g.playcount,0)
FROM players as p 
LEFT OUTER JOIN 
(
	SELECT winner, COUNT(*) AS wincount
	FROM matches
	GROUP BY winner
) AS w
ON p.pid = w.winner
LEFT OUTER JOIN 
(
	SELECT winner, COUNT(*) AS playcount
	FROM 
	(
		SELECT winner FROM matches
		UNION ALL 
		SELECT loser FROM matches
	) AS allMatches
	GROUP BY winner 
) as g
ON p.pid = g.winner
ORDER BY (coalesce(w.wincount,0)*1.0/coalesce(g.playcount,1)*1.0) DESC;

--CREATE VIEW matchesplayed AS
--SELECT winner, COUNT(*) AS playcount
--FROM 
--(
--	SELECT winner FROM matches
--	UNION ALL
--	SELECT loser FROM matches
--)
 
