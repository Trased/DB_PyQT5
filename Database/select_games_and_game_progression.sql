-- Outputs all the games played ordered by tournament.

SELECT
    t.TournamentName AS Tournament,
    g.GameID,
    p1.FirstName || ' ' || p1.LastName AS Winner,
    p2.FirstName || ' ' || p2.LastName AS Loser,
    g.RoundNumber,
    g.BoardNumber,
    g.RaitingInPlay
FROM
    Game g
JOIN Registration r1 ON g.WinnerID = r1.RegistrationID
JOIN Registration r2 ON g.LoserID = r2.RegistrationID
JOIN Player p1 ON r1.PlayerID = p1.PlayerID
JOIN Player p2 ON r2.PlayerID = p2.PlayerID
JOIN Tournament t ON r1.TournamentID = t.TournamentID
ORDER BY
    t.TournamentName,
    g.GameID;


-- Outputs the progress of each game (ordered by game_id)

SELECT
    GM.MoveID,
    GM.GameID,
    GM.MoveNumber,
    GM.MoveNotation
FROM
    GameMoves GM
JOIN
    Game G ON GM.GameID = G.GameID
ORDER BY
    G.GameID;

-- Outputs all the tournaments where a player is registred

SELECT DISTINCT
    p.FirstName || ' ' || p.LastName AS PlayerName,
    t.TournamentName,
    t.StartDate,
    t.EndDate,
    t.Location,
    t.Prize
FROM
    Player p
JOIN
    PlayerDetails pd ON p.PlayerID = pd.PlayerID
JOIN
    Registration r ON p.PlayerID = r.PlayerID
JOIN
    Tournament t ON r.TournamentID = t.TournamentID
ORDER BY
    PlayerName;


