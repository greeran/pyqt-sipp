from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sipp_user
from multiprocessing import Queue
from sipp_log import Sipp_Element
import time
from queue import Empty

class sippThread(QThread):
    def __init__(self, q, add_trigger):
        QThread.__init__(self)
        self.q = q
        self.add_trigger = add_trigger
        self.isTerminate = False

    def __del__(self):
        self.wait

    def run(self):
        while self.isTerminate is False:
            try:
                sipp_out=self.q.get(timeout=1)
                if len(str(sipp_out)) > 20:
                    self.add_trigger.emit(sipp_out)
            except Empty:
                print("is empty and isTerm = %d " % self.isTerminate)
                continue

    def endThread(self):
        self.isTerminate = True     
    
class TextWindow(QMainWindow):
    add_trigger = pyqtSignal(Sipp_Element)

    def __init__(self):
        QMainWindow.__init__(self)

        self.plaintextedit = QPlainTextEdit()
        self.plaintextedit.setPlaceholderText("This is some placeholder text.")
        layout = QGridLayout()
        layout.addWidget(self.plaintextedit, 0, 0)

        self.widget = QWidget()
        self.widget.setLayout(layout)
 
        self.setCentralWidget(self.widget)
        self.nextLineClear = False

    def add_output(self, emlt):
        self.plaintextedit.clear()    
        lines = str(emlt).split("\\n")
        for line in lines:
            self.plaintextedit.appendPlainText(line)    

    def run_sipp_thread(self):
        self._sipp_thread = sippThread(self.q, self.add_trigger)
        self.add_trigger.connect(self.add_output)
        self._sipp_thread.start()
    
    def endSipp(self):
        self._sipp_thread.endThread()
        self.plaintextedit.appendPlainText("finished test")
        self.sipp_Clnt.stop_sipp()
        self._sipp_thread.wait()

    def run_proc(self, cmd):
        self.sipp_Clnt, self.q = sipp_user.createSippAnswer(cmd)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = TextWindow()
    screen.show()
    sys.exit(app.exec_())