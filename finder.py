import sys, webbrowser, os
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem

from struct import unpack, error
import socket

def find_data_file(filename):
    """
        Used to get finder.ui when frozen by cx_Freeze
    """
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


class BCSFinder(QObject):
    """
        Class to interact with the BCS over UDP
    """
    found = pyqtSignal([dict])
    
    def __init__(self):
        super(BCSFinder, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        self.sock.bind(('', 4111))

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            try:
                bcs_info = unpack("BBBBB4B6B4c31s31s2cc", data)
                self.found.emit({
                    "address": addr[0],
                    "name": bcs_info[19].decode(encoding='UTF-8').strip(),
                    "type": "BCS-46{}".format(bcs_info[3]),
                    "version": "{}.{}.{}".format(bcs_info[16].decode(encoding='UTF-8'), 
                        bcs_info[17].decode(encoding='UTF-8'), 
                        bcs_info[18].decode(encoding='UTF-8')),
                    "mac": "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(bcs_info[9], bcs_info[10], 
                        bcs_info[11], bcs_info[12], bcs_info[13], bcs_info[14])
                })
            except error:
                pass

    @pyqtSlot()
    def ping(self):
        self.sock.sendto(b"\xff\x04\x02\xfb", ("<broadcast>", 4111))

class FinderUi(QWidget):
    """
        User Interface functions
    """
    def __init__(self):
        super(FinderUi, self).__init__()

        # Load UI file from Qt Designer
        uic.loadUi(find_data_file("finder.ui"), self)        
        
        # Setup the UDP listener in it's own thread
        self.finder = BCSFinder()
        self.thread = QThread()
        self.finder.moveToThread(self.thread)
        self.thread.started.connect(self.finder.listen)
        self.thread.finished.connect(app.exit)
        self.thread.start()
        
        # Connect to slots
        self.pushButton.clicked.connect(self.ping)
        self.finderTable.cellDoubleClicked.connect(self.open)
        self.finder.found.connect(self.located)
        

    def ping(self):
        # Clear table
        while(self.finderTable.rowCount() > 0):
            self.finderTable.removeRow(0)

        # Send ping
        self.finder.ping()
    
    def open(self, row, col):
        # When double clicked, open default web browser to the BCS
        webbrowser.open('http://{}/'.format(self.finderTable.item(row, 0).text()))
        
    def located(self, bcs):
        # Found a BCS, add a row to the table
        row = self.finderTable.rowCount()
        self.finderTable.insertRow(row)
        self.finderTable.setItem(row, 0, QTableWidgetItem(bcs['address']))
        self.finderTable.setItem(row, 1, QTableWidgetItem(bcs['name']))
        self.finderTable.setItem(row, 2, QTableWidgetItem(bcs['mac']))
        self.finderTable.setItem(row, 3, QTableWidgetItem(bcs['version']))
        self.finderTable.setItem(row, 4, QTableWidgetItem(bcs['type']))
        self.finderTable.resizeColumnsToContents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = FinderUi()
    f.show()
    sys.exit(app.exec_())