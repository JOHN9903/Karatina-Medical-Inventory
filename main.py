import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from PySide6.QtWidgets import QApplication

from screens.login import LoginWindow


def main():

    app = QApplication(
        sys.argv
    )

    window = LoginWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()