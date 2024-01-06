-- Violating Round Number Constraint
INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay) VALUES (NULL, 1, 2, 'NOT 1/8', 1, 10);

-- Violating Rating in Play Constraint
INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay) VALUES (NULL, 1, 2, '1/8', 1, 1000);

-- Violating Move Number Constraint
INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation) VALUES (NULL, 1, 1000, 'e4');

-- Violating Move Notation Constraint
INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation) VALUES (NULL, 1, 1, 'InvalidMove');

-- Violating First Name Constraint
INSERT INTO Player (PlayerID, FirstName, LastName, Raiting) VALUES (NULL, '123', 'Doe', 1500);

-- Violating Last Name Constraint
INSERT INTO Player (PlayerID, FirstName, LastName, Raiting) VALUES (2, 'John', '123', 1600);

-- Violating Rating Constraint
INSERT INTO Player (PlayerID, FirstName, LastName, Raiting) VALUES (NULL, 'Alice', 'Smith', 'NotANumber');

-- Violating Email Constraint
INSERT INTO PlayerDetails (DateOfBirth, Email, PhoneNumber, PlayerID) VALUES (TO_DATE('1990-01-01', 'YYYY-MM-DD'), 'invalid.email', '0734567890', 1);

-- Violating Phone Constraint
INSERT INTO PlayerDetails (DateOfBirth, Email, PhoneNumber, PlayerID) VALUES (TO_DATE('1990-01-01', 'YYYY-MM-DD'), 'valid@email.com', '1234567890', 1);

-- Violating Unique Constraint
INSERT INTO Registration (RegistrationID, PlayerID, TournamentID) VALUES (NULL, 1, 1);
INSERT INTO Registration (RegistrationID, PlayerID, TournamentID) VALUES (NULL, 1, 1);

-- Violating Tournament Name Constraint
INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize) VALUES (NULL, 'Invalid!@#', TO_DATE('2023-01-01', 'YYYY-MM-DD'), TO_DATE('2023-01-10', 'YYYY-MM-DD'), 'City', 10000);

-- Violating Tournament Duration Constraint
INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize) VALUES (NULL, 'Chess Tournament', TO_DATE('2023-01-01', 'YYYY-MM-DD'), TO_DATE('2023-01-01', 'YYYY-MM-DD'), 'City', 10000);

-- Violating Tournament Location Constraint
INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize) VALUES (NULL, 'Chess Tournament', TO_DATE('2023-01-01', 'YYYY-MM-DD'), TO_DATE('2023-01-10', 'YYYY-MM-DD'), 'Invalid!@#', 10000);


-- Violating Tournament Prize Constraint
INSERT INTO Tournament (TournamentID, TournamentName, StartDate, EndDate, Location, Prize) VALUES (NULL, 'Chess Tournament', TO_DATE('2023-01-01', 'YYYY-MM-DD'), TO_DATE('2023-01-10', 'YYYY-MM-DD'), 'City', 100000000);

-- Violating GameMoves Foreign Key Constraint
INSERT INTO GameMoves (MoveID, GameID, MoveNumber, MoveNotation) VALUES (NULL, 999, 1, 'e4');

-- Violating Game Foreign Key Constraints
INSERT INTO Game (GameID, WinnerID, LoserID, RoundNumber, BoardNumber, RaitingInPlay) VALUES (NULL, 999, 2, '1/8', 1, 10);



