import sys
import os

# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ==========================================================
# PYSide6
# ==========================================================

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
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QGroupBox,
)

from PySide6.QtCore import QDate, Qt


# ==========================================================
# DATABASE
# ==========================================================

from database.connection import get_connection


# ==========================================================
# TRANSFERS WINDOW
# ==========================================================

class TransferWindow(QMainWindow):

    def __init__(
        self,
        user_id=1,
        username="Admin"
    ):

        super().__init__()

        self.user_id = user_id

        self.username = username

        self.equipment_records = []

        self.department_records = []

        self.setWindowTitle(
            "Karatina Sub-County Hospital - Equipment Transfers"
        )

        self.setMinimumSize(
            1250,
            800
        )

        self.setup_ui()

        self.load_departments()

        self.load_equipment()

        self.load_transfers()


    # ======================================================
    # USER INTERFACE
    # ======================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout()

        central.setLayout(
            main_layout
        )


        # ==================================================
        # TITLE
        # ==================================================

        title = QLabel(
            "Equipment Transfers"
        )

        title.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
                padding: 10px;
            }
            """
        )

        main_layout.addWidget(
            title
        )


        subtitle = QLabel(
            "Internal transfer of medical equipment between hospital departments."
        )

        subtitle.setStyleSheet(
            """
            QLabel {
                color: #666666;
                font-size: 14px;
                padding-left: 10px;
                padding-bottom: 10px;
            }
            """
        )

        main_layout.addWidget(
            subtitle
        )


        # ==================================================
        # TRANSFER FORM
        # ==================================================

        form_group = QGroupBox(
            "Internal Equipment Transfer"
        )

        form_layout = QFormLayout()

        form_group.setLayout(
            form_layout
        )


        # ==================================================
        # EQUIPMENT SEARCH
        # ==================================================

        self.equipment_search = QLineEdit()

        self.equipment_search.setPlaceholderText(
            "Search equipment name, model or serial number..."
        )

        self.equipment_search.setMinimumHeight(
            35
        )

        self.equipment_search.textChanged.connect(
            self.filter_equipment
        )

        form_layout.addRow(
            "Search Equipment:",
            self.equipment_search
        )


        # ==================================================
        # EQUIPMENT
        # ==================================================

        self.equipment_combo = QComboBox()

        self.equipment_combo.setMinimumHeight(
            35
        )

        self.equipment_combo.currentIndexChanged.connect(
            self.show_equipment_information
        )

        form_layout.addRow(
            "Equipment:",
            self.equipment_combo
        )


        # ==================================================
        # CURRENT DEPARTMENT
        # ==================================================

        self.current_department = QLabel(
            ""
        )

        self.current_department.setStyleSheet(
            """
            QLabel {
                font-weight: bold;
                padding: 5px;
            }
            """
        )

        form_layout.addRow(
            "Current Department:",
            self.current_department
        )


        # ==================================================
        # FROM DEPARTMENT
        # ==================================================

        self.from_department = QComboBox()

        self.from_department.setMinimumHeight(
            35
        )

        form_layout.addRow(
            "From Department:",
            self.from_department
        )


        # ==================================================
        # TO DEPARTMENT
        # ==================================================

        self.to_department = QComboBox()

        self.to_department.setMinimumHeight(
            35
        )

        form_layout.addRow(
            "To Department:",
            self.to_department
        )


        # ==================================================
        # TRANSFER DATE
        # ==================================================

        self.transfer_date = QDateEdit()

        self.transfer_date.setCalendarPopup(
            True
        )

        self.transfer_date.setDate(
            QDate.currentDate()
        )

        self.transfer_date.setMinimumHeight(
            35
        )

        form_layout.addRow(
            "Transfer Date:",
            self.transfer_date
        )


        # ==================================================
        # REASON
        # ==================================================

        self.reason = QTextEdit()

        self.reason.setPlaceholderText(
            "Enter reason for the transfer..."
        )

        self.reason.setMaximumHeight(
            70
        )

        form_layout.addRow(
            "Reason:",
            self.reason
        )


        # ==================================================
        # CONDITION BEFORE
        # ==================================================

        self.condition_before = QLineEdit()

        self.condition_before.setPlaceholderText(
            "Condition of equipment before transfer"
        )

        form_layout.addRow(
            "Condition Before:",
            self.condition_before
        )


        # ==================================================
        # CONDITION AFTER
        # ==================================================

        self.condition_after = QLineEdit()

        self.condition_after.setPlaceholderText(
            "Condition of equipment after transfer"
        )

        form_layout.addRow(
            "Condition After:",
            self.condition_after
        )


        # ==================================================
        # RECEIVED BY
        # ==================================================

        self.received_by = QLineEdit()

        self.received_by.setPlaceholderText(
            "Name of person receiving equipment"
        )

        form_layout.addRow(
            "Received By:",
            self.received_by
        )


        # ==================================================
        # STATUS
        # ==================================================

        self.status = QComboBox()

        self.status.addItems(
            [
                "Pending",
                "Approved",
                "Completed",
                "Cancelled"
            ]
        )

        self.status.setMinimumHeight(
            35
        )

        form_layout.addRow(
            "Transfer Status:",
            self.status
        )


        # ==================================================
        # REMARKS
        # ==================================================

        self.remarks = QTextEdit()

        self.remarks.setPlaceholderText(
            "Additional remarks..."
        )

        self.remarks.setMaximumHeight(
            70
        )

        form_layout.addRow(
            "Remarks:",
            self.remarks
        )


        main_layout.addWidget(
            form_group
        )


        # ==================================================
        # BUTTONS
        # ==================================================

        button_layout = QHBoxLayout()


        save_button = QPushButton(
            "SAVE TRANSFER"
        )

        save_button.setMinimumHeight(
            45
        )

        save_button.setStyleSheet(
            """
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
            """
        )

        save_button.clicked.connect(
            self.save_transfer
        )


        clear_button = QPushButton(
            "CLEAR"
        )

        clear_button.setMinimumHeight(
            45
        )

        clear_button.clicked.connect(
            self.clear_form
        )


        refresh_button = QPushButton(
            "REFRESH"
        )

        refresh_button.setMinimumHeight(
            45
        )

        refresh_button.clicked.connect(
            self.refresh_data
        )


        button_layout.addWidget(
            save_button
        )

        button_layout.addWidget(
            clear_button
        )

        button_layout.addWidget(
            refresh_button
        )

        main_layout.addLayout(
            button_layout
        )


        # ==================================================
        # HISTORY
        # ==================================================

        history_title = QLabel(
            "Transfer History"
        )

        history_title.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: bold;
                padding-top: 15px;
                padding-bottom: 5px;
            }
            """
        )

        main_layout.addWidget(
            history_title
        )


        self.transfer_table = QTableWidget()

        self.transfer_table.setColumnCount(
            11
        )

        self.transfer_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Equipment",
                "From",
                "To",
                "Date",
                "Reason",
                "Transferred By",
                "Received By",
                "Status",
                "Remarks",
                "Created"
            ]
        )


        self.transfer_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        self.transfer_table.horizontalHeader().setStretchLastSection(
            True
        )

        self.transfer_table.setAlternatingRowColors(
            True
        )

        self.transfer_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.transfer_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        main_layout.addWidget(
            self.transfer_table
        )


    # ======================================================
    # LOAD DEPARTMENTS
    # ======================================================

    def load_departments(self):

        self.department_records = []

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
                    department_id,
                    department_name
                FROM departments
                WHERE is_active = 1
                ORDER BY department_name
                """
            )

            records = cursor.fetchall()


            self.from_department.clear()

            self.to_department.clear()


            for department_id, name in records:

                self.department_records.append(
                    {
                        "id": department_id,
                        "name": name
                    }
                )


                self.from_department.addItem(
                    name,
                    department_id
                )


                self.to_department.addItem(
                    name,
                    department_id
                )


        except Exception as error:

            QMessageBox.critical(
                self,
                "Database Error",
                "Could not load departments:\n\n"
                + str(error)
            )


        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass


    # ======================================================
    # LOAD EQUIPMENT
    # ======================================================

    def load_equipment(self):

        self.equipment_records = []

        connection = get_connection()

        if not connection:

            return


        cursor = None


        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    ei.equipment_id,
                    en.equipment_name,
                    ei.model_number,
                    ei.serial_number,
                    ei.department_id,
                    d.department_name,
                    ei.status
                FROM equipment_inventory ei

                INNER JOIN equipment_names en
                    ON ei.equipment_name_id =
                       en.equipment_name_id

                INNER JOIN departments d
                    ON ei.department_id =
                       d.department_id

                WHERE ei.is_active = 1

                ORDER BY en.equipment_name
                """
            )


            records = cursor.fetchall()


            for record in records:

                equipment_id = record[0]

                equipment_name = record[1]

                model = record[2] or ""

                serial = record[3] or ""

                department_id = record[4]

                department_name = record[5]

                status = record[6]


                display = equipment_name


                if model:

                    display += (
                        " | Model: "
                        + str(model)
                    )


                if serial:

                    display += (
                        " | S/N: "
                        + str(serial)
                    )


                self.equipment_records.append(
                    {
                        "equipment_id": equipment_id,
                        "equipment_name": equipment_name,
                        "model": model,
                        "serial": serial,
                        "department_id": department_id,
                        "department_name": department_name,
                        "status": status,
                        "display": display
                    }
                )


            self.populate_equipment(
                self.equipment_records
            )


        except Exception as error:

            QMessageBox.critical(
                self,
                "Database Error",
                "Could not load equipment:\n\n"
                + str(error)
            )


        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass


    # ======================================================
    # POPULATE EQUIPMENT
    # ======================================================

    def populate_equipment(
        self,
        records
    ):

        self.equipment_combo.blockSignals(
            True
        )

        self.equipment_combo.clear()


        for record in records:

            self.equipment_combo.addItem(
                record["display"],
                record["equipment_id"]
            )


        self.equipment_combo.blockSignals(
            False
        )


        if self.equipment_combo.count() > 0:

            self.equipment_combo.setCurrentIndex(
                0
            )

            self.show_equipment_information()


        else:

            self.current_department.setText(
                ""
            )


    # ======================================================
    # FILTER EQUIPMENT
    # ======================================================

    def filter_equipment(
        self,
        text
    ):

        search_text = (
            text
            .strip()
            .lower()
        )


        if not search_text:

            filtered = (
                self.equipment_records
            )


        else:

            filtered = []


            for record in self.equipment_records:

                searchable = " ".join(
                    [
                        str(record["equipment_name"]),
                        str(record["model"]),
                        str(record["serial"])
                    ]
                ).lower()


                if search_text in searchable:

                    filtered.append(
                        record
                    )


        self.populate_equipment(
            filtered
        )


    # ======================================================
    # SHOW EQUIPMENT INFORMATION
    # ======================================================

    def show_equipment_information(
        self
    ):

        index = (
            self.equipment_combo.currentIndex()
        )


        if index < 0:

            self.current_department.setText(
                ""
            )

            return


        equipment_id = (
            self.equipment_combo.itemData(
                index
            )
        )


        selected = None


        for record in self.equipment_records:

            if record["equipment_id"] == equipment_id:

                selected = record

                break


        if not selected:

            return


        self.current_department.setText(
            selected["department_name"]
        )


        department_index = (
            self.from_department.findData(
                selected["department_id"]
            )
        )


        if department_index >= 0:

            self.from_department.setCurrentIndex(
                department_index
            )


    # ======================================================
    # SAVE TRANSFER
    # ======================================================

    def save_transfer(self):

        equipment_id = (
            self.equipment_combo.currentData()
        )


        if not equipment_id:

            QMessageBox.warning(
                self,
                "Missing Equipment",
                "Please select equipment."
            )

            return


        from_department_id = (
            self.from_department.currentData()
        )


        to_department_id = (
            self.to_department.currentData()
        )


        if not from_department_id:

            QMessageBox.warning(
                self,
                "Missing Department",
                "Please select the source department."
            )

            return


        if not to_department_id:

            QMessageBox.warning(
                self,
                "Missing Department",
                "Please select the destination department."
            )

            return


        if (
            from_department_id ==
            to_department_id
        ):

            QMessageBox.warning(
                self,
                "Invalid Transfer",
                "The source and destination departments "
                "cannot be the same."
            )

            return


        transfer_date = (
            self.transfer_date
            .date()
            .toString(
                "yyyy-MM-dd"
            )
        )


        reason = (
            self.reason
            .toPlainText()
            .strip()
        )


        condition_before = (
            self.condition_before
            .text()
            .strip()
        )


        condition_after = (
            self.condition_after
            .text()
            .strip()
        )


        received_by = (
            self.received_by
            .text()
            .strip()
        )


        status = (
            self.status.currentText()
        )


        remarks = (
            self.remarks
            .toPlainText()
            .strip()
        )


        if not reason:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter the reason for the transfer."
            )

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


            # ==================================================
            # INSERT TRANSFER
            # ==================================================

            cursor.execute(
                """
                INSERT INTO equipment_transfers
                (
                    equipment_id,
                    from_department_id,
                    to_department_id,
                    transfer_date,
                    reason,
                    condition_before,
                    condition_after,
                    authorized_by,
                    transferred_by,
                    received_by,
                    status,
                    remarks
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    equipment_id,
                    from_department_id,
                    to_department_id,
                    transfer_date,
                    reason,
                    condition_before,
                    condition_after,
                    self.user_id,
                    self.user_id,
                    received_by,
                    status,
                    remarks
                )
            )


            # ==================================================
            # UPDATE EQUIPMENT DEPARTMENT
            #
            # Only update the inventory department when the
            # transfer is completed.
            # ==================================================

            if status == "Completed":

                cursor.execute(
                    """
                    UPDATE equipment_inventory
                    SET department_id = %s
                    WHERE equipment_id = %s
                    """,
                    (
                        to_department_id,
                        equipment_id
                    )
                )


            connection.commit()


            QMessageBox.information(
                self,
                "Transfer Saved",
                "Equipment transfer saved successfully."
            )


            self.clear_form()

            self.load_equipment()

            self.load_transfers()


        except Exception as error:

            try:

                connection.rollback()

            except Exception:
                pass


            QMessageBox.critical(
                self,
                "Transfer Error",
                "Could not save the transfer:\n\n"
                + str(error)
            )


        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass


    # ======================================================
    # LOAD TRANSFER HISTORY
    # ======================================================

    def load_transfers(self):

        self.transfer_table.setRowCount(
            0
        )


        connection = get_connection()

        if not connection:

            return


        cursor = None


        try:

            cursor = connection.cursor()


            cursor.execute(
                """
                SELECT

                    et.transfer_id,

                    en.equipment_name,

                    fd.department_name,

                    td.department_name,

                    et.transfer_date,

                    et.reason,

                    COALESCE(
                        su.username,
                        ''
                    ),

                    et.received_by,

                    et.status,

                    et.remarks,

                    et.created_at

                FROM equipment_transfers et


                INNER JOIN equipment_inventory ei
                    ON et.equipment_id =
                       ei.equipment_id


                INNER JOIN equipment_names en
                    ON ei.equipment_name_id =
                       en.equipment_name_id


                INNER JOIN departments fd
                    ON et.from_department_id =
                       fd.department_id


                INNER JOIN departments td
                    ON et.to_department_id =
                       td.department_id


                LEFT JOIN system_users su
                    ON et.transferred_by =
                       su.user_id


                ORDER BY
                    et.transfer_date DESC,
                    et.transfer_id DESC
                """
            )


            records = cursor.fetchall()


            for record in records:

                row = (
                    self.transfer_table.rowCount()
                )


                self.transfer_table.insertRow(
                    row
                )


                for column, value in enumerate(
                    record
                ):

                    if value is None:

                        value = ""


                    item = QTableWidgetItem(
                        str(value)
                    )


                    item.setTextAlignment(
                        Qt.AlignCenter
                    )


                    self.transfer_table.setItem(
                        row,
                        column,
                        item
                    )


        except Exception as error:

            QMessageBox.warning(
                self,
                "Transfer History",
                "Could not load transfer history:\n\n"
                + str(error)
            )


        finally:

            try:

                if cursor:
                    cursor.close()

                connection.close()

            except Exception:
                pass


    # ======================================================
    # CLEAR FORM
    # ======================================================

    def clear_form(self):

        self.equipment_search.clear()


        if self.equipment_combo.count() > 0:

            self.equipment_combo.setCurrentIndex(
                0
            )


        self.transfer_date.setDate(
            QDate.currentDate()
        )


        self.reason.clear()

        self.condition_before.clear()

        self.condition_after.clear()

        self.received_by.clear()

        self.status.setCurrentIndex(
            0
        )

        self.remarks.clear()


        self.show_equipment_information()


    # ======================================================
    # REFRESH
    # ======================================================

    def refresh_data(self):

        self.load_departments()

        self.load_equipment()

        self.load_transfers()


# ==========================================================
# STANDALONE TEST
# ==========================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )


    window = TransferWindow(
        user_id=1,
        username="Admin"
    )


    window.show()


    sys.exit(
        app.exec()
    )