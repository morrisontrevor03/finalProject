import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
import requests
import json
from part4bad import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        rowPosition = self.paramTable.rowCount()
        self.setWindowTitle("API Tester/Sandbox")
        self.addParameterButton.clicked.connect(self.onAddRowClicked)
        self.removeParameterButton.clicked.connect(self.onRemoveRowClicked)
        self.goButton.clicked.connect(self.onGoButtonClicked)
    
    def create_error_message(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error")
        msg.setText("An error occurred!")
        msg.setInformativeText(message)
        msg.exec()

    #handle adding rows
    def addRow(self):
        rowPosition = self.paramTable.rowCount()
        self.paramTable.insertRow(rowPosition)
    
    #handle removing rows
    def removeRow(self):
        rowPosition = self.paramTable.rowCount() - 1
        self.paramTable.removeRow(rowPosition)

    #add row button
    def onAddRowClicked(self):
        self.addRow()
    
    #remove row button
    def onRemoveRowClicked(self):
        self.removeRow()
    
    #handle 'go' button
    def onGoButtonClicked(self):
        try:
            if self.requestTypeComboBox.currentText() == "POST":
                self.makePostRequest()
            elif self.requestTypeComboBox.currentText() == "GET":
                self.makeGetRequest()
        except ValueError:
            self.create_error_message("Value Error")

    #this builds the request string that gets sent to the API
    def makePostRequest(self):
        try:
            url = self.hostLineEdit.text()
            if self.keyLineEdit.text() is None:
                header = {
                    "Content-Type": "application/json",
                }
            else:
                header = {
                    "Content-Type": "application/json",
                    "X-API-Key": self.keyLineEdit.text()
                }
            
            data = {}
            for i in range(self.paramTable.rowCount()):
                key = self.paramTable.item(i, 0).text()
                value = self.paramTable.item(i,1).text()
                data[key] = value
            print(url,header,data)
            response = requests.post(url, headers = header, data = json.dumps(data))
            print(response)
        except ValueError:
            print("value error")
    
    def makeGetRequest(self):
        try:
            url = self.hostLineEdit.text()
            if self.keyLineEdit.text() is None:
                header = {
                    "Content-Type": "application/json",
                }
            else:
                header = {
                    "Content-Type": "application/json",
                    "X-API-Key": self.keyLineEdit.text()
                }
            response = requests.get(url, headers = header)
            print(response.text)
            self.responseBrowser.setText(response.text)
        except ValueError:
            print("value error")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())