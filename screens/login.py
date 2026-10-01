import sys
import os
import hashlib

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)

from PySide6.QtCore import Qt

from database.connection import get_connection


class LoginWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.dashboard_window = None

        self.setWindowTitle(
            "Karatina Sub-County Hospital - Login"
        )

        self.setMinimumSize(
            500,
            450
        )

        self.setup_ui()

    # ==========================================================
    # USER INTERFACE
    # ==========================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout()

        central.setLayout(
            layout
        )

        layout.setContentsMargins(
            60,
            50,
            60,
            50
        )

        layout.setSpacing(
            15
        )

        # ======================================================
        # HOSPITAL NAME
        # ======================================================

        hospital = QLabel(
            "KARATINA SUB-COUNTY HOSPITAL"
        )

        hospital.setAlignment(
            Qt.AlignCenter
        )

        hospital.setStyleSheet(
            """
            QLabel {
                font-size: 23px;
                font-weight: bold;
                padding: 10px;
            }
            """
        )

        layout.addWidget(
            hospital
        )

        # ======================================================
        # SYSTEM NAME
        # ======================================================

        system_name = QLabel(
            "Medical Equipment Inventory System"
        )

        system_name.setAlignment(
            Qt.AlignCenter
        )

        system_name.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #555555;
                padding-bottom: 25px;
            }
            """
        )

        layout.addWidget(
            system_name
        )

        # ======================================================
        # USERNAME
        # ======================================================

        username_label = QLabel(
            "Username"
        )

        self.username_input = QLineEdit()

        self.username_input.setPlaceholderText(
            "Enter your username"
        )

        self.username_input.setMinimumHeight(
            42
        )

        layout.addWidget(
            username_label
        )

        layout.addWidget(
            self.username_input
        )

        # ======================================================
        # PASSWORD
        # ======================================================

        password_label = QLabel(
            "Password"
        )

        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Enter your password"
        )

        self.password_input.setEchoMode(
            QLineEdit.Password
        )

        self.password_input.setMinimumHeight(
            42
        )

        self.password_input.returnPressed.connect(
            self.login
        )

        layout.addWidget(
            password_label
        )

        layout.addWidget(
            self.password_input
        )

        # ======================================================
        # LOGIN BUTTON
        # ======================================================

        login_button = QPushButton(
            "LOGIN"
        )

        login_button.setMinimumHeight(
            48
        )

        login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }
            """
        )

        login_button.clicked.connect(
            self.login
        )

        layout.addWidget(
            login_button
        )

        # ======================================================
        # STATUS MESSAGE
        # ======================================================

        self.status_label = QLabel(
            ""
        )

        self.status_label.setAlignment(
            Qt.AlignCenter
        )

        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #dc2626;
                font-weight: bold;
                padding-top: 10px;
            }
            """
        )

        layout.addWidget(
            self.status_label
        )

        layout.addStretch()

    # ==========================================================
    # LOGIN
    # ==========================================================

    def login(self):

        username = (
            self.username_input
            .text()
            .strip()
        )

        password = (
            self.password_input
            .text()
        )

        if not username:

            self.status_label.setText(
                "Please enter your username."
            )

            self.username_input.setFocus()

            return

        if not password:

            self.status_label.setText(
                "Please enter your password."
            )

            self.password_input.setFocus()

            return

        connection = get_connection()

        if not connection:

            QMessageBox.critical(
                self,
                "Database Error",
                "Could not connect to the database."
            )

            return

        cursor = None

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    user_id,
                    full_name,
                    username,
                    password_hash,
                    role
                FROM system_users
                WHERE username = %s
                AND is_active = 1
                LIMIT 1
                """,
                (username,)
            )

            user = cursor.fetchone()

            if not user:

                self.status_label.setText(
                    "Invalid username or password."
                )

                self.password_input.clear()

                return

            user_id = user[0]
            full_name = user[1]
            database_username = user[2]
            stored_password = user[3]
            role = user[4]

            # ==================================================
            # CHECK PASSWORD
            # ==================================================

            password_hash = hashlib.sha256(
                password.encode("utf-8")
            ).hexdigest()

            password_valid = False

            if stored_password == password_hash:

                password_valid = True

            elif stored_password == password:

                password_valid = True

            if not password_valid:

                self.status_label.setText(
                    "Invalid username or password."
                )

                self.password_input.clear()

                return

            # ==================================================
            # OPEN DASHBOARD
            # ==================================================

            from screens.dashboard import DashboardWindow

            self.dashboard_window = DashboardWindow(
                user_id=user_id,
                username=database_username,
                role=role
            )

            self.dashboard_window.show()

            self.close()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Login Error",
                "Could not complete login:\n\n"
                + str(error)
            )

        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass


# ==========================================================
# STANDALONE TEST
# ==========================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    window = LoginWindow()

    window.show()

    sys.exit(
        app.exec()
    )