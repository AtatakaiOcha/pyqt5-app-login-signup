import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QEvent

from uis.mainWindow import Ui_MainWindow
from uis.login_form import Ui_LogInSignUpForm
from uis.sign_up_form import Ui_RegisterForm
from handler.handler import HandlerBd
from pass_gen import generate_password


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("__MAIN__WINDOW__")
        self.setWindowIcon(QtGui.QIcon(""))
        self.query = HandlerBd()
        self.user_data()

        self.init_ui()
        
    def init_ui(self):
        pass

    def user_data(self):
        global AUTH
        data = []
        for index in range(len(AUTH[0])):
            data.append(AUTH[0][index])
        text = "USER_ID: ", data[0]
        text1 = "USER_FNAME: ", data[1]
        text2 = "USER_SNAME: ", data[2]
        text3 = "USER_LNAME: ", data[3]
        self.ui.label_user_data.setFont(QtGui.QFont("Consolas", 12))
        self.ui.label_user_data.setWordWrap(True)
        self.ui.label_user_data.setText(str(text) + "\n" + str(text1) + "\n" + str(text2) + "\n" + str(text3))


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_LogInSignUpForm()
        self.ui.setupUi(self)
        self.ui.btn_signup.clicked.connect(self.reg_form)
        self.ui.btn_login.clicked.connect(self.login_form)
        self.query = HandlerBd()
        self.show()
        self.init_ui()

    def login_form(self):
        telephone = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()

        if self.query.query_select_login_passwd(telephone, password):
            global AUTH
            AUTH = self.query.query_select_current_user(telephone)
            self.run_main_window()
        else:
            QtWidgets.QMessageBox().critical(self, "Error", "You enter incorrect data", QtWidgets.QMessageBox().Ok)

    def init_ui(self):
        pass

    def reg_form(self):
        self.deleteLater()
        self.cams = SignupWindow()
        self.cams.show()

    def run_main_window(self):
        self.deleteLater()
        self.cams = MainWindow()
        self.cams.show()
        

class SignupWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SignupWindow, self).__init__()
        self.ui = Ui_RegisterForm()
        self.ui.setupUi(self)
        self.ui.btn_reg.clicked.connect(self.btn_register)
        self.ui.btn_back.clicked.connect(self._btn_back)
        self.query = HandlerBd()
        self.cntr = 0
        self.ui.lineEdit_password.installEventFilter(self)
        self.ui.lineEdit_password_rpt.installEventFilter(self)
        self.show()
        self.init_ui()

    def init_ui(self):
        pass

    def show_msg(self):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle("Prompt")
        msg.setText("Autogen password?")
        yes_ = msg.addButton("Yes", QtWidgets.QMessageBox.AcceptRole)
        no_ = msg.addButton("No", QtWidgets.QMessageBox.AcceptRole)
        msg.setDefaultButton(yes_)
        msg.exec_()
        msg.deleteLater()
        if msg.clickedButton() is yes_:
            self.autofill_password()
        else:
            pass

    def autofill_password(self):
        passwd = generate_password()
        self.ui.lineEdit_password.setText(passwd)
        self.ui.lineEdit_password_rpt.setText(passwd)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if (obj == self.ui.lineEdit_password or obj == self.ui.lineEdit_password_rpt) and self.cntr == 0:
                self.cntr += 1
                self.show_msg()
        return super(SignupWindow, self).eventFilter(obj, event)

    def btn_register(self):
        # todo regex
        fname = self.ui.lineEdit_fname.text()
        sname = self.ui.lineEdit_sname.text()
        lname = self.ui.lineEdit_lname.text()
        email = self.ui.lineEdit_email.text()
        address = self.ui.lineEdit_address.text()
        telephone = self.ui.lineEdit_phone.text()
        password = self.ui.lineEdit_password.text()
        password_rpt = self.ui.lineEdit_password_rpt.text()
        data = [fname, sname, lname, email, address, telephone, password]

        if all(data):
            if self.query.query_check_user(telephone):
                if password == password_rpt:
                    self.query.query_insert(data)
                    print(self.query.query_select_all())
                    self.run_login_window()
                else:
                    QtWidgets.QMessageBox().critical(self, "Error", "Your passwords are not equal.",
                                                     QtWidgets.QMessageBox().Ok)
            else:
                QtWidgets.QMessageBox().critical(self, "Error", "This user is already registered.",
                                                 QtWidgets.QMessageBox().Ok)
        else:
            QtWidgets.QMessageBox().critical(self, "Error", "Your data is not valid.", QtWidgets.QMessageBox().Ok)

    def _btn_back(self):
        self.run_login_window()

    def run_login_window(self):
        self.deleteLater()
        self.cams = LoginWindow()
        self.cams.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = LoginWindow()
    application.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    AUTH = ""
    main()
