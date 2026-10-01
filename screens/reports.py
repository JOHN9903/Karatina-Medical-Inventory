import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QGroupBox,
    QGridLayout,
    QComboBox,
)
from PySide6.QtCore import Qt
from database.connection import get_connection


class ReportsWindow(QMainWindow):

    def __init__(self, user_id=1):
        super().__init__()

        self.user_id = user_id

        self.setWindowTitle(
            "Karatina Sub-County Hospital - Reports & Analytics"
        )

        self.setMinimumSize(1250, 800)

        self.setup_ui()
        self.load_reports()

    # ==========================================================
    # USER INTERFACE
    # ==========================================================

    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # ======================================================
        # TITLE
        # ======================================================

        title = QLabel("Reports & Analytics")

        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                padding: 10px;
            }
        """)

        main_layout.addWidget(title)

        subtitle = QLabel(
            "Medical equipment inventory, condition and maintenance overview"
        )

        subtitle.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14px;
                padding-left: 10px;
                padding-bottom: 10px;
            }
        """)

        main_layout.addWidget(subtitle)

        # ======================================================
        # SUMMARY CARDS
        # ======================================================

        summary_group = QGroupBox("Equipment Summary")

        summary_layout = QGridLayout()
        summary_group.setLayout(summary_layout)

        self.total_label = self.create_summary_label(
            "Total Equipment"
        )

        self.functional_label = self.create_summary_label(
            "Functional"
        )

        self.nonfunctional_label = self.create_summary_label(
            "Non-Functional"
        )

        self.maintenance_label = self.create_summary_label(
            "Under Maintenance"
        )

        self.decommissioned_label = self.create_summary_label(
            "Decommissioned"
        )

        summary_layout.addWidget(
            self.total_label,
            0,
            0
        )

        summary_layout.addWidget(
            self.functional_label,
            0,
            1
        )

        summary_layout.addWidget(
            self.nonfunctional_label,
            0,
            2
        )

        summary_layout.addWidget(
            self.maintenance_label,
            0,
            3
        )

        summary_layout.addWidget(
            self.decommissioned_label,
            0,
            4
        )

        main_layout.addWidget(
            summary_group
        )

        # ======================================================
        # FILTER
        # ======================================================

        filter_layout = QHBoxLayout()

        filter_label = QLabel(
            "Report:"
        )

        self.report_combo = QComboBox()

        self.report_combo.addItems([
            "All Equipment",
            "Functional Equipment",
            "Non-Functional Equipment",
            "Under Maintenance",
            "Decommissioned Equipment"
        ])

        self.report_combo.setMinimumHeight(35)

        refresh_button = QPushButton(
            "REFRESH REPORT"
        )

        refresh_button.setMinimumHeight(35)

        refresh_button.clicked.connect(
            self.load_reports
        )

        filter_layout.addWidget(
            filter_label
        )

        filter_layout.addWidget(
            self.report_combo
        )

        filter_layout.addWidget(
            refresh_button
        )

        filter_layout.addStretch()

        main_layout.addLayout(
            filter_layout
        )

        self.report_combo.currentIndexChanged.connect(
            self.load_report_table
        )

        # ======================================================
        # REPORT TABLE
        # ======================================================

        table_title = QLabel(
            "Equipment Report"
        )

        table_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                padding-top: 15px;
                padding-bottom: 5px;
            }
        """)

        main_layout.addWidget(
            table_title
        )

        self.report_table = QTableWidget()

        self.report_table.setColumnCount(9)

        self.report_table.setHorizontalHeaderLabels([
            "ID",
            "Equipment",
            "Model",
            "Serial Number",
            "Manufacturer",
            "Year",
            "Department",
            "Status",
            "Date Added"
        ])

        self.report_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.report_table.setAlternatingRowColors(
            True
        )

        self.report_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.report_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        main_layout.addWidget(
            self.report_table
        )

        # ======================================================
        # MAINTENANCE SUMMARY
        # ======================================================

        maintenance_title = QLabel(
            "Maintenance Summary"
        )

        maintenance_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                padding-top: 15px;
                padding-bottom: 5px;
            }
        """)

        main_layout.addWidget(
            maintenance_title
        )

        self.maintenance_summary = QLabel(
            "Loading maintenance information..."
        )

        self.maintenance_summary.setStyleSheet("""
            QLabel {
                font-size: 15px;
                padding: 10px;
            }
        """)

        main_layout.addWidget(
            self.maintenance_summary
        )

    # ==========================================================
    # SUMMARY LABEL
    # ==========================================================

    def create_summary_label(self, title):

        label = QLabel(
            f"{title}\n0"
        )

        label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        label.setMinimumHeight(
            80
        )

        label.setStyleSheet("""
            QLabel {
                border: 1px solid #cccccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        return label

    # ==========================================================
    # LOAD REPORTS
    # ==========================================================

    def load_reports(self):

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

            # --------------------------------------------------
            # TOTAL
            # --------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
            """)

            total = cursor.fetchone()[0]

            # --------------------------------------------------
            # FUNCTIONAL
            # --------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
                AND status = 'Functional'
            """)

            functional = cursor.fetchone()[0]

            # --------------------------------------------------
            # NON-FUNCTIONAL
            # --------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
                AND status = 'Non-Functional'
            """)

            nonfunctional = cursor.fetchone()[0]

            # --------------------------------------------------
            # UNDER MAINTENANCE
            # --------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
                AND status = 'Under Maintenance'
            """)

            under_maintenance = cursor.fetchone()[0]

            # --------------------------------------------------
            # DECOMMISSIONED
            # --------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM equipment_inventory
                WHERE is_active = 1
                AND status = 'Decommissioned'
            """)

            decommissioned = cursor.fetchone()[0]

            # --------------------------------------------------
            # UPDATE SUMMARY
            # --------------------------------------------------

            self.total_label.setText(
                f"Total Equipment\n{total}"
            )

            self.functional_label.setText(
                f"Functional\n{functional}"
            )

            self.nonfunctional_label.setText(
                f"Non-Functional\n{nonfunctional}"
            )

            self.maintenance_label.setText(
                f"Under Maintenance\n{under_maintenance}"
            )

            self.decommissioned_label.setText(
                f"Decommissioned\n{decommissioned}"
            )

            # --------------------------------------------------
            # MAINTENANCE SUMMARY
            # --------------------------------------------------

            try:

                cursor.execute("""
                    SELECT
                        COUNT(*),
                        COALESCE(SUM(maintenance_cost), 0)
                    FROM maintenance
                """)

                maintenance_data = cursor.fetchone()

                maintenance_count = maintenance_data[0]
                maintenance_cost = maintenance_data[1]

                self.maintenance_summary.setText(
                    f"Maintenance Records: {maintenance_count}    |    "
                    f"Total Maintenance Cost: KES "
                    f"{maintenance_cost:,.2f}"
                )

            except Exception:

                self.maintenance_summary.setText(
                    "Maintenance information unavailable."
                )

            self.load_report_table()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Report Error",
                f"Could not generate report:\n\n{error}"
            )

        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass

    # ==========================================================
    # LOAD REPORT TABLE
    # ==========================================================

    def load_report_table(self):

        report = self.report_combo.currentText()

        self.report_table.setRowCount(0)

        connection = get_connection()

        if not connection:

            return

        cursor = None

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    ei.equipment_id,
                    en.equipment_name,
                    ei.model_number,
                    ei.serial_number,
                    ei.manufacturer,
                    ei.year_of_manufacture,
                    d.department_name,
                    ei.status,
                    ei.date_added
                FROM equipment_inventory ei
                INNER JOIN equipment_names en
                    ON ei.equipment_name_id = en.equipment_name_id
                INNER JOIN departments d
                    ON ei.department_id = d.department_id
                WHERE ei.is_active = 1
            """

            parameters = ()

            # --------------------------------------------------
            # FILTER
            # --------------------------------------------------

            if report == "Functional Equipment":

                query += """
                    AND ei.status = %s
                """

                parameters = (
                    "Functional",
                )

            elif report == "Non-Functional Equipment":

                query += """
                    AND ei.status = %s
                """

                parameters = (
                    "Non-Functional",
                )

            elif report == "Under Maintenance":

                query += """
                    AND ei.status = %s
                """

                parameters = (
                    "Under Maintenance",
                )

            elif report == "Decommissioned Equipment":

                query += """
                    AND ei.status = %s
                """

                parameters = (
                    "Decommissioned",
                )

            query += """
                ORDER BY en.equipment_name
            """

            cursor.execute(
                query,
                parameters
            )

            records = cursor.fetchall()

            for record in records:

                row = self.report_table.rowCount()

                self.report_table.insertRow(
                    row
                )

                for column, value in enumerate(
                    record
                ):

                    if value is None:
                        value = ""

                    self.report_table.setItem(
                        row,
                        column,
                        QTableWidgetItem(
                            str(value)
                        )
                    )

        except Exception as error:

            QMessageBox.warning(
                self,
                "Report Error",
                f"Could not load equipment report:\n\n{error}"
            )

        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass


# ==============================================================
# STANDALONE TEST
# ==============================================================

if __name__ == "__main__":

    from PySide6.QtCore import Qt

    app = QApplication(sys.argv)

    window = ReportsWindow(
        user_id=1
    )

    window.show()

    sys.exit(
        app.exec()
    )