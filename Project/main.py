import sys
from PyQt5.QtWidgets import QApplication
from GraphicForm import Form


if __name__ == "__main__":
    app = QApplication([])
    main_form = Form()
    sys.exit(app.exec_())
