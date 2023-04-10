import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
import sqlite3
from hashlib import sha256

class RegisterWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 300, 200)
        
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.username_label)
        hbox1.addWidget(self.username_input)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.password_label)
        hbox2.addWidget(self.password_input)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.register_button)
        
        self.setLayout(vbox)
    
    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        if user:
            QMessageBox.warning(self, "Register Error", "User already exists.")
        else:
            password_hash = sha256(password.encode()).hexdigest()
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password_hash))
            conn.commit()
            QMessageBox.information(self, "Register Success", "User registered successfully.")
            self.username_input.setText("")
            self.password_input.setText("")


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
        
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_user)
        
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.username_label)
        hbox1.addWidget(self.username_input)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.password_label)
        hbox2.addWidget(self.password_input)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.login_button)
        
        self.setLayout(vbox)
    
    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        if user:
            password_hash = sha256(password.encode()).hexdigest()
            if password_hash == user[1]:
                self.close()
                self.user_dashboard = UserDashboard(username)
                self.user_dashboard.show()
            else:
                QMessageBox.warning(self, "Login Error", "Invalid password.")
        else:
            QMessageBox.warning(self, "Login Error", "User does not exist.")
    

class UserDashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("User Dashboard")
        self.setGeometry(100, 100, 300, 200)

        self.welcome_label = QLabel(f"Welcome, {username}!")
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout_user)

        vbox = QVBoxLayout()
        vbox.addWidget(self.welcome_label)
        vbox.addWidget(self.logout_button)

        self.setLayout(vbox)

    def logout_user(self):
        self.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("User Registration and Login System")
        self.setGeometry(100, 100, 300, 200)
        
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.open_register_widget)
    
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.open_login_widget)
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.register_button)
        hbox.addWidget(self.login_button)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)

    def open_register_widget(self):
        self.register_widget = RegisterWidget()
        self.register_widget.show()

    def open_login_widget(self):
        self.login_widget = LoginWidget()
        self.login_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())