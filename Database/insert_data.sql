-- Insert into Player
INSERT INTO Player (PlayerID, FirstName, LastName, Raiting)
VALUES (NULL, 'John', 'Doe', 1500);

INSERT INTO Player (PlayerID, FirstName, LastName, Raiting)
VALUES (NULL, 'Jane', 'Smith', 1600);

INSERT INTO Player (PlayerID, FirstName, LastName, Raiting)
VALUES (NULL, 'Bob', 'Johnson', 1550);

INSERT INTO Player (PlayerID, FirstName, LastName, Raiting)
VALUES (NULL, 'Alice', 'Williams', 1620);

INSERT INTO Player (PlayerID, FirstName, LastName, Raiting)
VALUES (NULL, 'Charlie', 'Brown', 1480);

INSERT INTO Player (PlayerID, FirstName, LastName, Raiting)
VALUES (NULL, 'Eva', 'Green', 1575);

INSERT INTO PlayerDetails (DateOfBirth, Email, PhoneNumber, PlayerID)
VALUES (TO_DATE('1990-01-15', 'YYYY-MM-DD'), 'john.doe@example.com', '0712345678', 1);

INSERT INTO PlayerDetails (DateOfBirth, Email, PhoneNumber, PlayerID)
VALUES (TO_DATE('1988-05-20', 'YYYY-MM-DD'), 'jane.smith@example.com', '0723456789', 2);

INSERT INTO PlayerDetails (DateOfBirth, Email, PhoneNumber, PlayerID)
VALUES (TO_DATE('1995-12-10', 'YYYY-MM-DD'), 'bob.johnson@example.com', '0734567890', 3);

INSERT INTO PlayerDetails (DateOfBirth, Email, PhoneNumber, PlayerID)
VALUES (TO_DATE('1985-08-05', 'YYYY-MM-DD'), 'alice.williams@example.com', '0745678901', 4);

INSERT INTO PlayerDetails (DateOfBirth, Email, PhoneNumber, PlayerID)
VALUES (TO_DATE('1992-03-25', 'YYYY-MM-DD'), 'charlie.brown@example.com', '0756789012', 5);

INSERT INTO PlayerDetails (DateOfBirth, Email, PhoneNumber, PlayerID)
VALUES (TO_DATE('1998-09-15', 'YYYY-MM-DD'), 'eva.green@example.com', '0767890123', 6);


-- Insert into Tournament
INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize)
VALUES (NULL, 'Chess Masters 2023', TO_DATE('2023-03-01', 'YYYY-MM-DD'), TO_DATE('2023-03-10', 'YYYY-MM-DD'), 'New York', 5000);

INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize)
VALUES (NULL, 'Grand Slam 2023', TO_DATE('2023-04-05', 'YYYY-MM-DD'), TO_DATE('2023-04-15', 'YYYY-MM-DD'), 'London', 7500);

INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize)
VALUES (NULL, 'World Chess Championship', TO_DATE('2023-06-01', 'YYYY-MM-DD'), TO_DATE('2023-06-15', 'YYYY-MM-DD'), 'Moscow', 10000);

INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize)
VALUES (NULL, 'Rapid Chess Open', TO_DATE('2023-08-10', 'YYYY-MM-DD'), TO_DATE('2023-08-20', 'YYYY-MM-DD'), 'Paris', 6000);

INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize)
VALUES (NULL, 'Blitz Championship', TO_DATE('2023-09-05', 'YYYY-MM-DD'), TO_DATE('2023-09-15', 'YYYY-MM-DD'), 'Berlin', 8000);

INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize)
VALUES (NULL, 'Chess Olympiad', TO_DATE('2023-11-01', 'YYYY-MM-DD'), TO_DATE('2023-11-15', 'YYYY-MM-DD'), 'Athens', 9000);


-- Insert into Registration
INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 1, 1);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 2, 1);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 3, 2);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 4, 2);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 5, 3);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 6, 3);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 1, 2);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 2, 2);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 3, 1);

INSERT INTO Registration (RegistrationID, PlayerID, TournamentID)
VALUES (NULL, 4, 1);

-- Insert into Game

INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay)
VALUES (NULL, 1, 2, '1/8', 1, 10);

INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay)
VALUES (NULL, 3, 4, '1/8', 2, 12);

INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay)
VALUES (NULL, 5, 6, '1/8', 3, 15);

INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay)
VALUES (NULL, 1, 9, '1/8', 1, 8);

INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay)
VALUES (NULL, 2, 10, '1/8', 2, 14);

INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay)
VALUES (NULL, 3, 7, '1/8', 1, 20);

-- Insert into Game Moves
INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation)
VALUES (NULL, 1, 1, 'e4');

INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation)
VALUES (NULL, 1, 2, 'c5');

INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation)
VALUES (NULL, 1, 3, 'Nf3');

INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation)
VALUES (NULL, 2, 1, 'd4');

INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation)
VALUES (NULL, 2, 2, 'e6');

INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation)
VALUES (NULL, 2, 3, 'c4');




