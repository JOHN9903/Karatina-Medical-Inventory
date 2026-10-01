import sys
import os

# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------
# PYQT
# ---------------------------------------------------------
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QFrame,
)

from PySide6.QtCore import Qt


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
from database.connection import get_connection


# =========================================================
# DASHBOARD WINDOW
# =========================================================
class DashboardWindow(QMainWindow):

    def __init__(
        self,
        user_id=1,
        username="Admin",
        role="Viewer"
    ):

        super().__init__()

        self.user_id = user_id
        self.username = username
        self.role = role

        self.inventory_window = None
        self.maintenance_window = None
        self.transfer_window = None

        self.setWindowTitle(
            "Karatina Medical Inventory Management System"
        )

        self.setMinimumSize(1200, 750)

        self.setup_ui()
        self.load_statistics()

    # =====================================================
    # MAIN UI
    # =====================================================
    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(0)

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------
        header = QFrame()

        header.setStyleSheet("""
            QFrame {
                background-color: #0B5D4B;
            }
        """)

        header_layout = QHBoxLayout(header)

        header_layout.setContentsMargins(
            30,
            20,
            30,
            20
        )

        # Hospital information
        hospital_layout = QVBoxLayout()

        hospital_name = QLabel(
            "KARATINA SUB-COUNTY HOSPITAL"
        )

        hospital_name.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
            }
        """)

        system_name = QLabel(
            "Medical Equipment Inventory Management System"
        )

        system_name.setStyleSheet("""
            QLabel {
                color: #D9F2EA;
                font-size: 13px;
            }
        """)

        hospital_layout.addWidget(
            hospital_name
        )

        hospital_layout.addWidget(
            system_name
        )

        header_layout.addLayout(
            hospital_layout
        )

        header_layout.addStretch()

        # User information
        user_box = QFrame()

        user_box.setStyleSheet("""
            QFrame {
                background-color: #084638;
                border-radius: 8px;
            }
        """)

        user_layout = QVBoxLayout(user_box)

        user_layout.setContentsMargins(
            15,
            8,
            15,
            8
        )

        logged_in_label = QLabel(
            f"Logged in as: {self.username}"
        )

        logged_in_label.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 13px;
            }
        """)

        role_label = QLabel(
            f"Role: {self.role}"
        )

        role_label.setStyleSheet("""
            QLabel {
                color: #C7E8DE;
                font-size: 12px;
            }
        """)

        user_layout.addWidget(
            logged_in_label
        )

        user_layout.addWidget(
            role_label
        )

        header_layout.addWidget(
            user_box
        )

        main_layout.addWidget(
            header
        )

        # -------------------------------------------------
        # CONTENT AREA
        # -------------------------------------------------
        content = QWidget()

        content_layout = QVBoxLayout(content)

        content_layout.setContentsMargins(
            30,
            25,
            30,
            20
        )

        content_layout.setSpacing(20)

        main_layout.addWidget(
            content
        )

        # -------------------------------------------------
        # WELCOME SECTION
        # -------------------------------------------------
        welcome_layout = QHBoxLayout()

        welcome_text_layout = QVBoxLayout()

        welcome_label = QLabel(
            f"Welcome, {self.username} 👋"
        )

        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
                color: #1F2937;
            }
        """)

        description_label = QLabel(
            "Manage medical equipment, maintenance activities "
            "and equipment transfers from one place."
        )

        description_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 14px;
            }
        """)

        welcome_text_layout.addWidget(
            welcome_label
        )

        welcome_text_layout.addWidget(
            description_label
        )

        welcome_layout.addLayout(
            welcome_text_layout
        )

        welcome_layout.addStretch()

        refresh_button = QPushButton(
            "↻  Refresh Dashboard"
        )

        refresh_button.setMinimumHeight(40)

        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #0B5D4B;
                border: 1px solid #0B5D4B;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #EAF6F2;
            }
        """)

        refresh_button.clicked.connect(
            self.load_statistics
        )

        welcome_layout.addWidget(
            refresh_button
        )

        content_layout.addLayout(
            welcome_layout
        )

        # -------------------------------------------------
        # MODULE TITLE
        # -------------------------------------------------
        modules_title = QLabel(
            "System Modules"
        )

        modules_title.setStyleSheet("""
            QLabel {
                font-size: 19px;
                font-weight: bold;
                color: #1F2937;
                margin-top: 5px;
            }
        """)

        content_layout.addWidget(
            modules_title
        )

        # -------------------------------------------------
        # MODULE CARDS
        # -------------------------------------------------
        modules_layout = QHBoxLayout()

        modules_layout.setSpacing(18)

        # Inventory
        inventory_card = self.create_module_card(
            icon="🏥",
            title="Medical Equipment Inventory",
            description=(
                "View, add, manage and export "
                "medical equipment inventory."
            ),
            accent="#0B5D4B"
        )

        inventory_card.mousePressEvent = (
            lambda event: self.open_inventory()
        )

        modules_layout.addWidget(
            inventory_card
        )

        # Maintenance
        maintenance_card = self.create_module_card(
            icon="🔧",
            title="Equipment Maintenance",
            description=(
                "Record maintenance, repairs, faults "
                "and equipment service history."
            ),
            accent="#2563EB"
        )

        maintenance_card.mousePressEvent = (
            lambda event: self.open_maintenance()
        )

        modules_layout.addWidget(
            maintenance_card
        )

        # Transfers
        transfer_card = self.create_module_card(
            icon="🔄",
            title="Equipment Transfers",
            description=(
                "Manage department transfers, "
                "external transfers and donations."
            ),
            accent="#7C3AED"
        )

        transfer_card.mousePressEvent = (
            lambda event: self.open_transfers()
        )

        modules_layout.addWidget(
            transfer_card
        )

        content_layout.addLayout(
            modules_layout
        )

        # -------------------------------------------------
        # OVERVIEW TITLE
        # -------------------------------------------------
        overview_title = QLabel(
            "Equipment Overview"
        )

        overview_title.setStyleSheet("""
            QLabel {
                font-size: 19px;
                font-weight: bold;
                color: #1F2937;
                margin-top: 5px;
            }
        """)

        content_layout.addWidget(
            overview_title
        )

        # -------------------------------------------------
        # STATISTICS GRID
        # -------------------------------------------------
        stats_grid = QGridLayout()

        stats_grid.setHorizontalSpacing(15)
        stats_grid.setVerticalSpacing(15)

        # Create statistic cards
        self.total_card, self.total_value = (
            self.create_stat_card(
                "TOTAL EQUIPMENT",
                "0",
                "#0B5D4B"
            )
        )

        self.functional_card, self.functional_value = (
            self.create_stat_card(
                "FUNCTIONAL",
                "0",
                "#16A34A"
            )
        )

        self.nonfunctional_card, self.nonfunctional_value = (
            self.create_stat_card(
                "NON-FUNCTIONAL",
                "0",
                "#DC2626"
            )
        )

        self.maintenance_card, self.maintenance_value = (
            self.create_stat_card(
                "UNDER MAINTENANCE",
                "0",
                "#D97706"
            )
        )

        self.decommissioned_card, self.decommissioned_value = (
            self.create_stat_card(
                "DECOMMISSIONED",
                "0",
                "#6B7280"
            )
        )

        self.departments_card, self.departments_value = (
            self.create_stat_card(
                "ACTIVE DEPARTMENTS",
                "0",
                "#2563EB"
            )
        )

        self.maintenance_records_card, self.maintenance_records_value = (
            self.create_stat_card(
                "MAINTENANCE RECORDS",
                "0",
                "#7C3AED"
            )
        )

        self.transfer_records_card, self.transfer_records_value = (
            self.create_stat_card(
                "TRANSFER RECORDS",
                "0",
                "#0891B2"
            )
        )

        stats_grid.addWidget(
            self.total_card,
            0,
            0
        )

        stats_grid.addWidget(
            self.functional_card,
            0,
            1
        )

        stats_grid.addWidget(
            self.nonfunctional_card,
            0,
            2
        )

        stats_grid.addWidget(
            self.maintenance_card,
            0,
            3
        )

        stats_grid.addWidget(
            self.decommissioned_card,
            1,
            0
        )

        stats_grid.addWidget(
            self.departments_card,
            1,
            1
        )

        stats_grid.addWidget(
            self.maintenance_records_card,
            1,
            2
        )

        stats_grid.addWidget(
            self.transfer_records_card,
            1,
            3
        )

        content_layout.addLayout(
            stats_grid
        )

        content_layout.addStretch()

        # -------------------------------------------------
        # FOOTER
        # -------------------------------------------------
        footer_layout = QHBoxLayout()

        footer_label = QLabel(
            "Karatina Sub-County Hospital • "
            "Medical Engineering Services"
        )

        footer_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 11px;
            }
        """)

        footer_layout.addWidget(
            footer_label
        )

        footer_layout.addStretch()

        exit_button = QPushButton(
            "Exit"
        )

        exit_button.setMinimumWidth(80)

        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)

        exit_button.clicked.connect(
            self.close_application
        )

        footer_layout.addWidget(
            exit_button
        )

        content_layout.addLayout(
            footer_layout
        )

    # =====================================================
    # MODULE CARD
    # =====================================================
    def create_module_card(
        self,
        icon,
        title,
        description,
        accent
    ):

        card = QFrame()

        card.setCursor(
            Qt.PointingHandCursor
        )

        card.setMinimumHeight(150)

        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #E5E7EB;
                border-left: 5px solid {accent};
                border-radius: 10px;
            }}

            QFrame:hover {{
                background-color: #F9FAFB;
                border: 1px solid {accent};
                border-left: 5px solid {accent};
            }}
        """)

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        icon_label = QLabel(
            icon
        )

        icon_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                border: none;
                background: transparent;
            }
        """)

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet(f"""
            QLabel {{
                color: {accent};
                font-size: 16px;
                font-weight: bold;
                border: none;
                background: transparent;
            }}
        """)

        description_label = QLabel(
            description
        )

        description_label.setWordWrap(True)

        description_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 12px;
                border: none;
                background: transparent;
            }
        """)

        layout.addWidget(
            icon_label
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            description_label
        )

        return card

    # =====================================================
    # STATISTIC CARD
    # =====================================================
    def create_stat_card(
        self,
        title,
        value,
        accent
    ):

        card = QFrame()

        card.setMinimumHeight(115)

        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #E5E7EB;
                border-top: 4px solid {accent};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            15,
            12,
            15,
            12
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 11px;
                font-weight: bold;
                border: none;
            }
        """)

        value_label = QLabel(
            value
        )

        value_label.setStyleSheet(f"""
            QLabel {{
                color: {accent};
                font-size: 30px;
                font-weight: bold;
                border: none;
            }}
        """)

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            value_label
        )

        layout.addStretch()

        return card, value_label

    # =====================================================
    # LOAD STATISTICS
    # =====================================================
    def load_statistics(self):

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # -------------------------------------------------
            # TOTAL EQUIPMENT
            # -------------------------------------------------
            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
            """)

            total_equipment = (
                cursor.fetchone()[0] or 0
            )

            # -------------------------------------------------
            # FUNCTIONAL
            # -------------------------------------------------
            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
                AND status = 'Functional'
            """)

            functional = (
                cursor.fetchone()[0] or 0
            )

            # -------------------------------------------------
            # NON-FUNCTIONAL
            # -------------------------------------------------
            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
                AND status = 'Non-Functional'
            """)

            nonfunctional = (
                cursor.fetchone()[0] or 0
            )

            # -------------------------------------------------
            # UNDER MAINTENANCE
            # -------------------------------------------------
            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
                AND status = 'Under Maintenance'
            """)

            under_maintenance = (
                cursor.fetchone()[0] or 0
            )

            # -------------------------------------------------
            # DECOMMISSIONED
            # -------------------------------------------------
            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
                AND status = 'Decommissioned'
            """)

            decommissioned = (
                cursor.fetchone()[0] or 0
            )

            # -------------------------------------------------
            # ACTIVE DEPARTMENTS
            # -------------------------------------------------
            cursor.execute("""
                SELECT COUNT(*)
                FROM departments
                WHERE is_active = 1
            """)

            active_departments = (
                cursor.fetchone()[0] or 0
            )

            # -------------------------------------------------
            # MAINTENANCE RECORDS
            # -------------------------------------------------
            try:

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM maintenance
                """)

                maintenance_records = (
                    cursor.fetchone()[0] or 0
                )

            except Exception:

                maintenance_records = 0

            # -------------------------------------------------
            # TRANSFER RECORDS
            # -------------------------------------------------
            try:

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM equipment_transactions
                """)

                transfer_records = (
                    cursor.fetchone()[0] or 0
                )

            except Exception:

                transfer_records = 0

            cursor.close()
            connection.close()

            # -------------------------------------------------
            # UPDATE UI
            # -------------------------------------------------
            self.total_value.setText(
                str(total_equipment)
            )

            self.functional_value.setText(
                str(functional)
            )

            self.nonfunctional_value.setText(
                str(nonfunctional)
            )

            self.maintenance_value.setText(
                str(under_maintenance)
            )

            self.decommissioned_value.setText(
                str(decommissioned)
            )

            self.departments_value.setText(
                str(active_departments)
            )

            self.maintenance_records_value.setText(
                str(maintenance_records)
            )

            self.transfer_records_value.setText(
                str(transfer_records)
            )

        except Exception as e:

            # Do not crash the dashboard if statistics
            # cannot be loaded.

            self.total_value.setText("0")
            self.functional_value.setText("0")
            self.nonfunctional_value.setText("0")
            self.maintenance_value.setText("0")
            self.decommissioned_value.setText("0")
            self.departments_value.setText("0")
            self.maintenance_records_value.setText("0")
            self.transfer_records_value.setText("0")

            print(
                "Dashboard statistics error:",
                e
            )

    # =====================================================
    # OPEN INVENTORY
    # =====================================================
    def open_inventory(self):

        try:

            from screens.inventory import (
                EquipmentInventoryWindow
            )

            self.inventory_window = (
                EquipmentInventoryWindow(
                    parent=self,
                    user_id=self.user_id,
                    role=self.role
                )
            )

            self.inventory_window.show()

            self.inventory_window.resize(
                1400,
                800
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Inventory Error",
                f"Could not open Medical Equipment Inventory.\n\n"
                f"{e}"
            )

    # =====================================================
    # OPEN MAINTENANCE
    # =====================================================
    def open_maintenance(self):

        try:

            from screens.maintenance import (
                MaintenanceWindow
            )

            self.maintenance_window = (
                MaintenanceWindow(
                    user_id=self.user_id
                )
            )

            self.maintenance_window.show()

            self.maintenance_window.resize(
                1400,
                800
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Maintenance Error",
                f"Could not open Equipment Maintenance.\n\n"
                f"{e}"
            )

    # =====================================================
    # OPEN TRANSFERS
    # =====================================================
    def open_transfers(self):

        try:

            from screens.transfers import (
                TransferWindow
            )

            self.transfer_window = (
                TransferWindow(
                    user_id=self.user_id
                )
            )

            self.transfer_window.show()

            self.transfer_window.resize(
                1400,
                800
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Transfer Error",
                f"Could not open Equipment Transfers.\n\n"
                f"{e}"
            )

    # =====================================================
    # CLOSE APPLICATION
    # =====================================================
    def close_application(self):

        confirmation = QMessageBox.question(
            self,
            "Exit System",
            "Are you sure you want to exit the system?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            QApplication.quit()


# =========================================================
# STANDALONE TEST
# =========================================================
if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = DashboardWindow(
        user_id=1,
        username="Admin",
        role="Admin"
    )

    window.show()

    sys.exit(app.exec())