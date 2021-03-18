from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(479, 90)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.idLineEdit = QtWidgets.QLineEdit(Form)
        self.idLineEdit.setObjectName("idLineEdit")
        self.horizontalLayout.addWidget(self.idLineEdit)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.pwLineEdit = QtWidgets.QLineEdit(Form)
        self.pwLineEdit.setObjectName("pwLineEdit")
        self.horizontalLayout.addWidget(self.pwLineEdit)
        self.buttonLogin = QtWidgets.QPushButton(Form)
        self.buttonLogin.setObjectName("buttonLogin")
        self.horizontalLayout.addWidget(self.buttonLogin)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Login Eclass"))
        self.label.setText(_translate("Form", "ID"))
        self.label_2.setText(_translate("Form", "PW"))
        self.buttonLogin.setText(_translate("Form", "LogIn"))


if __name__ == "__main__":
    import sys
    import pprint
    import EclassCrawlingModule as Module
    f = open("account",encoding='UTF-8')
    account = f.readlines()
    secrets = Module.Login(account[0].replace("\n",''), account[1].replace("\n",''))

    secrets.getSession()
    secrets.getUserInfo()
    # pprint.pprint(Module.Lecture(secrets.s, secrets.uid).goCategory('A20203ACS1202102', 'getClassInfo'))
    # pprint.pprint(Module.ConvFunctions(secrets.s, secrets.uid).getCalender('20210224', 'readSchedule'))
    pprint.pprint(Module.Lecture(secrets.s, secrets.uid).goCategory('A20211ACS1101012', 'getHomeWorkList'))    #모듈의 강의 관련
    # pprint.pprint(Module.ConvFunctions(secrets.s, secrets.uid, False).getMessage("transmissedMessage", 1, 10))
    # pprint.pprint(Module.ConvFunctions(secrets.s, secrets.uid, False).getMessage("showSelectedMessage", 0))

    # num = int(input())
    # # pprint.pprint(Module.ConvFunctions(secrets.s, secrets.uid, True).getMessage("deleteMessage", num))
    # i = 1
    # while True:
    #     inp = input("")
    #     if inp == '1':
    #         pprint.pprint(Module.ConvFunctions(secrets.s, secrets.uid).getCalender('20210224', "insertSchedule",str(i),"asdf","20210312","1221"))    #모듈의 편의 기능 관련  #기준이 뭔지 모르겠지만 28개가 최고임
    #
    #     elif inp == '2':
    #         idx = input("몇번째껄 지울까?")
    #         pprint.pprint(Module.ConvFunctions(secrets.s, secrets.uid).getCalender('20210224', "deleteSchedule",int(idx) - 1))    #모듈의 편의 기능 관련  #기준이 뭔지 모르겠지만 28개가 최고임
    #
    #     elif inp == '3':
    #         pprint.pprint(Module.ConvFunctions(secrets.s, secrets.uid).getCalender('20210224', 'readSchedule'))
    #     else:
    #         break
    #     i = i+1
    # pprint.pprint(Module.ConvFunctions(secrets.s, secrets.uid).getCalender('20210224', 'readSchedule'))
    # app = QtWidgets.QApplication(sys.argv)
    # Form = QtWidgets.QWidget()
    # ui = Ui_Form()
    # ui.setupUi(Form)
    # Form.show()
    # sys.exit(app.exec_())
