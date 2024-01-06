import sys
from PyQt5.QtWidgets import (
    QTableWidget, QApplication, QMainWindow,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QLineEdit, QDialog, QDialogButtonBox, QFormLayout,
    QTableWidgetItem, QMessageBox, QProgressBar, QDateEdit, QCalendarWidget,
    QMenu, QAction, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDateTime, QDate
import cx_Oracle
import datetime

class ErrorWindow(QDialog):
    def __init__(self, error_message):
        super().__init__()

        self.setWindowTitle("Error")
        self.setGeometry(300, 300, 400, 200)

        # Error message label
        error_label = QLabel(error_message)

        # OK button to close the window
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.close)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(error_label)
        layout.addWidget(ok_button)

        self.setLayout(layout)

def show_error_window(error_message):
    error_window = ErrorWindow(error_message)
    error_window.exec_()

class AddGameWindow(QDialog):
    def __init__(self, db_connection, tournament_id):
        super().__init__()

        self.db_connection = db_connection
        self.tournament_id = tournament_id

        self.setWindowTitle("Add New Game")
        self.setGeometry(300, 300, 400, 200)

        winner_id_label = QLabel("Winner ID:")
        loser_id_label = QLabel("Loser ID:")
        round_number_label = QLabel("Round Number:")
        board_number_label = QLabel("Board Number:")
        rating_in_play_label = QLabel("Rating In Play:")

        self.winner_id_combobox = QComboBox(self)
        self.loser_id_combobox = QComboBox(self)
        self.populate_player_ids()

        self.round_number_combobox = QComboBox(self)
        self.round_number_combobox.addItems(["1/8", "1/4", "1/2", "1"])

        self.board_number_edit = QLineEdit()
        self.rating_in_play_edit = QLineEdit()

        add_game_button = QPushButton("Add New Game", self)
        add_game_button.clicked.connect(self.add_new_game)

        layout = QVBoxLayout()
        layout.addWidget(winner_id_label)
        layout.addWidget(self.winner_id_combobox)
        layout.addWidget(loser_id_label)
        layout.addWidget(self.loser_id_combobox)
        layout.addWidget(round_number_label)
        layout.addWidget(self.round_number_combobox)
        layout.addWidget(board_number_label)
        layout.addWidget(self.board_number_edit)
        layout.addWidget(rating_in_play_label)
        layout.addWidget(self.rating_in_play_edit)
        layout.addWidget(add_game_button)

        self.setLayout(layout)

    def populate_player_ids(self):
        cursor = self.db_connection.cursor()
        query = "SELECT RegistrationID FROM REGISTRATION WHERE TOURNAMENTID = :tournament_id"
        cursor.execute(query, {'tournament_id': self.tournament_id})
        registration_ids = cursor.fetchall()
        cursor.close()

        for registration_id in registration_ids:
            self.winner_id_combobox.addItem(str(registration_id[0]))
            self.loser_id_combobox.addItem(str(registration_id[0]))

    def add_new_game(self):
        winner_id = self.winner_id_combobox.currentText()
        loser_id = self.loser_id_combobox.currentText()
        round_number = self.round_number_combobox.currentText()
        board_number = self.board_number_edit.text()
        rating_in_play = self.rating_in_play_edit.text()

        if winner_id != loser_id:
            self.insert_new_game(winner_id, loser_id, round_number, board_number, rating_in_play)
            self.accept()
        else:
            show_error_window("Winner and Loser cannot be the same.")

    def insert_new_game(self, winner_id, loser_id, round_number, board_number, rating_in_play):
        try:
            cursor = self.db_connection.cursor()
            query = """
                INSERT INTO Game (WinnerID, LoserID, RoundNumber, BoardNumber, RatingInPlay)
                VALUES (:winner_id, :loser_id, :round_number, :board_number, :rating_in_play)
            """

            cursor.execute(query, {
                'winner_id': winner_id,
                'loser_id': loser_id,
                'round_number': round_number,
                'board_number': board_number,
                'rating_in_play': rating_in_play,
            })

            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            show_error_window(str(e))

class AddMovesWindow(QDialog):
    def __init__(self, db_connection, game_id):
        super().__init__()
        self.db_connection = db_connection
        self.game_id = game_id

        self.setWindowTitle("Add Moves")
        self.setGeometry(300, 300, 400, 150)

        move_notation_label = QLabel("Move Notation:")

        self.move_notation_edit = QLineEdit()

        add_moves_button = QPushButton("Add Moves", self)
        add_moves_button.clicked.connect(self.add_moves)

        layout = QVBoxLayout()
        layout.addWidget(move_notation_label)
        layout.addWidget(self.move_notation_edit)
        layout.addWidget(add_moves_button)

        self.setLayout(layout)

    def add_moves(self):
        move_notation = self.move_notation_edit.text()
        self.insert_move(move_notation)
        self.accept()

    def insert_move(self, move_notation):
        try:
            cursor = self.db_connection.cursor()
            query = """
                    INSERT INTO GameMoves (GameID, MoveNumber, MoveNotation) 
                     VALUES (:game_id, :move_number, :move_notation)
                     """
            move_number_query = "SELECT MAX(MoveNumber) FROM GameMoves WHERE GameID = :game_id"
            cursor.execute(move_number_query, {'game_id': self.game_id})
            max_move_number = cursor.fetchone()[0]
            move_number = max_move_number + 1 if max_move_number else 1

            cursor.execute(query, {'game_id': self.game_id, 'move_number': move_number, 'move_notation': move_notation})

            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            show_error_window(str(e))


class GameProgressionWindow(QDialog):
    def __init__(self, db_connection, game_id):
        super().__init__()
        self.db_connection = db_connection
        self.game_id = game_id

        self.setWindowTitle("Game Progression")
        self.setGeometry(300, 300, 600, 400)

        self.instructions_label = QLabel("Right click on a move to delete it", self)

        add_moves_button = QPushButton("Add Moves", self)
        add_moves_button.clicked.connect(self.add_moves)

        self.moves_table = QTableWidget(self)
        self.moves_table.setColumnCount(4)
        self.moves_table.setHorizontalHeaderLabels(["Move ID", "Game ID", "Move Number", "Move Notation"])

        moves_data = self.fetch_moves(game_id)
        self.populate_table(moves_data)

        layout = QVBoxLayout()
        layout.addWidget(self.instructions_label)
        layout.addWidget(add_moves_button)
        layout.addWidget(self.moves_table)

        self.setLayout(layout)

        # Set up context menu for the table
        self.moves_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.moves_table.customContextMenuRequested.connect(self.show_context_menu)

    def fetch_moves(self, game_id):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT
                    MoveID,
                    GameID,
                    MoveNumber,
                    MoveNotation
                FROM
                    GameMoves
                WHERE
                    GameID = :game_id
                ORDER BY
                    MoveID
            """

            cursor.execute(query, {'game_id': game_id})
            moves_data = cursor.fetchall()

            cursor.close()
            return moves_data
        except Exception as e:
            show_error_window(str(e))

    def populate_table(self, moves_data):
        self.moves_table.setRowCount(len(moves_data))

        for row_index, row_data in enumerate(moves_data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.moves_table.setItem(row_index, col_index, item)

    def add_moves(self):
        add_moves_window = AddMovesWindow(self.db_connection, self.game_id)
        add_moves_window.exec_()
        self.refresh_table()
    def show_context_menu(self, pos):
        context_menu = QMenu(self)

        delete_action = QAction("Delete Move", self)
        delete_action.triggered.connect(self.delete_move)

        context_menu.addAction(delete_action)
        context_menu.exec_(self.moves_table.mapToGlobal(pos))

    def delete_move(self):
        selected_row = self.moves_table.currentRow()

        if selected_row >= 0:
            move_id_item = self.moves_table.item(selected_row, 0)
            move_id = int(move_id_item.text())

            reply = QMessageBox.question(self, 'Delete Move', 'Are you sure you want to delete the move?', QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.execute_delete_query(move_id)
                self.moves_table.removeRow(selected_row)

    def execute_delete_query(self, move_id):
        try:
            cursor = self.db_connection.cursor()
            query = "DELETE FROM GameMoves WHERE MoveID = :move_id"
            cursor.execute(query, {'move_id': move_id})
            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            show_error_window(str(e))

    def refresh_table(self):
        moves_data = self.fetch_moves(self.game_id)
        self.populate_table(moves_data)

class ViewGamesWindow(QDialog):
    def __init__(self, tournament_id, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.tournament_id = tournament_id

        self.setWindowTitle("View Games")
        self.setGeometry(300, 300, 600, 400)

        info_label = QLabel("Double-click for checking game progression.", self)

        add_game_button = QPushButton("Add New Game", self)
        add_game_button.clicked.connect(self.add_new_game)

        self.games_table = QTableWidget(self)
        self.games_table.setColumnCount(6)
        self.games_table.setHorizontalHeaderLabels(
            ["Winner Name", "Loser Name", "Round Number", "Board Number", "Rating In Play", "Game ID"])

        self.games_table.itemDoubleClicked.connect(self.show_game_progression)

        self.games_data = self.fetch_games(tournament_id)
        self.populate_table(self.games_data)

        layout = QVBoxLayout()
        layout.addWidget(info_label)
        layout.addWidget(add_game_button)
        layout.addWidget(self.games_table)
        self.setLayout(layout)

    def fetch_games(self, tournament_id):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT
                    p1.FirstName || ' ' || p1.LastName,
                    p2.FirstName || ' ' || p2.LastName,
                    g.RoundNumber,
                    g.BoardNumber,
                    g.RaitingInPlay,
                    g.GameID
                FROM
                    Game g
                JOIN Registration r1 ON g.WinnerID = r1.RegistrationID
                JOIN Registration r2 ON g.LoserID = r2.RegistrationID
                JOIN Player p1 ON r1.PlayerID = p1.PlayerID
                JOIN Player p2 ON r2.PlayerID = p2.PlayerID
                WHERE
                    r1.TournamentID = :tournament_id
                ORDER BY
                    g.GameID
            """

            cursor.execute(query, {'tournament_id': tournament_id})
            games_data = cursor.fetchall()

            cursor.close()
            return games_data
        except Exception as e:
            show_error_window(str(e))

    def populate_table(self, games_data):

        self.games_table.setRowCount(len(games_data))

        for row_index, row_data in enumerate(games_data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.games_table.setItem(row_index, col_index, item)
                self.games_table.resizeColumnToContents(col_index)

    def add_new_game(self):
        add_game_window = AddGameWindow(self.db_connection, self.tournament_id)
        add_game_window.exec_()

    def show_game_progression(self, item):
        selected_row = item.row()
        game_id_item = self.games_table.item(selected_row, 5)
        selected_game_id = int(game_id_item.text())

        game_progression_window = GameProgressionWindow(self.db_connection, selected_game_id)
        game_progression_window.exec_()

class EditPlayerDetailsWindow(QDialog):
    def __init__(self, player_data, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.setWindowTitle("Edit Player Details")
        self.setGeometry(300, 300, 400, 200)

        dob_label = QLabel("Date of Birth:")
        self.dob_edit = QDateEdit()
        self.dob_edit.setDate(QDate.fromString(player_data[0].strftime('%d-%m-%Y'), 'dd-MM-yyyy'))

        email_label = QLabel("Email:")
        self.email_edit = QLineEdit(player_data[1])

        phone_label = QLabel("Phone Number:")
        self.phone_edit = QLineEdit(player_data[2])

        self.email_edit.setText(player_data[1])
        self.phone_edit.setText(player_data[2])

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow(dob_label, self.dob_edit)
        form_layout.addRow(email_label, self.email_edit)
        form_layout.addRow(phone_label, self.phone_edit)
        form_layout.addWidget(button_box)

        self.setLayout(form_layout)
        self.original_player_data = player_data

    def accept(self):
        edited_player_data = self.get_player_data()
        self.update_database(edited_player_data)
        super().accept()

    def update_database(self, edited_player_data):
        try:
            player_id = self.original_player_data[3]
            cursor = self.db_connection.cursor()
            query = """
                UPDATE PLAYERDETAILS
                SET DATEOFBIRTH = TO_DATE(:dob, 'DD-MM-YYYY'), EMAIL = :email, PHONENUMBER = :phone
                WHERE PLAYERID = :player_id
            """
            cursor.execute(query, {
                'dob': edited_player_data[0],
                'email': edited_player_data[1],
                'phone': edited_player_data[2],
                'player_id': player_id
            })
            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            show_error_window(str(e))
    def get_player_data(self):
        dob = self.dob_edit.date().toString('dd-MM-yyyy')
        email = self.email_edit.text()
        phone = self.phone_edit.text()

        return dob, email, phone

class PlayerDetailsWindowID(QDialog):
    def __init__(self, player_id, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.player_id = player_id
        self.setWindowTitle(f"Player Details - ID: {player_id}")
        self.setGeometry(300, 300, 400, 200)
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT * FROM PLAYERDETAILS WHERE PLAYERID = :id
            """
            cursor.execute(query, {'id': self.player_id})
            self.player_data = cursor.fetchone()
            cursor.close()
        except Exception as e:
            show_error_window(str(e))

        edit_button = QPushButton("Edit Player", self)
        edit_button.clicked.connect(self.edit_player_details)

        dob = self.player_data[0].strftime("%d-%m-%Y")
        date_of_birth_label = QLabel(f"Date of Birth: {dob}", self)
        email_label = QLabel(f"Email: {self.player_data[1]}", self)
        phone_number_label = QLabel(f"Phone number: {self.player_data[2]}", self)

        layout = QVBoxLayout()
        layout.addWidget(date_of_birth_label)
        layout.addWidget(email_label)
        layout.addWidget(phone_number_label)
        layout.addWidget(edit_button)
        self.setLayout(layout)

    def edit_player_details(self):
        edited_data = self.player_data
        edit_player_window = EditPlayerDetailsWindow(edited_data, self.db_connection)
        result = edit_player_window.exec_()

        if result == QDialog.Accepted:
            self.player_data = edit_player_window.get_player_data()
            self.update_displayed_data()

    def update_displayed_data(self):
        dob = self.player_data[0]
        QLabel(f"Date of Birth: {dob}", self)
        QLabel(f"Email: {self.player_data[1]}", self)
        QLabel(f"Phone number: {self.player_data[2]}", self)
class PlayerDetailsWindow(QDialog):
    def __init__(self, player_data, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.player_data = player_data
        self.setWindowTitle(f"Player Details - ID: {player_data[3]}")
        self.setGeometry(300, 300, 400, 200)

        edit_button = QPushButton("Edit Player", self)
        edit_button.clicked.connect(self.edit_player_details)

        dob = player_data[0].strftime("%d-%m-%Y")
        date_of_birth_label = QLabel(f"Date of Birth: {dob}", self)
        email_label = QLabel(f"Email: {player_data[1]}", self)
        phone_number_label = QLabel(f"Phone number: {player_data[2]}", self)

        layout = QVBoxLayout()
        layout.addWidget(date_of_birth_label)
        layout.addWidget(email_label)
        layout.addWidget(phone_number_label)
        layout.addWidget(edit_button)
        self.setLayout(layout)

    def edit_player_details(self):
        edited_data = self.player_data
        edit_player_window = EditPlayerDetailsWindow(edited_data, self.db_connection)
        result = edit_player_window.exec_()

        if result == QDialog.Accepted:
            self.player_data = edit_player_window.get_player_data()
            self.update_displayed_data()

    def update_displayed_data(self):
        dob = self.player_data[0]
        QLabel(f"Date of Birth: {dob}", self)
        QLabel(f"Email: {self.player_data[1]}", self)
        QLabel(f"Phone number: {self.player_data[2]}", self)


class AddRegistrationWindow(QDialog):
    def __init__(self, tournament_id, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.tournament_id = tournament_id
        self.setWindowTitle("Add Registration")
        self.setGeometry(300, 300, 300, 150)

        player_id_label = QLabel("Player ID:")
        self.player_id_combobox = QComboBox(self)
        self.populate_player_ids()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        form_layout = QVBoxLayout()
        form_layout.addWidget(player_id_label)
        form_layout.addWidget(self.player_id_combobox)
        form_layout.addWidget(button_box)

        self.setLayout(form_layout)



    def populate_player_ids(self):
        cursor = self.db_connection.cursor()
        query = "SELECT PLAYERID FROM PLAYER"
        cursor.execute(query)
        player_ids = cursor.fetchall()
        cursor.close()

        for player_id in player_ids:
            self.player_id_combobox.addItem(str(player_id[0]))

    def accept(self):
        player_id = self.player_id_edit.text()
        self.insert_registration(player_id)
        super().accept()

    def validate_and_accept(self):
        player_id = self.player_id_combobox.currentText()

        if not self.is_player_registered(player_id):
            self.insert_registration(player_id)
            super().accept()
        else:
            QMessageBox.warning(self, "Warning", "Player is already registered in the tournament.", QMessageBox.Ok)

    def is_player_registered(self, player_id):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM REGISTRATION WHERE PLAYERID = :player_id AND TOURNAMENTID = :tournament_id"
        cursor.execute(query, {'player_id': player_id, 'tournament_id': self.tournament_id})
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def insert_registration(self, player_id):
        cursor = self.db_connection.cursor()
        query = "INSERT INTO REGISTRATION (PLAYERID, TOURNAMENTID) VALUES (:player_id, :tournament_id)"
        cursor.execute(query, {'player_id': player_id, 'tournament_id': self.tournament_id})
        self.db_connection.commit()
        cursor.close()


class RegistrationsWindow(QDialog):
    def __init__(self, tournament_id, db_connection):
        super().__init__()
        self.setWindowTitle(f"Registrations for Tournament {tournament_id}")
        self.setGeometry(300, 300, 600, 400)
        self.tournament_id = tournament_id
        self.db_connection = db_connection

        self.registrations_table = QTableWidget(self)
        self.registrations_table.setColumnCount(2)
        self.registrations_table.setHorizontalHeaderLabels(["Registration ID", "Player Name"])
        self.registrations_table.itemDoubleClicked.connect(self.view_player_details)

        view_label = QLabel("Double click on the registration to view player details", self)
        view_label.setAlignment(Qt.AlignCenter)

        add_registration_button = QPushButton("Add Registration", self)
        add_registration_button.clicked.connect(self.add_registration)

        layout = QVBoxLayout()
        layout.addWidget(view_label)
        layout.addWidget(self.registrations_table)
        layout.addWidget(add_registration_button)

        self.setLayout(layout)
        self.populate_table()

    def populate_table(self):
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT REGISTRATIONID, FIRSTNAME || ' ' || LASTNAME
                FROM Registration r, Player p
                WHERE r.TournamentID = :tournament_id AND p.PlayerID = r.PlayerID
                """
            cursor.execute(query, {'tournament_id': self.tournament_id})
            registrations_data = cursor.fetchall()
            self.registrations_table.setRowCount(len(registrations_data))
            for row_index, row_data in enumerate(registrations_data):
                for col_index, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.registrations_table.setItem(row_index, col_index, item)
            cursor.close()
            self.registrations_table.resizeColumnsToContents()
        except Exception as e:
            show_error_window(str(e))
    def view_player_details(self, item):
        reg_id = self.registrations_table.item(item.row(), 0).text()
        cursor = self.db_connection.cursor()
        query = "SELECT PLAYERID FROM REGISTRATION WHERE REGISTRATIONID = :registration_id"
        cursor.execute(query, {'registration_id': reg_id})
        player_id = cursor.fetchone()
        cursor.close()

        cursor = self.db_connection.cursor()
        query = "SELECT * FROM PLAYERDETAILS WHERE PLAYERID = :player_id"
        cursor.execute(query, {'player_id': player_id[0]})
        player_data = cursor.fetchone()
        cursor.close()

        player_details_window = PlayerDetailsWindow(player_data, self.db_connection)
        player_details_window.exec_()

    def add_registration(self):
        add_registration_window = AddRegistrationWindow(self.tournament_id, self.db_connection)
        result = add_registration_window.exec_()

        if result == QDialog.Accepted:
            self.populate_table()


class EditTournamentWindow(QDialog):
    def __init__(self, tournament_data):
        super().__init__()

        self.setWindowTitle("Edit Tournament")
        self.setGeometry(300, 300, 400, 200)

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit(tournament_data[1])

        self.start_date_label = QLabel("Start Date:")
        self.start_date_edit = QLineEdit(tournament_data[2].strftime("%d-%m-%Y"))

        self.end_date_label = QLabel("End Date:")
        self.end_date_edit = QLineEdit(tournament_data[3].strftime("%d-%m-%Y"))

        self.location_label = QLabel("Location:")
        self.location_edit = QLineEdit(tournament_data[4])

        self.prize_label = QLabel("Prize:")
        self.prize_edit = QLineEdit(str(tournament_data[5]))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow(self.name_label, self.name_edit)
        form_layout.addRow(self.start_date_label, self.start_date_edit)
        form_layout.addRow(self.end_date_label, self.end_date_edit)
        form_layout.addRow(self.location_label, self.location_edit)
        form_layout.addRow(self.prize_label, self.prize_edit)
        form_layout.addWidget(button_box)

        self.setLayout(form_layout)

    def get_tournament_data(self):
        name = self.name_edit.text()
        start_date = self.start_date_edit.text()
        end_date = self.end_date_edit.text()
        location = self.location_edit.text()
        prize = self.prize_edit.text()

        return name, start_date, end_date, location, prize


class ViewTournamentWindow(QDialog):
    def __init__(self, tournament_id, db_connection):
        super().__init__()

        self.setWindowTitle(f"View Tournament {tournament_id}")
        self.setGeometry(300, 300, 300, 200)

        self.tournament_id = tournament_id
        self.db_connection = db_connection

        view_registrations_button = QPushButton("View Registrations", self)
        view_registrations_button.clicked.connect(self.view_registrations)

        view_games_button = QPushButton("View Games", self)
        view_games_button.clicked.connect(self.view_games)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(view_registrations_button)
        buttons_layout.addWidget(view_games_button)

        self.setLayout(buttons_layout)

    def view_registrations(self):
        registrations_window = RegistrationsWindow(self.tournament_id, self.db_connection)
        registrations_window.exec_()

    def view_games(self):
        view_games_window = ViewGamesWindow(self.tournament_id, self.db_connection)
        view_games_window.exec_()


class AddTournamentWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adding Tournament")
        self.setGeometry(300, 300, 400, 200)

        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()

        self.start_date_label = QLabel("Start Date:")
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())

        self.end_date_label = QLabel("End Date:")
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate().addDays(7))

        self.location_label = QLabel("Location:")
        self.location_edit = QLineEdit()

        self.prize_label = QLabel("Prize:")
        self.prize_edit = QLineEdit()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow(self.name_label, self.name_edit)
        form_layout.addRow(self.start_date_label, self.start_date_edit)
        form_layout.addRow(self.end_date_label, self.end_date_edit)
        form_layout.addRow(self.location_label, self.location_edit)
        form_layout.addRow(self.prize_label, self.prize_edit)
        form_layout.addWidget(button_box)

        self.setLayout(form_layout)

    def get_tournament_data(self):
        name = self.name_edit.text()
        start_date = self.start_date_edit.date().toString(Qt.ISODate)
        end_date = self.end_date_edit.date().toString(Qt.ISODate)
        location = self.location_edit.text()
        prize = self.prize_edit.text()

        return name, start_date, end_date, location, prize


class TournamentsWindow(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()

        self.setWindowTitle("Tournament Manager")
        self.setGeometry(100, 100, 800, 600)
        self.db_connection = db_connection

        title_label = QLabel("TOURNAMENT MANAGER", self)
        title_label.setAlignment(Qt.AlignCenter)

        add_button = QPushButton("Add Tournament", self)
        add_button.clicked.connect(self.open_add_tournament_window)

        view_label = QLabel("Double click on the tournament to view it", self)
        view_label.setAlignment(Qt.AlignCenter)
        edit_label = QLabel("Right click on the tournament to edit it", self)
        edit_label.setAlignment(Qt.AlignCenter)

        self.tournaments_table = QTableWidget(self)
        self.tournaments_table.setColumnCount(6)
        self.tournaments_table.setHorizontalHeaderLabels(["ID", "Name", "Start Date", "End Date", "Location", "Prize"])

        self.tournaments_table.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.tournaments_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tournaments_table.customContextMenuRequested.connect(self.show_context_menu)

        self.read_table(self.db_connection)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_button)
        buttons_layout.addStretch()

        central_layout = QVBoxLayout()
        central_layout.addWidget(title_label)
        central_layout.addWidget(view_label)
        central_layout.addWidget(edit_label)
        central_layout.addLayout(buttons_layout)
        central_layout.addWidget(self.tournaments_table)

        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def read_table(self, db_connection):
        cursor = db_connection.cursor()
        query = "SELECT * FROM Tournament ORDER BY TOURNAMENTID"
        cursor.execute(query)
        tournaments_data = cursor.fetchall()
        self.tournaments_table.setRowCount(len(tournaments_data))

        for row_index, row_data in enumerate(tournaments_data):
            for col_index, col_data in enumerate(row_data):
                if isinstance(col_data, datetime.datetime):
                    col_data = col_data.strftime("%d-%m-%Y")
                item = QTableWidgetItem(str(col_data))
                self.tournaments_table.setItem(row_index, col_index, item)
        self.tournaments_table.resizeColumnsToContents()
        cursor.close()

    def populate_table(self, db_connection, tournament_data):
        try:
            cursor = db_connection.cursor()
            query = """
                    INSERT INTO Tournament (TOURNAMENTNAME, STARTDATE, ENDDATE, LOCATION, PRIZE)
                    VALUES (:name, TO_DATE(:start_date, 'YYYY-MM-DD'), TO_DATE(:end_date, 'YYYY-MM-DD'), :location, :prize)
                    """
            cursor.execute(query,
                           {'name': tournament_data[0], 'start_date': tournament_data[1], 'end_date': tournament_data[2],
                            'location': tournament_data[3], 'prize': tournament_data[4]})
            self.db_connection.commit()
            self.read_table(db_connection)
            cursor.close()
        except Exception as e:
            show_error_window(str(e))

    def open_add_tournament_window(self):
        add_tournament_window = AddTournamentWindow()
        result = add_tournament_window.exec_()

        if result == QDialog.Accepted:
            tournament_data = add_tournament_window.get_tournament_data()
            self.populate_table(self.db_connection, tournament_data)

    def on_item_double_clicked(self, item):
        tournament_id = self.tournaments_table.item(item.row(), 0).text()

        view_tournament_window = ViewTournamentWindow(tournament_id, self.db_connection)
        view_tournament_window.exec_()

    def show_context_menu(self, position):
        item = self.tournaments_table.itemAt(position)
        if item:
            menu = QMenu(self)
            edit_action = menu.addAction("Edit Tournament")
            edit_action.triggered.connect(lambda: self.edit_tournament(item.row()))
            menu.exec_(self.tournaments_table.viewport().mapToGlobal(position))

    def edit_tournament(self, row):
        tournament_id = self.tournaments_table.item(row, 0).text()
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM Tournament WHERE TOURNAMENTID = :id"
        cursor.execute(query, {'id': tournament_id})
        tournament_data = cursor.fetchone()
        cursor.close()

        edit_tournament_window = EditTournamentWindow(tournament_data)
        result = edit_tournament_window.exec_()

        if result == QDialog.Accepted:
            new_data = edit_tournament_window.get_tournament_data()
            self.update_tournament(tournament_id, new_data)

    def update_tournament(self, tournament_id, new_data):
        try:
            cursor = self.db_connection.cursor()
            query = """
            UPDATE Tournament
            SET TOURNAMENTNAME = :name, STARTDATE = TO_DATE(:start_date, 'DD-MM-YYYY'),
                ENDDATE = TO_DATE(:end_date, 'DD-MM-YYYY'), LOCATION = :location, PRIZE = :prize
            WHERE TOURNAMENTID = :id
            """

            cursor.execute(query,
                           {'id': tournament_id, 'name': new_data[0], 'start_date': new_data[1], 'end_date': new_data[2],
                            'location': new_data[3], 'prize': new_data[4]})
            self.db_connection.commit()
            cursor.close()
            self.read_table(self.db_connection)
        except Exception as e:
            show_error_window(str(e))


class AddPlayerWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adding Player")
        self.setGeometry(300, 300, 400, 200)

        self.first_name_label = QLabel("First Name:")
        self.first_name_edit = QLineEdit()

        self.last_name_label = QLabel("Last Name:")
        self.last_name_edit = QLineEdit()

        self.raiting_label = QLabel("Raiting:")
        self.raiting_edit = QLineEdit()

        self.dob_label = QLabel("Date of Birth:")
        self.dob_edit = QDateEdit()
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setDate(QDate.currentDate())

        self.email_label = QLabel("Email:")
        self.email_edit = QLineEdit()

        self.phone_number_label = QLabel("Phone Number:")
        self.phone_number_edit = QLineEdit()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        form_layout = QFormLayout()
        form_layout.addRow(self.first_name_label, self.first_name_edit)
        form_layout.addRow(self.last_name_label, self.last_name_edit)
        form_layout.addRow(self.raiting_label, self.raiting_edit)
        form_layout.addRow(self.dob_label, self.dob_edit)
        form_layout.addRow(self.email_label, self.email_edit)
        form_layout.addRow(self.phone_number_label, self.phone_number_edit)
        form_layout.addWidget(button_box)

        self.setLayout(form_layout)

    def get_player_data(self):
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        raiting = self.raiting_edit.text()
        dob = self.dob_edit.date().toString(Qt.ISODate)
        email = self.email_edit.text()
        phone = self.phone_number_edit.text()

        return first_name, last_name, raiting, dob, email, phone


class ViewTournamentsWindow(QDialog):
    def __init__(self, tournament_data, player_id):
        super().__init__()

        self.setWindowTitle(f"Tournaments for player {player_id}")
        self.setGeometry(300, 300, 400, 200)
        self.tournaments_table = QTableWidget()
        self.tournaments_table.setColumnCount(1)
        self.tournaments_table.setHorizontalHeaderLabels(["Tournament Name"])
        self.populate_table(tournament_data)

        layout = QVBoxLayout()
        layout.addWidget(self.tournaments_table)
        self.setLayout(layout)

    def populate_table(self, tournament_data):
        self.tournaments_table.setRowCount(len(tournament_data))

        for row_index, tournament_name in enumerate(tournament_data):
            item = QTableWidgetItem(tournament_name)
            self.tournaments_table.setItem(row_index, 0, item)
            self.tournaments_table.resizeColumnsToContents()


class PlayersWindow(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.setWindowTitle("Players Window")
        self.setGeometry(100, 100, 800, 600)

        self.label1 = QLabel("Double-click to view player details")
        self.label2 = QLabel("Right-click to view player tournaments")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)

        self.add_player_button = QPushButton("Add Player")
        self.add_player_button.clicked.connect(self.open_add_player_window)

        self.players_table = QTableWidget()
        self.players_table.setColumnCount(3)
        self.players_table.setHorizontalHeaderLabels(["First Name", "Last Name", "Rating"])

        self.players_table.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.players_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.players_table.customContextMenuRequested.connect(self.show_context_menu)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.add_player_button)
        layout.addWidget(self.players_table)

        self.setLayout(layout)
        self.read_table(self.db_connection)

    def read_table(self, db_connection):
        cursor = db_connection.cursor()
        query = "SELECT * FROM Player ORDER BY PlayerID"
        cursor.execute(query)
        players_data = cursor.fetchall()
        self.players_table.setRowCount(len(players_data))

        for row_index, row_data in enumerate(players_data):
            for col_index, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.players_table.setItem(row_index, col_index, item)
        self.players_table.resizeColumnsToContents()
        cursor.close()

    def populate_table(self, db_connection, player_data):
        try:
            cursor = db_connection.cursor()
            query = """
                    INSERT INTO Player (FIRSTNAME, LASTNAME, RAITING)
                    VALUES (:first_name, :last_name, :raiting)
                    """
            cursor.execute(query, {'first_name': player_data[0], 'last_name': player_data[1], 'raiting': player_data[2]})
            self.db_connection.commit()
            self.read_table(db_connection)
            cursor.close()
        except Exception as e:
            show_error_window(str(e))

        try:
            cursor = db_connection.cursor()
            query = """
                    SELECT PLAYERID FROM PLAYER WHERE FIRSTNAME = :first_name AND LASTNAME = :last_name
                    """
            cursor.execute(query, {'first_name': player_data[0], 'last_name': player_data[1]})
            player_id = cursor.fetchone()
            cursor.close()
        except Exception as e:
            show_error_window(str(e))

        try:
            cursor = db_connection.cursor()
            query = """
                    INSERT INTO PlayerDetails (DATEOFBIRTH, EMAIL, PHONENUMBER, PLAYERID)
                    VALUES (TO_DATE(:dob, 'YYYY-MM-DD'), :email, :phone, :player_id)
                    """
            cursor.execute(query, {'dob': player_data[3], 'email': player_data[4], 'phone': player_data[5],
                                   'player_id': player_id[0]})
            self.db_connection.commit()
            self.read_table(db_connection)
            cursor.close()
        except Exception as e:
            show_error_window(str(e))


    def open_add_player_window(self):
        add_player_window = AddPlayerWindow()
        result = add_player_window.exec_()

        if result == QDialog.Accepted:
            player_data = add_player_window.get_player_data()
            self.populate_table(self.db_connection, player_data)

    def on_item_double_clicked(self, item):
        player_id = self.players_table.item(item.row(), 0).text()
        view_player_window = PlayerDetailsWindowID(player_id, self.db_connection)
        view_player_window.exec_()

    def show_context_menu(self, position):
        item = self.players_table.itemAt(position)
        if item:
            menu = QMenu(self)
            edit_action = menu.addAction("View Player Tournaments")
            edit_action.triggered.connect(lambda: self.view_tournaments(item.row()))
            menu.exec_(self.players_table.viewport().mapToGlobal(position))

    def view_tournaments(self, row):
        try:
            player_id = self.players_table.item(row, 0).text()
            cursor = self.db_connection.cursor()
            query = """
                    SELECT TOURNAMENTNAME 
                    FROM TOURNAMENT T, REGISTRATION R 
                    WHERE T.TOURNAMENTID = R.TOURNAMENTID AND R.PLAYERID = :id
                     """
            cursor.execute(query, {'id': player_id})
            tournament_data = cursor.fetchall()
            tournament_list = []
            for tournament in tournament_data:
                tournament_list += tournament

            cursor.close()
            view_tournament_window = ViewTournamentsWindow(tournament_list, player_id)
            view_tournament_window.exec_()
        except Exception as e:
            show_error_window(str(e))


class ChessTournamentManager(QMainWindow):
    def __init__(self, db_connection):
        super().__init__()

        self.setWindowTitle("Chess Tournament Manager")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.logo_label = QLabel(self)
        self.logo_label.setPixmap(QPixmap("chess.gif"))
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.manage_tournaments_button = QPushButton("Manage Tournaments", self)
        self.manage_tournaments_button.clicked.connect(self.open_tournaments_window)

        self.manage_players_button = QPushButton("Manage Players", self)
        self.manage_players_button.clicked.connect(self.open_players_window)

        self.db_connection = db_connection
        self.tournaments_window = None
        self.player_window = None

        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addStretch(1)
        layout.addWidget(self.manage_tournaments_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.manage_players_button, alignment=Qt.AlignCenter)
        layout.addStretch(2)

        self.central_widget.setLayout(layout)

    def open_tournaments_window(self):
        if not self.tournaments_window or not self.tournaments_window.isVisible():
            self.tournaments_window = TournamentsWindow(self.db_connection)
            self.tournaments_window.show()

    def open_players_window(self):
        if not self.player_window or not self.player_window.isVisible():
            self.player_window = PlayersWindow(self.db_connection)
            self.player_window.show()


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 100)

        self.username_label = QLabel("Username:")
        self.username_edit = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow(self.username_label, self.username_edit)
        layout.addRow(self.password_label, self.password_edit)
        layout.addWidget(button_box)

        self.setLayout(layout)


def get_user_credentials():
    login_dialog = LoginWindow()
    result = login_dialog.exec_()

    if result == QDialog.Accepted:
        user = login_dialog.username_edit.text()
        passw = login_dialog.password_edit.text()
        return user, passw
    else:
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    username, password = get_user_credentials()

    host = "bd-dc.cs.tuiasi.ro"
    port = 1539
    service_name = "orcl"

    dsn = cx_Oracle.makedsn(host, port, service_name)
    connection = cx_Oracle.connect(username, password, dsn)

    main_window = ChessTournamentManager(connection)
    main_window.destroyed.connect(lambda: connection.close())
    main_window.show()

    sys.exit(app.exec_())
