#Discoverability
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from PyQt6.QtCore import Qt
from part3bad import Ui_MainWindow
import sqlite3
from cryptography.fernet import Fernet
from functools import partial

class MainWindow(QMainWindow, Ui_MainWindow):
    connection = sqlite3.connect("password.db")
    cur = connection.cursor()

    if os.path.isfile("secret.key"):
        with open("secret.key", "rb") as file:
            key = file.read()  
    else:
        key = Fernet.generate_key()
        with open("secret.key","wb") as key_file:
            key_file.write(key)
        cur.execute("CREATE TABLE password(id INTEGER PRIMARY KEY AUTOINCREMENT, account, user, password)")
        connection.commit()

        

    cipher_suite = Fernet(key)

    #cur.execute("CREATE TABLE password(id, account, user, password)")
    #cur.execute("INSERT INTO password VALUES ('gmail', 'trevor@gmail.com', '12345')")
    #cur.execute("DELETE FROM password")
    connection.commit()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.encryptButton.clicked.connect(self.encryptButtonPushed)
        self.searchButton.clicked.connect(self.searchButtonPushed)
    
    #handle search button pressed
    def searchButtonPushed(self):
        self.search()

    #handle search button pressed
    def encryptButtonPushed(self):
        self.addRecord()
    
    #handle delete button
    def deleteButtonPushed(self,row):
        self.deleteRecord(row)

    #handle save button
    def saveButtonPushed(self,row, row_index):
        self.saveRecord(row, row_index)
    
    #search function
    def search(self):
        self.tableWidget.setRowCount(0)
        query = self.searchLineEdit.text().lower()
        res = self.cur.execute(f"SELECT id, account, user, password FROM password WHERE account = '{query}'")
        result = res.fetchall()
        self.showResults(result)

    #show results from search()
    def showResults(self, results):
        searchIndex = 0
        for i in results:
            self.tableWidget.insertRow(searchIndex)
            account = i[1]
            user = i[2]
            password = str(self.cipher_suite.decrypt(i[3]).decode())

            self.tableWidget.setItem(searchIndex, 0, QTableWidgetItem(account))
            self.tableWidget.setItem(searchIndex, 1, QTableWidgetItem(user))
            self.tableWidget.setItem(searchIndex, 2, QTableWidgetItem(password))

            saveButton = QPushButton("Save Changes")
            deleteButton = QPushButton("Delete Record")

            deleteButton.clicked.connect(partial(self.deleteButtonPushed, i[0]))
            saveButton.clicked.connect(partial(self.saveButtonPushed, i[0], searchIndex))

            self.tableWidget.setCellWidget(searchIndex, 3, saveButton)
            self.tableWidget.setCellWidget(searchIndex, 4, deleteButton)
            searchIndex += 1
    
    #add new sign in record
    def addRecord(self):
        try:
            #encrypt password: takes the string from the UI, encodes to bytes then encrypts
            password = self.cipher_suite.encrypt(self.passwordLineEdit.text().encode('utf-8'))

            data = [
                (self.accountLineEdit.text(), self.userLineEdit.text(), password)
            ]
            self.cur.executemany("INSERT INTO password (account, user, password) VALUES (?,?,?)", data)
            self.connection.commit()

            #clear editLines
            self.accountLineEdit.clear()
            self.userLineEdit.clear()
            self.passwordLineEdit.clear()
        except ValueError:
            print("value error")
    
    #delete record
    def deleteRecord(self,row):
        self.cur.execute(f"DELETE FROM password WHERE id = {row}")
        self.connection.commit()
        self.search()
    
    #save record
    def saveRecord(self,record_id, row):
        accountItem = self.tableWidget.item(row,0)
        userItem = self.tableWidget.item(row,1)
        passwordItem = self.tableWidget.item(row,2)

        account = accountItem.text() if accountItem else ""
        user = userItem.text() if userItem else ""
        password = passwordItem.text() if passwordItem else ""

        passwordEncrypted = self.cipher_suite.encrypt(password.encode("utf-8"))

        self.cur.execute(f"UPDATE password SET account = ?, user = ?, password = ? WHERE id = ?", (account, user, passwordEncrypted, record_id))
        self.connection.commit()
        self.search()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())