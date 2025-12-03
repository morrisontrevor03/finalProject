#feedback
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
import requests
import json
from part4good import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        rowPosition = self.paramTable.rowCount()
    
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

    def setStatus(self, code):
        print(code)
        statuses = {
            "100": "The client should continue with its request",
            "200": "The request was successful",
            "201": "The request has been fulfilled and a new resource was created",
            "204": "The server succesfully processed the request but is not returning any content",
            "301": "The resource has permanently moved",
            "302": "The resource has temporarily moved to a different URI",
            "304": "The resource has not been modified since the last requeust",
            "400": "The server cannot process the request due to a client error. Please double check your inputs.",
            "401": "The request requires user authentication. Ensure your API key is correct.",
            "403": "The server understood the request but refuses to authorize it",
            "404": "The server cannot find the requested resource. Please double check that the endpoint exists and is entered correctly",
            "500": "Internal Servor Error",
            "502": "The server acted as a gateway or proxy and received an invalid response from an upstream server",
            "503": "Service unavailable. The server is currently down."
        }

        if code in statuses:
            self.statusCode.setText(code)
            self.statusExplanation.setText(statuses[code])

        if code.startswith("2"):
            self.statusCode.setStyleSheet("QLabel {color: green}")
        elif code.startswith("1"):
            self.statusCode.setStyleSheet("QLabel {color: yellow}")
        elif code.startswith("3"):
            self.statusCode.setStyleSheet("QLabel {color: blue}")
        elif code.startswith("4"):
            self.statusCode.setStyleSheet("QLabel {color: orange}")
        else:
            self.statusCode.setStyleSheet("QLabel {color: red}")

    #this builds the request string that gets sent to the API
    def makePostRequest(self):
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
        self.setStatus(str(response.status_code))
        print(response)
        print(response.status_code)
    
    def makeGetRequest(self):
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
        self.setStatus(str(response.status_code))
        print(response.text)
        print(response.status_code)
        self.responseBrowser.setText(response.text)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())