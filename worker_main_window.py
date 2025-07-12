import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QFormLayout,
    QLineEdit, QComboBox, QMessageBox
)

class AccountManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('إدارة حسابات تويتر')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['المعرف', 'اسم المستخدم', 'البريد الإلكتروني', 'كلمة المرور', 'نوع الحساب'])
        self.layout.addWidget(self.table)

        self.add_button = QPushButton('إضافة حساب')
        self.add_button.clicked.connect(self.add_account)
        self.layout.addWidget(self.add_button)

        self.edit_button = QPushButton('تعديل حساب')
        self.edit_button.clicked.connect(self.edit_account)
        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton('حذف حساب')
        self.delete_button.clicked.connect(self.delete_account)
        self.layout.addWidget(self.delete_button)

        self.load_accounts()

    def load_accounts(self):
        self.table.setRowCount(0)
        conn = sqlite3.connect('twitter_accounts.db')
        c = conn.cursor()
        c.execute("SELECT * FROM accounts")
        accounts = c.fetchall()
        for row_num, row_data in enumerate(accounts):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        conn.close()

    def add_account(self):
        dialog = AccountDialog()
        if dialog.exec_():
            username = dialog.username.text()
            email = dialog.email.text()
            password = dialog.password.text()
            account_type = dialog.account_type.currentText()

            conn = sqlite3.connect('twitter_accounts.db')
            c = conn.cursor()
            c.execute("INSERT INTO accounts (username, email, password, account_type) VALUES (?, ?, ?, ?)",
                      (username, email, password, account_type))
            conn.commit()
            conn.close()
            self.load_accounts()

    def edit_account(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'خطأ', 'الرجاء تحديد حساب لتعديله.')
            return

        account_id = self.table.item(selected_row, 0).text()
        username = self.table.item(selected_row, 1).text()
        email = self.table.item(selected_row, 2).text()
        password = self.table.item(selected_row, 3).text()
        account_type = self.table.item(selected_row, 4).text()

        dialog = AccountDialog(username, email, password, account_type)
        if dialog.exec_():
            new_username = dialog.username.text()
            new_email = dialog.email.text()
            new_password = dialog.password.text()
            new_account_type = dialog.account_type.currentText()

            conn = sqlite3.connect('twitter_accounts.db')
            c = conn.cursor()
            c.execute("UPDATE accounts SET username=?, email=?, password=?, account_type=? WHERE id=?",
                      (new_username, new_email, new_password, new_account_type, account_id))
            conn.commit()
            conn.close()
            self.load_accounts()

    def delete_account(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'خطأ', 'الرجاء تحديد حساب لحذفه.')
            return

        account_id = self.table.item(selected_row, 0).text()
        conn = sqlite3.connect('twitter_accounts.db')
        c = conn.cursor()
        c.execute("DELETE FROM accounts WHERE id=?", (account_id,))
        conn.commit()
        conn.close()
        self.load_accounts()

class AccountDialog(QDialog):
    def __init__(self, username='', email='', password='', account_type=''):
        super().__init__()
        self.setWindowTitle('إضافة/تعديل حساب')
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.username = QLineEdit(username)
        self.email = QLineEdit(email)
        self.password = QLineEdit(password)
        self.password.setEchoMode(QLineEdit.Password)
        self.account_type = QComboBox()
        self.account_type.addItems(['رئيسي', 'فرعي'])
        self.account_type.setCurrentText(account_type)

        self.layout.addRow('اسم المستخدم:', self.username)
        self.layout.addRow('البريد الإلكتروني:', self.email)
        self.layout.addRow('كلمة المرور:', self.password)
        self.layout.addRow('نوع الحساب:', self.account_type)

        self.add_button = QPushButton('حفظ')
        self.add_button.clicked.connect(self.accept)
        self.layout.addWidget(self.add_button)


class InteractionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('مهمة جديدة')
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.accounts_list = QComboBox()
        self.layout.addRow('الحسابات:', self.accounts_list)

        self.interaction_type = QComboBox()
        self.interaction_type.addItems(['إعجاب', 'إعادة تغريد', 'تعليق'])
        self.layout.addRow('نوع التفاعل:', self.interaction_type)

        self.comment_text = QLineEdit()
        self.layout.addRow('نص التعليق:', self.comment_text)

        self.execute_button = QPushButton('تنفيذ المهمة')
        self.execute_button.clicked.connect(self.accept)
        self.layout.addWidget(self.execute_button)


class TweetsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('التغريدات')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['التغريدة', ''])
        self.layout.addWidget(self.table)

        self.load_tweets()

    def load_tweets(self):
        # In a real application, you would fetch tweets from the API
        tweets = [{'text': 'هذه تغريدة تجريبية'}, {'text': 'تغريدة أخرى'}]
        self.table.setRowCount(len(tweets))
        for row_num, tweet in enumerate(tweets):
            self.table.setItem(row_num, 0, QTableWidgetItem(tweet['text']))
            button = QPushButton('مهمة جديدة')
            button.clicked.connect(self.open_interactions_dialog)
            self.table.setCellWidget(row_num, 1, button)

    def open_interactions_dialog(self):
        dialog = InteractionsDialog(self)
        dialog.exec_()


class PostWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setWindowTitle('نشر تغريدة')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tweet_text = QLineEdit()
        self.layout.addWidget(self.tweet_text)

        self.post_button = QPushButton('نشر')
        self.post_button.clicked.connect(self.post_tweet)
        self.layout.addWidget(self.post_button)

    def post_tweet(self):
        text = self.tweet_text.text()
        if not text:
            QMessageBox.warning(self, 'خطأ', 'الرجاء إدخال نص للتغريدة.')
            return
        # In a real application, you would select the main account
        # self.client.create_tweet(text)
        print(f'Posting tweet: {text}')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('برنامج إدارة حسابات تويتر')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.account_manager = AccountManager()
        self.layout.addWidget(self.account_manager)

        self.tweets_widget = TweetsWidget()
        self.layout.addWidget(self.tweets_widget)

        # In a real application, you would initialize the client and log in
        self.post_widget = PostWidget(None)
        self.layout.addWidget(self.post_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
