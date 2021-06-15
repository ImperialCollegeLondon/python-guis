import sys
from PySide2 import QtWidgets

if sys.platform == "darwin":
    # There is an issue with pyside2 and MacOS BigSur. This hack sorts it
    # https://stackoverflow.com/a/64878899/3778792
    import os

    os.environ["QT_MAC_WANTS_LAYER"] = "1"


def on_button_clicked():
    return "Hello Pythoners!"


class MySimpleGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("")

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.text)

        self.button.clicked.connect(self._on_button_clicked)

    def _on_button_clicked(self):
        self.text.setText(on_button_clicked())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    gui = MySimpleGUI()
    gui.show()

    sys.exit(app.exec_())
