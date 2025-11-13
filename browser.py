#!/usr/bin/env python3
import sys
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar,
    QAction, QStatusBar, QFileDialog
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MiniBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gabriel’s Mini Browser")
        self.setMinimumSize(1000, 700)

        # Create the web view
        self.view = QWebEngineView()
        self.setCentralWidget(self.view)

        # Load google by default
        self.view.setUrl(QUrl("https://www.google.com/"))

        # Navigation toolbar
        nav_bar = QToolBar()
        nav_bar.setMovable(False)
        self.addToolBar(nav_bar)

        # Back button
        back_btn = QAction("←", self)
        back_btn.setStatusTip("Go back")
        back_btn.triggered.connect(self.view.back)
        nav_bar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("→", self)
        forward_btn.setStatusTip("Go forward")
        forward_btn.triggered.connect(self.view.forward)
        nav_bar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("⟳", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.view.reload)
        nav_bar.addAction(reload_btn)

        # Home button
        home_btn = QAction("🏠", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.go_home)
        nav_bar.addAction(home_btn)

        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL or file path...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        # Open file button
        open_file_btn = QAction("📁", self)
        open_file_btn.setStatusTip("Open local HTML file")
        open_file_btn.triggered.connect(self.open_file)
        nav_bar.addAction(open_file_btn)

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Connect events
        self.view.urlChanged.connect(self.update_url_bar)
        self.view.loadProgress.connect(self.show_progress)

    def go_home(self):
        self.view.setUrl(QUrl("https://www.google.com/"))

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url:
            return
        if not url.startswith(("http://", "https://", "file://")):
            url = "http://" + url
        self.view.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open HTML file", "", "HTML Files (*.html *.htm)"
        )
        if file_path:
            self.view.setUrl(QUrl.fromLocalFile(file_path))

    def show_progress(self, progress):
        self.status.showMessage(f"Loading... {progress}%")


def main():
    app = QApplication(sys.argv)
    window = MiniBrowser()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
