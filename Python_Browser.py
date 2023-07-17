import sys
import os
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# Check if database file has write permission
filename = 'my_history.db'
if os.access(filename, os.W_OK):
    print("File has write permission")
else:
    print("File does not have write permission")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the browser view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Set up the navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        history_btn = QAction('History', self)
        history_btn.triggered.connect(self.view_history)
        navbar.addAction(history_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Connect to the database and create history table if it doesn't exist
        self.conn = sqlite3.connect('my_history.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS my_history
                            (id INTEGER PRIMARY KEY,
                             url TEXT NOT NULL,
                             date_time TEXT NOT NULL);''')
        self.conn.commit()

    def navigate_home(self):
        self.browser.setUrl(QUrl('http://google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))


    def update_url(self, q):
        self.url_bar.setText(q.toString())
        url = q.toString()
        date_time = QDateTime.currentDateTime().toString(Qt.ISODate)

        try:
            # Insert the URL and current date time into the database
            self.cur.execute("INSERT INTO my_history(url, date_time) VALUES (?, ?)", (url, date_time))
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting into database: {str(e)}")

    def view_history(self):
        # Retrieve URLs and date times from the history table in descending order of date time
        self.cur.execute("SELECT url, date_time FROM my_history ORDER BY date_time DESC")
        history_list = [f"{row[0]} ({row[1]})" for row in self.cur.fetchall()]

        # Create a dialog to display the history list
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle('History')
        history_dialog_layout = QVBoxLayout()
        history_dialog.setLayout(history_dialog_layout)

        # Create a list widget to display the history list
        history_list_widget = QListWidget()
        for url in history_list:
            history_list_widget.addItem(url)

        history_dialog_layout.addWidget(history_list_widget)
        history_dialog.setMinimumSize(600, 400)
        history_dialog.exec_()
    
def view_history(self):
    # Retrieve URLs and date times from the history table in descending order of date time
    self.cur.execute("SELECT url, date_time FROM my_history ORDER BY date_time DESC")
    history_list = [f"{row[0]} ({row[1]})" for row in self.cur.fetchall()]

    # Create a dialog to display the history list
    history_dialog = QDialog(self)
    history_dialog.setWindowTitle('History')
    history_dialog_layout = QVBoxLayout()
    history_dialog.setLayout(history_dialog_layout)

    # Create a list widget to display the history list
    history_list_widget = QListWidget()
    history_list_widget.setMinimumSize(1280, 720)
    history_list_widget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
    for url in history_list:
        history_list_widget.addItem(url)

    #history_list_widget.setMinimumSize(history_list_widget.sizeHint())  # Set the minimum size hint to the current size of the widget
    history_dialog_layout.addWidget(history_list_widget)
    history_dialog.setMinimumSize(1280, 720)
    history_dialog.exec_()


    def closeEvent(self, event):
        # Close the database connection when the window is closed
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName('My Cool Browser')
    window = MainWindow()
    app.exec_()
