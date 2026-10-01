import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QDoubleSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QGroupBox,
)

from PySide6.QtCore import QDate

from database.connection import get_connection


class MaintenanceWindow(QMainWindow):

    def __init__(self, user_id=1):
        super().__init__()

        self.user_id = user_id
        self.equipment_records = []

        self.setWindowTitle(
            "Karatina Sub-County Hospital - Equipment Maintenance"
        )

        self.setMinimumSize(1250, 800)

        self.setup_ui()
        self.load_equipment()
        self.load_maintenance_records()

    # ==========================================================
    # USER INTERFACE
    # ==========================================================

    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        title = QLabel("Equipment Maintenance")

        title.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
                padding: 10px;
            }
        """)

        main_layout.addWidget(title)

        subtitle = QLabel(
            "Record and monitor preventive and corrective maintenance "
            "activities for hospital equipment."
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
        # MAINTENANCE FORM
        # ======================================================

        form_group = QGroupBox("Maintenance Record")
        form_layout = QFormLayout()
        form_group.setLayout(form_layout)

        # Equipment search
        self.equipment_search = QLineEdit()

        self.equipment_search.setPlaceholderText(
            "Search equipment name, model or serial number..."
        )

        self.equipment_search.setMinimumHeight(35)

        self.equipment_search.textChanged.connect(
            self.filter_equipment
        )

        form_layout.addRow(
            "Search Equipment:",
            self.equipment_search
        )

        # Equipment
        self.equipment_combo = QComboBox()
        self.equipment_combo.setMinimumHeight(35)

        self.equipment_combo.currentIndexChanged.connect(
            self.show_equipment_information
        )

        form_layout.addRow(
            "Equipment:",
            self.equipment_combo
        )

        # Current status
        self.current_status = QLabel("")

        self.current_status.setStyleSheet("""
            QLabel {
                font-weight: bold;
                padding: 5px;
            }
        """)

        form_layout.addRow(
            "Current Status:",
            self.current_status
        )

        # Maintenance type
        self.maintenance_type = QComboBox()

        self.maintenance_type.addItems([
            "Preventive",
            "Corrective"
        ])

        self.maintenance_type.setMinimumHeight(35)

        form_layout.addRow(
            "Maintenance Type:",
            self.maintenance_type
        )

        # Maintenance date
        self.maintenance_date = QDateEdit()

        self.maintenance_date.setCalendarPopup(True)
        self.maintenance_date.setDate(QDate.currentDate())
        self.maintenance_date.setMinimumHeight(35)

        form_layout.addRow(
            "Maintenance Date:",
            self.maintenance_date
        )

        # Fault reported
        self.fault_reported = QTextEdit()

        self.fault_reported.setPlaceholderText(
            "Describe the fault reported, if applicable..."
        )

        self.fault_reported.setMaximumHeight(70)

        form_layout.addRow(
            "Fault Reported:",
            self.fault_reported
        )

        # Diagnosis
        self.diagnosis = QTextEdit()

        self.diagnosis.setPlaceholderText(
            "Enter diagnosis / findings..."
        )

        self.diagnosis.setMaximumHeight(70)

        form_layout.addRow(
            "Diagnosis:",
            self.diagnosis
        )

        # Work performed
        self.work_performed = QTextEdit()

        self.work_performed.setPlaceholderText(
            "Describe the maintenance work performed..."
        )

        self.work_performed.setMaximumHeight(70)

        form_layout.addRow(
            "Work Performed:",
            self.work_performed
        )

        # Parts replaced
        self.parts_replaced = QTextEdit()

        self.parts_replaced.setPlaceholderText(
            "List parts replaced, if any..."
        )

        self.parts_replaced.setMaximumHeight(60)

        form_layout.addRow(
            "Parts Replaced:",
            self.parts_replaced
        )

        # Technician
        self.technician = QLineEdit()

        self.technician.setPlaceholderText(
            "Technician name"
        )

        form_layout.addRow(
            "Technician:",
            self.technician
        )

        # Maintenance cost
        self.maintenance_cost = QDoubleSpinBox()

        self.maintenance_cost.setMaximum(
            999999999.99
        )

        self.maintenance_cost.setDecimals(2)
        self.maintenance_cost.setValue(0.00)
        self.maintenance_cost.setPrefix("KES ")

        form_layout.addRow(
            "Maintenance Cost:",
            self.maintenance_cost
        )

        # Next maintenance
        self.next_maintenance_date = QDateEdit()

        self.next_maintenance_date.setCalendarPopup(True)
        self.next_maintenance_date.setDate(QDate.currentDate())
        self.next_maintenance_date.setMinimumHeight(35)

        form_layout.addRow(
            "Next Maintenance:",
            self.next_maintenance_date
        )

        # Equipment status
        self.equipment_status = QComboBox()

        self.equipment_status.addItems([
            "Functional",
            "Non-Functional",
            "Under Maintenance",
            "Decommissioned"
        ])

        self.equipment_status.setMinimumHeight(35)

        form_layout.addRow(
            "Equipment Status:",
            self.equipment_status
        )

        # Remarks
        self.remarks = QTextEdit()

        self.remarks.setPlaceholderText(
            "Additional remarks..."
        )

        self.remarks.setMaximumHeight(70)

        form_layout.addRow(
            "Remarks:",
            self.remarks
        )

        main_layout.addWidget(form_group)

        # ======================================================
        # BUTTONS
        # ======================================================

        button_layout = QHBoxLayout()

        save_button = QPushButton(
            "SAVE MAINTENANCE RECORD"
        )

        save_button.setMinimumHeight(45)

        save_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        save_button.clicked.connect(
            self.save_maintenance
        )

        clear_button = QPushButton("CLEAR")
        clear_button.setMinimumHeight(45)

        clear_button.clicked.connect(
            self.clear_form
        )

        refresh_button = QPushButton("REFRESH")
        refresh_button.setMinimumHeight(45)

        refresh_button.clicked.connect(
            self.refresh_data
        )

        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(refresh_button)

        main_layout.addLayout(button_layout)

        # ======================================================
        # HISTORY
        # ======================================================

        history_title = QLabel(
            "Maintenance History"
        )

        history_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                padding-top: 15px;
                padding-bottom: 5px;
            }
        """)

        main_layout.addWidget(history_title)

        self.history_table = QTableWidget()

        self.history_table.setColumnCount(10)

        self.history_table.setHorizontalHeaderLabels([
            "ID",
            "Equipment",
            "Type",
            "Date",
            "Technician",
            "Cost",
            "Status",
            "Next Maintenance",
            "Performed By",
            "Remarks"
        ])

        self.history_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.history_table.setAlternatingRowColors(True)

        self.history_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.history_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        main_layout.addWidget(
            self.history_table
        )

    # ==========================================================
    # LOAD EQUIPMENT
    # ==========================================================

    def load_equipment(self):

        self.equipment_records = []

        self.equipment_combo.clear()

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

            query = """
                SELECT
                    ei.equipment_id,
                    en.equipment_name,
                    ei.model_number,
                    ei.serial_number,
                    ei.status
                FROM equipment_inventory ei
                INNER JOIN equipment_names en
                    ON ei.equipment_name_id = en.equipment_name_id
                WHERE ei.is_active = 1
                ORDER BY en.equipment_name
            """

            cursor.execute(query)

            records = cursor.fetchall()

            for record in records:

                equipment_id = record[0]
                equipment_name = record[1]
                model = record[2] or ""
                serial = record[3] or ""
                status = record[4] or "Functional"

                display = equipment_name

                if model:
                    display += f" | Model: {model}"

                if serial:
                    display += f" | S/N: {serial}"

                self.equipment_records.append({
                    "equipment_id": equipment_id,
                    "equipment_name": equipment_name,
                    "model": model,
                    "serial": serial,
                    "status": status,
                    "display": display
                })

            self.populate_equipment_combo(
                self.equipment_records
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Could not load equipment:\n\n{error}"
            )

        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass

    # ==========================================================
    # POPULATE EQUIPMENT
    # ==========================================================

    def populate_equipment_combo(self, records):

        self.equipment_combo.blockSignals(True)

        self.equipment_combo.clear()

        for record in records:

            self.equipment_combo.addItem(
                record["display"],
                record["equipment_id"]
            )

        self.equipment_combo.blockSignals(False)

        if self.equipment_combo.count() > 0:

            self.equipment_combo.setCurrentIndex(0)

            self.show_equipment_information()

        else:

            self.current_status.setText("No equipment found.")

    # ==========================================================
    # FILTER EQUIPMENT
    # ==========================================================

    def filter_equipment(self, text):

        search_text = text.strip().lower()

        if not search_text:

            filtered = self.equipment_records

        else:

            filtered = []

            for record in self.equipment_records:

                searchable = " ".join([
                    record["equipment_name"],
                    record["model"],
                    record["serial"]
                ]).lower()

                if search_text in searchable:
                    filtered.append(record)

        self.populate_equipment_combo(filtered)

    # ==========================================================
    # SHOW EQUIPMENT INFORMATION
    # ==========================================================

    def show_equipment_information(self):

        index = self.equipment_combo.currentIndex()

        if index < 0:

            self.current_status.setText("")

            return

        equipment_id = self.equipment_combo.itemData(index)

        selected = None

        for record in self.equipment_records:

            if record["equipment_id"] == equipment_id:

                selected = record

                break

        if not selected:

            self.current_status.setText("")

            return

        self.current_status.setText(
            selected["status"]
        )

        status_index = self.equipment_status.findText(
            selected["status"]
        )

        if status_index >= 0:

            self.equipment_status.setCurrentIndex(
                status_index
            )

    # ==========================================================
    # LOAD MAINTENANCE HISTORY
    # ==========================================================

    def load_maintenance_records(self):

        self.history_table.setRowCount(0)

        connection = get_connection()

        if not connection:
            return

        cursor = None

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                    m.maintenance_id,
                    en.equipment_name,
                    m.maintenance_type,
                    m.maintenance_date,
                    m.technician,
                    m.maintenance_cost,
                    m.equipment_status,
                    m.next_maintenance_date,
                    su.username,
                    m.remarks
                FROM maintenance m
                INNER JOIN equipment_inventory ei
                    ON m.equipment_id = ei.equipment_id
                INNER JOIN equipment_names en
                    ON ei.equipment_name_id = en.equipment_name_id
                INNER JOIN system_users su
                    ON m.performed_by = su.user_id
                ORDER BY
                    m.maintenance_date DESC,
                    m.maintenance_id DESC
            """

            cursor.execute(query)

            records = cursor.fetchall()

            for record in records:

                row = self.history_table.rowCount()

                self.history_table.insertRow(row)

                for column, value in enumerate(record):

                    if value is None:
                        value = ""

                    self.history_table.setItem(
                        row,
                        column,
                        QTableWidgetItem(str(value))
                    )

        except Exception as error:

            QMessageBox.warning(
                self,
                "Maintenance History",
                f"Could not load maintenance history:\n\n{error}"
            )

        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass

    # ==========================================================
    # SAVE MAINTENANCE
    # ==========================================================

    def save_maintenance(self):

        equipment_id = self.equipment_combo.currentData()

        if not equipment_id:

            QMessageBox.warning(
                self,
                "Missing Equipment",
                "Please select equipment."
            )

            return

        work_performed = (
            self.work_performed.toPlainText().strip()
        )

        if not work_performed:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter the work performed."
            )

            return

        maintenance_type = (
            self.maintenance_type.currentText()
        )

        maintenance_date = (
            self.maintenance_date.date().toString(
                "yyyy-MM-dd"
            )
        )

        fault_reported = (
            self.fault_reported.toPlainText().strip()
        )

        diagnosis = (
            self.diagnosis.toPlainText().strip()
        )

        parts_replaced = (
            self.parts_replaced.toPlainText().strip()
        )

        technician = (
            self.technician.text().strip()
        )

        maintenance_cost = (
            self.maintenance_cost.value()
        )

        next_date = (
            self.next_maintenance_date.date().toString(
                "yyyy-MM-dd"
            )
        )

        equipment_status = (
            self.equipment_status.currentText()
        )

        remarks = (
            self.remarks.toPlainText().strip()
        )

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

            query = """
                INSERT INTO maintenance (
                    equipment_id,
                    maintenance_type,
                    maintenance_date,
                    fault_reported,
                    diagnosis,
                    work_performed,
                    parts_replaced,
                    technician,
                    maintenance_cost,
                    next_maintenance_date,
                    equipment_status,
                    remarks,
                    performed_by
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
            """

            values = (
                equipment_id,
                maintenance_type,
                maintenance_date,
                fault_reported,
                diagnosis,
                work_performed,
                parts_replaced,
                technician,
                maintenance_cost,
                next_date,
                equipment_status,
                remarks,
                self.user_id
            )

            cursor.execute(
                query,
                values
            )

            update_query = """
                UPDATE equipment_inventory
                SET status = %s
                WHERE equipment_id = %s
            """

            cursor.execute(
                update_query,
                (
                    equipment_status,
                    equipment_id
                )
            )

            connection.commit()

            QMessageBox.information(
                self,
                "Success",
                "Maintenance record saved successfully."
            )

            self.clear_form()

            self.load_equipment()

            self.load_maintenance_records()

        except Exception as error:

            connection.rollback()

            QMessageBox.critical(
                self,
                "Save Error",
                f"Could not save maintenance record:\n\n{error}"
            )

        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass

    # ==========================================================
    # CLEAR FORM
    # ==========================================================

    def clear_form(self):

        self.equipment_search.clear()

        if self.equipment_combo.count() > 0:

            self.equipment_combo.setCurrentIndex(0)

        self.maintenance_type.setCurrentIndex(0)

        self.maintenance_date.setDate(
            QDate.currentDate()
        )

        self.fault_reported.clear()
        self.diagnosis.clear()
        self.work_performed.clear()
        self.parts_replaced.clear()
        self.technician.clear()

        self.maintenance_cost.setValue(0.00)

        self.next_maintenance_date.setDate(
            QDate.currentDate()
        )

        self.remarks.clear()

        self.show_equipment_information()

    # ==========================================================
    # REFRESH
    # ==========================================================

    def refresh_data(self):

        self.load_equipment()
        self.load_maintenance_records()


# ==============================================================
# STANDALONE TEST
# ==============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MaintenanceWindow(user_id=1)

    window.show()

    sys.exit(app.exec())