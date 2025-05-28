import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Ocean")
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        self.navtb = QToolBar("Navigation")
        self.navtb.setIconSize(self.style().standardIcon(QStyle.SP_BrowserReload).actualSize(self.browser.size()))
        self.addToolBar(self.navtb)

        self.back_btn = QAction(self.style().standardIcon(QStyle.SP_ArrowBack), "Back", self)
        self.back_btn.setStatusTip("Back to previous page")
        self.back_btn.setShortcut("Alt+Left")
        self.back_btn.triggered.connect(self.browser.back)
        self.navtb.addAction(self.back_btn)

        self.forward_btn = QAction(self.style().standardIcon(QStyle.SP_ArrowForward), "Forward", self)
        self.forward_btn.setStatusTip("Forward to next page")
        self.forward_btn.setShortcut("Alt+Right")
        self.forward_btn.triggered.connect(self.browser.forward)
        self.navtb.addAction(self.forward_btn)

        self.reload_btn = QAction(self.style().standardIcon(QStyle.SP_BrowserReload), "Reload", self)
        self.reload_btn.setStatusTip("Reload current page")
        self.reload_btn.setShortcut("Ctrl+R")
        self.reload_btn.triggered.connect(self.browser.reload)
        self.navtb.addAction(self.reload_btn)

        self.home_btn = QAction(self.style().standardIcon(QStyle.SP_DirHomeIcon), "Home", self)
        self.home_btn.setStatusTip("Go to Home Page")
        self.home_btn.setShortcut("Alt+H")
        self.home_btn.triggered.connect(self.navigate_home)
        self.navtb.addAction(self.home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setPlaceholderText("Enter URL here...")
        self.navtb.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(150)
        self.status.addPermanentWidget(self.progress)

        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadFinished.connect(self.load_finished)

        self.setStyleSheet("""
            QWebEngineView{
                background: #00FFDE;           
            }
            QToolBar {
                background: #00CAFF;
                padding: 5px;
            }
            QLineEdit {
                padding: 5px;
                font-size: 14px;
                border: 2px solid #0065F8;
                border-radius: 10px;
            }
            QMainWindow {
                background-color: #00FFDE;
            }
        """)

     
        self.showMaximized()

    def update_progress(self, progress):
        """Update the progress bar during page load."""
        self.progress.setValue(progress)
        if progress < 100:
            self.status.showMessage(f"Loading... {progress}%")
        else:
            self.status.showMessage("Page loaded", 2000)

    def load_finished(self):
        """Reset the progress bar after loading is complete."""
        self.progress.setValue(0)

    def navigate_home(self):
        """Navigate to the homepage."""
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        """Navigate to the URL entered by the user. Auto-corrects URL if scheme is missing."""
        url_text = self.url_bar.text().strip()
        if not (url_text.startswith("http://") or url_text.startswith("https://")):
            url_text = "http://" + url_text
        self.browser.setUrl(QUrl(url_text))

    def update_url(self, qurl):
        """Update the URL bar to match the browser's current URL."""
        self.url_bar.setText(qurl.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Ocean")
    window = MainWindow()
    sys.exit(app.exec_())


