import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import QDir
from PyQt5.Qt import QDesktopServices
import platform
from PyQt5.QtCore import QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        home_path = os.path.expanduser("~")
        self.model = QFileSystemModel()
        self.tree_view = QTreeView()

        try:
            self.model.setRootPath(home_path)
        except OSError as e:
            print(f"Error: {e}")
            home_path = '/'
            self.model.setRootPath(home_path)

        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)

        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(home_path))
        self.tree_view.doubleClicked.connect(self.open_file_or_directory)

        self.filter_input = QLineEdit()
        self.filter_input.textChanged.connect(self.filter_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.filter_input)
        layout.addWidget(self.tree_view)

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setWindowTitle("File System Explorer")
        self.setGeometry(100, 100, 800, 600)

        self.setCentralWidget(main_widget)

    def filter_changed(self, text):
        self.model.setNameFilters([f"*{text}*"])
        self.model.setNameFilterDisables(False)

    def open_file_or_directory(self, index):
        file_info = self.model.fileInfo(index)
        file_path = file_info.filePath()
        if file_info.isFile():
            if platform.system() == 'Windows':
                os.system(f'start "" "{file_path}"')
            else:
                url = QUrl.fromLocalFile(file_path)
                QDesktopServices.openUrl(url)
        elif file_info.isDir():
            self.tree_view.setRootIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
