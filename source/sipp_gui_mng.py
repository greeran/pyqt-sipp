#!/usr/bin/env python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import time
import json
from sipp_textedit import TextWindow
from LineeditValidate import QLineEditPort, QLineEditIP, QLineEditFile, QLineEditStub

answer_command = "d:\\cgwin-64\\Sipp_3.2\\sipp.exe -r 1 -rp 1 -sf C:\\sipp\\answer.xml -i [172.17.125.12] -p 5090  -default_behaviors -bye"
#call_command = "d:\\cgwin-64\\Sipp_3.2\\sipp.exe -r 1 -rp 1 -sf C:\\sipp\\answer.xml -i [172.17.125.12] -p 5080  -default_behaviors -bye"
#answer_command = "d:\\cgwin-64\\Sipp_3.2\\sipp.exe -r 1 -rp 1 -sf C:\\sipp\\answer.xml -i [192.168.43.25] -p 5070  -default_behaviors -bye"
call_command = "d:\\cgwin-64\\Sipp_3.2\\sipp.exe 172.17.125.126 -rp 1 -r 100 -l 892 -sf C:\\sipp\\calling_dSec.xml -i [172.17.125.12] -p 5070  -trace_err  -default_behaviors -bye"

class MngWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.lableToTextMap = {}
        layout = QGridLayout()
        
        #general configuration
        generalBox = QGroupBox("General Configuration")
        generalBox.setCheckable(False)
        generalLayout=QGridLayout()
        generalBox.setLayout(generalLayout)

        SIPPFileLable = QLabel("SIPP path")
        self.SIPPFileText = QLineEditFile()
        self.SIPPFileText.setToolTip(SIPPFileLable.text())
        self.lableToTextMap[self.SIPPFileText.toolTip()]=self.SIPPFileText
        sippFileBtn = QToolButton()
        sippFileBtn.setText("...")
        sippFileBtn.clicked.connect(lambda: self.fileBtnClk(self.SIPPFileText, "*.exe"))
        

        TargeIpLable = QLabel("Target Ip")
        self.TargetIpText = QLineEditIP()
        self.TargetIpText.setToolTip(TargeIpLable.text())
        self.lableToTextMap[self.TargetIpText.toolTip()]=self.TargetIpText
        
        generalLayout.addWidget(SIPPFileLable, 0, 0)
        generalLayout.addWidget(self.SIPPFileText,  0, 1)
        generalLayout.addWidget(TargeIpLable, 1, 0)
        generalLayout.addWidget(self.TargetIpText,  1, 1)
        generalLayout.addWidget(sippFileBtn, 0, 6)

        #answer configuration
        answerBox = QGroupBox("Answer Configuration")
        answerBox.setCheckable(False)
        answerLayout=QGridLayout()
        answerBox.setLayout(answerLayout)

        AnswerFileLbl = QLabel("Answer File")
        self.AnswerFileText = QLineEditFile()
        self.AnswerFileText.setToolTip(AnswerFileLbl.text())
        
        anserFileBtn = QToolButton()
        anserFileBtn.setText("...")
        anserFileBtn.clicked.connect(lambda: self.fileBtnClk(self.AnswerFileText, "*.xml"))
        
        AnswerPortLbl = QLabel("Answer Port")
        self.AnswerPortText = QLineEditPort()
        self.AnswerPortText.setToolTip(AnswerPortLbl.text())
        self.lableToTextMap[self.AnswerFileText.toolTip()]=self.AnswerFileText
        self.lableToTextMap[self.AnswerPortText.toolTip()]=self.AnswerPortText


        answerLayout.addWidget(AnswerFileLbl, 0, 0)
        answerLayout.addWidget(self.AnswerFileText,  0, 1)
        answerLayout.addWidget(AnswerPortLbl, 1, 0)
        answerLayout.addWidget(self.AnswerPortText,  1, 1)
        answerLayout.addWidget(anserFileBtn, 0, 6)

        #caller Configuration        []
        callBox = QGroupBox("Call Configuration")
        callBox.setCheckable(False)
        callLayout = QGridLayout()
        callBox.setLayout(callLayout)

        CallFileLbl = QLabel("Call File")
        self.CallFileText = QLineEditFile()
        self.CallFileText.setToolTip(CallFileLbl.text())
        callerFileBtn = QToolButton()
        callerFileBtn.setText("...")
        callerFileBtn.clicked.connect(lambda: self.fileBtnClk(self.CallFileText, "*.xml"))
        
        CallPpSLbl = QLabel("Packets per Sec")
        self.CallPpSText = QLineEditStub()
        self.CallPpSText.setToolTip(CallPpSLbl.text())
        CallIpLbl = QLabel("Call IP")
        self.CallIpText = QLineEditIP()
        self.CallIpText.setToolTip(CallIpLbl.text())
        CallPortLbl = QLabel("Call Port")
        self.CallPortText = QLineEditPort()
        self.CallPortText.setToolTip(CallPortLbl.text())
        
        self.lableToTextMap[self.CallFileText.toolTip()]=self.CallFileText
        self.lableToTextMap[self.CallPpSText.toolTip()]=self.CallPpSText
        self.lableToTextMap[self.CallIpText.toolTip()]=self.CallIpText
        self.lableToTextMap[self.CallPortText.toolTip()]=self.CallPortText

        callLayout.addWidget(CallFileLbl, 0, 0)
        callLayout.addWidget(self.CallFileText,  0, 1)
        callLayout.addWidget(CallPpSLbl, 1, 0)
        callLayout.addWidget(self.CallPpSText,  1, 1)
        callLayout.addWidget(CallIpLbl, 2, 0)
        callLayout.addWidget(self.CallIpText,  2, 1)
        callLayout.addWidget(CallPortLbl, 2, 2)
        callLayout.addWidget(self.CallPortText,  2, 3)
        callLayout.addWidget(callerFileBtn, 0, 6)

        #actions 
        actionBox = QGroupBox("")
        actionBox.setCheckable(False)
        actionLayout = QGridLayout()
        actionBox.setLayout(actionLayout)

        self.button = QPushButton("Start Ssip")
        self.buttonEnd = QPushButton("Stop Ssip")
        
        actionLayout.addWidget(self.button,0,0)
        actionLayout.addWidget(self.buttonEnd,0,1)
        
        toolbar = QToolBar()
        toolbutton = QToolButton()
        toolbutton.setText("Save Setup")
        toolbutton.setCheckable(True)
        toolbutton.setAutoExclusive(True)
        toolbutton.clicked.connect(self.on_button_save)
        toolbar.addWidget(toolbutton)
        
        toolbutton1 = QToolButton()
        toolbutton1.setText("Load Setup")
        toolbutton1.setCheckable(True)
        toolbutton1.setAutoExclusive(True)
        toolbutton1.clicked.connect(self.on_button_load)
        toolbar.addWidget(toolbutton1)

        layout.addWidget(toolbar)
        layout.addWidget(generalBox,1,0)
        layout.addWidget(answerBox,2,0)
        layout.addWidget(callBox,3,0)
        layout.addWidget(actionBox,4,0)

        #layout.addWidget(self.button, 1, 0) 
        #layout.addWidget(self.buttonEnd, 1, 1)  

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        self.button.clicked.connect(self.on_button_clicked)
        self.buttonEnd.clicked.connect(self.on_button_end)

        self.on_button_load()

    def createCmdStrings(self):
        #"d:\\cgwin-64\\Sipp_3.2\\sipp.exe -r 1 -rp 1 -sf C:\\sipp\\answer.xml -i [172.17.125.12] -p 5090  -default_behaviors -bye"
        #"d:\\cgwin-64\\Sipp_3.2\\sipp.exe 172.17.125.126 -rp 1 -r 100 -l 892 
        # -sf C:\\sipp\\calling_dSec.xml -i [172.17.125.12] -p 5070  -trace_err  -default_behaviors -bye"
        self.answerCmd = "d:\\cgwin-64\\Sipp_3.2\\sipp.exe -r 1 -rp 1 -sf "+\
            self.AnswerFileText.text()+" -i ["+self.TargetIpText.text(),"] -p "+\
            self.AnswerPortText.text()+ " -default_behaviors -bye"
        self.callerCmd = "d:\\cgwin-64\\Sipp_3.2\\sipp.exe "+self.CallIpText.text()+\
            " -r 1 -rp "+self.CallPpSText.text()+\
            " -l 892 -sf "+self.CallFileText.text()+" -i [",self.TargetIpText.text()+"] -p"+\
            self.CallPortText.text()+ " -trace_err  -default_behaviors -bye"

    def validateParams(self):
        errorArray = []
        for key, value in self.lableToTextMap.items():
            isValidate, erroStr = value.Validate()
            if isValidate is False:
                errorArray.append(erroStr)
        if not errorArray:
            return True
        else:
            QMessageBox.warning(self, "warning", '\n'.join(errorArray))
            #error_dialog = QErrorMessage()
            #error_dialog.showMessage(''.join(errorArray),QMessageBox.Ok)
            return False


    def on_button_clicked(self):
        if self.validateParams() is False:
            return
        self.createCmdStrings()
        print(self.callerCmd)
        print(self.answerCmd)
        self.textwindow_answer = TextWindow()
        self.textwindow_answer.show()
        self.textwindow_answer.run_proc(self.answerCmd)
        self.textwindow_answer.run_sipp_thread()
        time.sleep(1)
        self.textwindow_call = TextWindow()
        self.textwindow_call.show()
        self.textwindow_call.run_proc(self.callerCmd)
        self.textwindow_call.run_sipp_thread()
        
    def on_button_end(self):
        self.textwindow_answer.endSipp()
        self.textwindow_answer.close()
        self.textwindow_call.endSipp()
        self.textwindow_call.close()

    def on_button_save(self):
        jsonObj = {}
        for key, value in self.lableToTextMap.items():
            jsonObj[key]=value.text()
        try:
            with open("sipp_config.json","w") as write_file:
                json.dump(jsonObj , write_file)
        except:
            print("failed to save config")

    def on_button_load(self):
        print("in load file")
        try:
            with open("sipp_config.json","r") as read_file:
                jsonObj=json.load(read_file)
                for key, value in jsonObj.items():
                    self.lableToTextMap[key].setText(value)
        except FileNotFoundError:
            print("config file not found")
        except:
            print("failed to load config")
            
    def fileBtnClk(self, fileLineEdit, suffix):
        fileLineEdit.setText(
            str(QFileDialog.getOpenFileName(self, "Select File",None,suffix)[0]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = MngWindow()
    screen.show()
    sys.exit(app.exec_())
