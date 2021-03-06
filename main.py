# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import EclassCrawlingModule as Module
import pprint

class Ui_MainWindow(object):
    def __init__(self):
        f = open("account", encoding='UTF-8')
        account = f.readlines()
        self.secrets = Module.Login(account[0].replace("\n", ''), account[1].replace("\n", ''))

        self.secrets.getSession()
        self.secrets.getUserInfo()
        self.lecture_info = Module.Lecture(self.secrets.s, self.secrets.uid).getLectureList()  # 강의 번호 등 정보
        print(self.lecture_info)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(930, 662)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.subInfoTable = QtWidgets.QTableView(self.groupBox)
        self.subInfoTable.setObjectName("subInfoTable")
        self.verticalLayout_4.addWidget(self.subInfoTable)
        self.subInfoCombo = QtWidgets.QComboBox(self.groupBox)
        self.subInfoCombo.setObjectName("subInfoCombo")
        self.verticalLayout_4.addWidget(self.subInfoCombo)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.anceTable = QtWidgets.QTableView(self.groupBox_3)
        self.anceTable.setObjectName("anceTable")
        self.horizontalLayout_5.addWidget(self.anceTable)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.anceShowBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.anceShowBtn.setObjectName("anceShowBtn")
        self.verticalLayout_5.addWidget(self.anceShowBtn)
        self.ancePageBtn = QtWidgets.QPushButton(self.groupBox_3)
        self.ancePageBtn.setObjectName("ancePageBtn")
        self.verticalLayout_5.addWidget(self.ancePageBtn)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.hwTable = QtWidgets.QTableView(self.groupBox_2)
        self.hwTable.setObjectName("hwTable")
        self.horizontalLayout_3.addWidget(self.hwTable)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.hwSubmitBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.hwSubmitBtn.setObjectName("hwSubmitBtn")
        self.verticalLayout_3.addWidget(self.hwSubmitBtn)
        self.hwPageBtn = QtWidgets.QPushButton(self.groupBox_2)
        self.hwPageBtn.setObjectName("hwPageBtn")
        self.verticalLayout_3.addWidget(self.hwPageBtn)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.groupBox_4)
        self.calendarWidget.setObjectName("calendarWidget")
        self.horizontalLayout_4.addWidget(self.calendarWidget)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox_4)
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout_6.addWidget(self.dateEdit)
        self.dateEdtBtn = QtWidgets.QPushButton(self.groupBox_4)
        self.dateEdtBtn.setObjectName("dateEdtBtn")
        self.verticalLayout_6.addWidget(self.dateEdtBtn)
        self.chkScheduleBtn = QtWidgets.QPushButton(self.groupBox_4)
        self.chkScheduleBtn.setObjectName("chkScheduleBtn")
        self.verticalLayout_6.addWidget(self.chkScheduleBtn)
        self.horizontalLayout_4.addLayout(self.verticalLayout_6)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 930, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogIn = QtWidgets.QAction(MainWindow)
        self.actionLogIn.setObjectName("actionLogIn")
        self.actionShow_Message = QtWidgets.QAction(MainWindow)
        self.actionShow_Message.setObjectName("actionShow_Message")
        self.menu.addAction(self.actionLogIn)
        self.menu_2.addAction(self.actionShow_Message)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.today_date = self.calendarWidget.selectedDate()
        self.today_date1 = str(self.today_date.getDate()[0]) + ('0'+ str(self.today_date.getDate()[1])) if self.today_date.getDate()[1] < 10 else (self.today_date.getDate()[1])
        self.today_date1 = self.today_date1 + ('0'+ str(self.today_date.getDate()[2])) if self.today_date.getDate()[2] < 10 else self.today_date.getDate()[2]
        self.today_schedule = Module.ConvFunctions(self.secrets.s, self.secrets.uid).getCalender(self.today_date1, 'readSchedule')
        if len(self.today_schedule['title']) == 0:
            self.today_schedule = '일정이 없습니다.'

        self.subInfoCombo.addItems(self.lecture_info.keys())    #combobox에 과목 크롤링 데이터 추가
        self.subInfoCombo.currentIndexChanged.connect(self.getData)

    def getData(self):
        print("getData")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "과목 보기"))
        self.groupBox_3.setTitle(_translate("MainWindow", "공지 사항"))
        self.anceShowBtn.setText(_translate("MainWindow", "바로 보기"))
        self.ancePageBtn.setText(_translate("MainWindow", "페이지 이동"))
        self.groupBox_2.setTitle(_translate("MainWindow", "과제 제출"))
        self.hwSubmitBtn.setText(_translate("MainWindow", "과제 제출"))
        self.hwPageBtn.setText(_translate("MainWindow", "페이지 이동"))
        self.groupBox_4.setTitle(_translate("MainWindow", "스케줄 관리"))
        self.dateEdtBtn.setText(_translate("MainWindow", "추가/삭제"))
        self.chkScheduleBtn.setText(_translate("MainWindow", "일정 확인"))
        self.menu.setTitle(_translate("MainWindow", "설정"))
        self.menu_2.setTitle(_translate("MainWindow", "기타 기능"))
        self.actionLogIn.setText(_translate("MainWindow", "Change Account"))
        self.actionShow_Message.setText(_translate("MainWindow", "Show Message"))
'''
시작하면서 수집해와야할 데이터
1. 과목 정보
2. 스케줄
'''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
