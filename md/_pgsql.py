# coding=utf-8

"""

PostgreSQL 连接配置界面模块

"""

import psycopg2
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QGridLayout,
)
from md import _DBConfigWidget


class PgsqlWidget(_DBConfigWidget):
    def __init__(self, parent=None):
        super(PgsqlWidget, self).__init__(parent)
        self.setWindowTitle('PostgreSQL 连接配置')
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self._init_ui()

    def _init_ui(self):
        layout = QGridLayout()
        layout.setVerticalSpacing(5)
        self.setLayout(layout)

        # icon
        icon = QIcon("../assets/icons/widget/PostgreSQL.png")
        self.setWindowIcon(icon)

        layout_host = QGridLayout()
        layout_host.setSpacing(10)
        label_host = QLabel('主机')
        label_host.setFixedSize(40, 20)
        label_host.setAlignment(Qt.AlignLeft)
        self.edit_host = QLineEdit()
        self.edit_host.setFixedSize(200, 20)
        layout_host.addWidget(label_host, 0, 0)
        layout_host.addWidget(self.edit_host, 0, 1)
        layout.addLayout(layout_host, 0, 0)

        layout_port = QGridLayout()
        layout_port.setSpacing(10)
        label_port = QLabel('端口号')
        label_port.setFixedSize(40, 20)
        label_port.setAlignment(Qt.AlignLeft)
        self.edit_port = QLineEdit()
        self.edit_port.setText('5432')
        self.edit_port.setFixedSize(200, 20)
        layout_port.addWidget(label_port, 0, 0)
        layout_port.addWidget(self.edit_port, 0, 1)
        layout.addLayout(layout_port, 1, 0)

        layout_user = QGridLayout()
        layout_user.setSpacing(10)
        label_user = QLabel('用户名')
        label_user.setFixedSize(40, 20)
        label_user.setAlignment(Qt.AlignLeft)
        self.edit_user = QLineEdit()
        self.edit_user.setFixedSize(200, 20)
        layout_user.addWidget(label_user, 0, 0)
        layout_user.addWidget(self.edit_user, 0, 1)
        layout.addLayout(layout_user, 2, 0)

        layout_password = QGridLayout()
        layout_password.setSpacing(10)
        label_password = QLabel('密码')
        label_password.setFixedSize(40, 20)
        label_password.setAlignment(Qt.AlignLeft)
        self.edit_password = QLineEdit()
        self.edit_password.setFixedSize(150, 20)
        self.edit_password.setEchoMode(QLineEdit.Password)
        layout_password.addWidget(label_password, 0, 0)
        layout_password.addWidget(self.edit_password, 0, 1)
        self.passwd_viewable_button = QPushButton('显示')
        self.passwd_viewable_button.setFixedSize(40, 20)
        self.passwd_viewable_button.clicked.connect(self._viewable_password)
        layout_password.addWidget(self.passwd_viewable_button, 0, 2)
        layout.addLayout(layout_password, 3, 0)

        layout_database = QGridLayout()
        layout_database.setSpacing(10)
        label_database = QLabel('数据库')
        label_database.setFixedSize(40, 20)
        label_database.setAlignment(Qt.AlignLeft)
        self.edit_database = QLineEdit()
        self.edit_database.setFixedSize(200, 20)
        layout_database.addWidget(label_database, 0, 0)
        layout_database.addWidget(self.edit_database, 0, 1)
        layout.addLayout(layout_database, 4, 0)

        layout_button = QGridLayout()
        layout_button.setSpacing(10)
        self.button_connect = QPushButton('测试连接')
        self.button_connect.clicked.connect(self.connect_test)
        self.button_connect.setFixedSize(100, 30)
        layout_button.addWidget(self.button_connect, 0, 0)

        self.button_save = QPushButton('保存')
        self.button_save.clicked.connect(self.save)
        self.button_save.setFixedSize(100, 30)
        layout_button.addWidget(self.button_save, 0, 1)

        layout.addLayout(layout_button, 5, 0)

    def connect_test(self):
        host = self.edit_host.text()
        port = self.edit_port.text()
        user = self.edit_user.text()
        password = self.edit_password.text()
        database = self.edit_database.text()
        try:
            conn = psycopg2.connect(host=host, port=port, user=user,
                                    password=password, database=database)
            conn.close()
            QMessageBox.information(self, 'Notice', 'Connect Test Success!')
        except Exception as e:
            QMessageBox.information(self, 'Notice', 'Connect Test Failed!\n' + str(e))

    def _viewable_password(self):
        if self.edit_password.echoMode() == QLineEdit.Normal:
            self.edit_password.setEchoMode(QLineEdit.Password)
            self.passwd_viewable_button.setText('显示')
        else:
            self.edit_password.setEchoMode(QLineEdit.Normal)
            self.passwd_viewable_button.setText('隐藏')

    def save(self):
        host = self.edit_host.text()
        port = self.edit_port.text()
        user = self.edit_user.text()
        password = self.edit_password.text()
        database = self.edit_database.text()
        encoding = self.edit_encoding.currentText()
        try:
            db_config = {'host': host, 'port': port,
                         'user': user, 'password': password,
                         'database': database, 'encoding': encoding}
            self.save_db_config(**db_config)
            QMessageBox.information(self, 'Notice', 'Save Success!')
        except Exception as e:
            QMessageBox.information(self, 'Notice', 'Save Failed!\n' + str(e))


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = PgsqlWidget()
    window.show()
    sys.exit(app.exec_())
