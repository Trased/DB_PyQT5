-- Generated by Oracle SQL Developer Data Modeler 4.1.3.901
--   at:        2023-12-21 11:15:01 EET
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g




CREATE TABLE Game
  (
    GameID        NUMBER (10) NOT NULL ,
    WinnerID      NUMBER (10) NOT NULL ,
    LoserID       NUMBER (10) NOT NULL ,
    RoundNumber   VARCHAR2 (3) ,
    BoardNumber   NUMBER (10) ,
    RaitingInPlay NUMBER (3)
  ) ;
ALTER TABLE Game ADD CONSTRAINT round_number_const CHECK ( REGEXP_LIKE(RoundNumber, '^(1/16|1/8|1/4|1/2|1)$')) ;
ALTER TABLE Game ADD CONSTRAINT raiting_in_play_const CHECK ( REGEXP_LIKE(RaitingInPlay, '^[0-9]{1,2}$')) ;
ALTER TABLE Game ADD CONSTRAINT Game_PK PRIMARY KEY ( GameID ) ;


CREATE TABLE GameMoves
  (
    MoveID       NUMBER (10) NOT NULL ,
    GameID       NUMBER (10) NOT NULL ,
    MoveNumber   NUMBER (3) NOT NULL ,
    MoveNotation VARCHAR2 (7) NOT NULL
  ) ;
ALTER TABLE GameMoves ADD CONSTRAINT move_number_const CHECK ( REGEXP_LIKE(MoveNumber, '^[0-9]{1,3}$')) ;
ALTER TABLE GameMoves ADD CONSTRAINT move_notation_const  CHECK (REGEXP_LIKE(MoveNotation, '^[NBRQK]?[a-h]?[1-8]?[x-]?[a-h][1-8][NBRQ]?[+#]?|^(O-O|O-O-O)$'));
ALTER TABLE GameMoves ADD CONSTRAINT GameMoves_PK PRIMARY KEY ( MoveID ) ;


CREATE TABLE Player
  (
    PlayerID  NUMBER (10) NOT NULL ,
    FirstName VARCHAR2 (10) NOT NULL ,
    LastName  VARCHAR2 (10) NOT NULL ,
    Raiting   NUMBER (5)
  ) ;
ALTER TABLE Player ADD CONSTRAINT player_firstname_const CHECK ( REGEXP_LIKE(FirstName, '^[a-zA-Z]+$')) ;
ALTER TABLE Player ADD CONSTRAINT player_lastname_const CHECK ( REGEXP_LIKE(LastName, '^[a-zA-Z]+$')) ;
ALTER TABLE Player ADD CONSTRAINT player_raiting_const CHECK ( Raiting NOT LIKE '[^0-9]') ;
ALTER TABLE Player ADD CONSTRAINT Player_PK PRIMARY KEY ( PlayerID ) ;


CREATE TABLE PlayerDetails
  (
    DateOfBirth DATE ,
    Email       VARCHAR2 (30) ,
    PhoneNumber VARCHAR2 (10) ,
    PlayerID    NUMBER (10) NOT NULL
  ) ;
ALTER TABLE PlayerDetails ADD CONSTRAINT pdetails_email_const CHECK ( REGEXP_LIKE(Email, '[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}')) ;
ALTER TABLE PlayerDetails ADD CONSTRAINT pdetails_phone_const CHECK ( REGEXP_LIKE(PhoneNumber, '^07\d{8}$')) ;
CREATE UNIQUE INDEX PlayerDetails__IDX ON PlayerDetails ( PlayerID ASC ) ;
ALTER TABLE PlayerDetails ADD CONSTRAINT EMAIL_UNIQUE UNIQUE ( Email ) ;


CREATE TABLE Registration
  (
    RegistrationID NUMBER (10) NOT NULL ,
    PlayerID       NUMBER (10) NOT NULL ,
    TournamentID   NUMBER (10) NOT NULL
  ) ;
ALTER TABLE Registration ADD CONSTRAINT Registration_PK PRIMARY KEY ( RegistrationID ) ;
ALTER TABLE Registration ADD CONSTRAINT PlayerTournamentUN UNIQUE ( PlayerID , TournamentID ) ;


CREATE TABLE Tournament
  (
    TournamentID   NUMBER (10) NOT NULL ,
    TournamentName VARCHAR2 (30) NOT NULL ,
    StartDate      DATE ,
    EndDate        DATE ,
    Location       VARCHAR2 (20) ,
    Prize          NUMBER (7)
  ) ;
ALTER TABLE Tournament ADD CONSTRAINT tournament_name_const CHECK ( REGEXP_LIKE(TournamentName, '^[a-zA-Z0-9 ]{1,30}$')) ;
ALTER TABLE Tournament ADD CONSTRAINT tournament_duration_const CHECK ( EndDate-StartDate > 1) ;
ALTER TABLE Tournament ADD CONSTRAINT tournament_location_const CHECK ( REGEXP_LIKE(Location, '^[a-zA-Z ]{1,10}$')) ;
ALTER TABLE Tournament ADD CONSTRAINT tournament_prize_const CHECK ( REGEXP_LIKE(Prize, '^[0-9]{1,7}$')) ;
ALTER TABLE Tournament ADD CONSTRAINT Tournament_PK PRIMARY KEY ( TournamentID ) ;
ALTER TABLE Tournament ADD CONSTRAINT TOURNAMENT_NAME UNIQUE ( TournamentName ) ;


ALTER TABLE GameMoves ADD CONSTRAINT game_id_fk FOREIGN KEY ( GameID ) REFERENCES Game ( GameID ) ;

ALTER TABLE Game ADD CONSTRAINT loser_id_fk FOREIGN KEY ( LoserID ) REFERENCES Registration ( RegistrationID ) ;

ALTER TABLE PlayerDetails ADD CONSTRAINT player_details_fk FOREIGN KEY ( PlayerID ) REFERENCES Player ( PlayerID ) ;

ALTER TABLE Registration ADD CONSTRAINT player_id_fk FOREIGN KEY ( PlayerID ) REFERENCES Player ( PlayerID ) ;

ALTER TABLE Registration ADD CONSTRAINT tournament_id_fk FOREIGN KEY ( TournamentID ) REFERENCES Tournament ( TournamentID ) ;

ALTER TABLE Game ADD CONSTRAINT winner_id_fk FOREIGN KEY ( WinnerID ) REFERENCES Registration ( RegistrationID ) ;

CREATE SEQUENCE Game_GameID_SEQ START WITH 1 NOCACHE ORDER ;
CREATE OR REPLACE TRIGGER Game_GameID_TRG BEFORE
  INSERT ON Game FOR EACH ROW WHEN (NEW.GameID IS NULL) BEGIN :NEW.GameID := Game_GameID_SEQ.NEXTVAL;
END;
/

CREATE SEQUENCE GameMoves_MoveID_SEQ START WITH 1 NOCACHE ORDER ;
CREATE OR REPLACE TRIGGER GameMoves_MoveID_TRG BEFORE
  INSERT ON GameMoves FOR EACH ROW WHEN (NEW.MoveID IS NULL) BEGIN :NEW.MoveID := GameMoves_MoveID_SEQ.NEXTVAL;
END;
/

CREATE SEQUENCE Player_PlayerID_SEQ START WITH 1 NOCACHE ORDER ;
CREATE OR REPLACE TRIGGER Player_PlayerID_TRG BEFORE
  INSERT ON Player FOR EACH ROW WHEN (NEW.PlayerID IS NULL) BEGIN :NEW.PlayerID := Player_PlayerID_SEQ.NEXTVAL;
END;
/

CREATE SEQUENCE Registration_RegistrationID START WITH 1 NOCACHE ORDER ;
CREATE OR REPLACE TRIGGER Registration_RegistrationID BEFORE
  INSERT ON Registration FOR EACH ROW WHEN (NEW.RegistrationID IS NULL) BEGIN :NEW.RegistrationID := Registration_RegistrationID.NEXTVAL;
END;
/

CREATE SEQUENCE Tournament_TournamentID_SEQ START WITH 1 NOCACHE ORDER ;
CREATE OR REPLACE TRIGGER Tournament_TournamentID_TRG BEFORE
  INSERT ON Tournament FOR EACH ROW WHEN (NEW.TournamentID IS NULL) BEGIN :NEW.TournamentID := Tournament_TournamentID_SEQ.NEXTVAL;
END;
/


CREATE OR REPLACE TRIGGER CheckNegativeRating
BEFORE INSERT ON Game
FOR EACH ROW
DECLARE
    LoserPlayerRaiting NUMBER;
    WinnerPlayerRaiting NUMBER;
BEGIN
    -- Ensure only one row is returned for the loser
    SELECT p.Raiting INTO LoserPlayerRaiting
    FROM Registration r
    JOIN Player p ON r.PlayerID = :NEW.LoserID AND p.PlayerID = r.PlayerID
    WHERE ROWNUM = 1;  -- Add this condition to limit to one row

    -- Ensure only one row is returned for the winner
    SELECT p.Raiting INTO WinnerPlayerRaiting
    FROM Registration r
    JOIN Player p ON r.PlayerID = :NEW.WinnerID AND p.PlayerID = r.PlayerID
    WHERE ROWNUM = 1;  -- Add this condition to limit to one row

    -- Check if loser's rating doesn't go below 0
    IF (LoserPlayerRaiting - :NEW.RaitingInPlay) < 0 THEN
        RAISE_APPLICATION_ERROR(-20002, 'Loser''s rating cannot go below 0.');
    ELSE
        -- Update loser's rating
        UPDATE Player SET Raiting = LoserPlayerRaiting - :NEW.RaitingInPlay WHERE PlayerID = :NEW.LoserID;
        -- Update winner's rating
        UPDATE Player SET Raiting = WinnerPlayerRaiting + :NEW.RaitingInPlay WHERE PlayerID = :NEW.WinnerID;
    END IF;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        -- Handle the case where no records are found in the SELECT statements
        NULL;
END;
/

CREATE OR REPLACE TRIGGER CheckSameTournament
BEFORE INSERT ON Game
FOR EACH ROW
DECLARE
    WinnerPlayerTournamentID NUMBER;
    LoserPlayerTournamentID NUMBER;
BEGIN
    SELECT r.TournamentID INTO WinnerPlayerTournamentID
    FROM Registration r
    WHERE r.RegistrationID = :NEW.WinnerID;
    
    SELECT r.TournamentID INTO LoserPlayerTournamentID
    FROM Registration r
    WHERE r.RegistrationID = :NEW.LoserID;
    
    IF (WinnerPlayerTournamentID != LoserPlayerTournamentID) THEN
        RAISE_APPLICATION_ERROR(-20003, 'Players are not in the same tournament.');
    END IF;
END;
/
CREATE OR REPLACE TRIGGER CheckGameCount
BEFORE INSERT ON Game
FOR EACH ROW
DECLARE
    TotalGames NUMBER;
    TournamentIDValue NUMBER;
    MAX_1_8 CONSTANT NUMBER := 8;
    MAX_1_4 CONSTANT NUMBER := 4;
    MAX_1_2 CONSTANT NUMBER := 2;
    MAX_1 CONSTANT NUMBER := 1;
BEGIN
    SELECT DISTINCT r1.TournamentID INTO TournamentIDValue
    FROM Registration r1, Registration r2
    WHERE :NEW.WinnerID = r1.RegistrationID AND :NEW.LoserID = r2.RegistrationID and r1.TournamentID = r2.TournamentID;

    SELECT COUNT(*)
    INTO TotalGames
    FROM Registration
    WHERE TournamentID = TournamentIDValue;
    
    TotalGames := TotalGames / 2;

    CASE :NEW.RoundNumber
        WHEN '1/8' THEN
            IF TotalGames >= MAX_1_8 THEN
                RAISE_APPLICATION_ERROR(-20003, 'Maximum of ' || MAX_1_8 || ' "1/8" games already played.');
            END IF;
        WHEN '1/4' THEN
            IF TotalGames < MAX_1_8 THEN
                RAISE_APPLICATION_ERROR(-20004, '1/4 games cannot be played before all "1/8" games are played.');
            END IF;
            IF TotalGames >= (MAX_1_4 + MAX_1_8) THEN
                RAISE_APPLICATION_ERROR(-20005, 'Maximum of ' || MAX_1_4 || ' "1/4" games already played.');
            END IF;
        WHEN '1/2' THEN
            IF TotalGames < (MAX_1_4 + MAX_1_8) THEN
                RAISE_APPLICATION_ERROR(-20006, '1/2 games cannot be played before all "1/4" games are played.');
            END IF;
            IF TotalGames >= (MAX_1_2 + MAX_1_4 + MAX_1_8) THEN
                RAISE_APPLICATION_ERROR(-20007, 'Maximum of ' || MAX_1_2 || ' "1/2" games already played.');
            END IF;
        WHEN '1' THEN
            IF TotalGames < (MAX_1_2 + MAX_1_4 + MAX_1_8) THEN
                RAISE_APPLICATION_ERROR(-20008, '1 games cannot be played before all "1/2" games are played.');
            END IF;
            IF TotalGames >= (MAX_1+MAX_1_2 + MAX_1_4 + MAX_1_8) THEN
                RAISE_APPLICATION_ERROR(-20009, 'Maximum of ' || MAX_1 || ' "1" game already played.');
            END IF;
    END CASE;
END;
/



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                             6
-- CREATE INDEX                             1
-- ALTER TABLE                             27
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           5
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          5
-- CREATE MATERIALIZED VIEW                 0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
