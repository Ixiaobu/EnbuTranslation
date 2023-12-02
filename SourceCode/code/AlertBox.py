from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QApplication, QMainWindow
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QCursor, QFont
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QScrollBar, QTextEdit

class AlertBox(QMainWindow):
    def __init__(self, text):
        super(AlertBox, self).__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 窗口透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |
                            QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint)  # 无边框

        self.resize(340, 210)
        self.m_flag = True
        self.text = text  #警示信息
        self.SetUp()

    # 背景阴影
    def Get_Shaow(self):
        shadow = QGraphicsDropShadowEffect(self)  # 创建阴影
        shadow.setBlurRadius(20)  # 设置阴影大小为9px
        shadow.setOffset(0, 0)  # 阴影偏移距离为0px
        return shadow

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            try:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                QMouseEvent.accept()
                self.change_window_emit(self.x(), self.y())
            except:
                return

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def SetNight(self):
        self.Bk.setStyleSheet("background-color:#150430;border-radius:10;")
        self.text_qt.setStyleSheet("color:rgb(255,255,255)")
        self.Close_qt.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);border-radius:8px;color:rgb(255,255,255)}QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''')

    def SetDay(self):
        self.Bk.setStyleSheet("background-color:#F0F0F0;border-radius:10;")
        self.text_qt.setStyleSheet("color:rgb(0,0,0)")
        self.Close_qt.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);border-radius:8px;color:rgb(0,0,0)}QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''')

    def SetQt(self):
        self.Bk = QLabel(self)  # 背景
        self.text_qt = QLabel(self) # 显示文字的地方
        self.Close_qt = QPushButton(self)

        # 设置背景格式
        self.Bk.resize(300, 170)
        self.Bk.move(20, 20)
        self.Bk.setGraphicsEffect(self.Get_Shaow())

        # 文字部分
        self.text_qt.setText(self.text)
        self.text_qt.resize(300, 170)
        self.text_qt.move(20, 20)
        self.text_qt.setFont(QFont("幼圆", 16))
        self.text_qt.setAlignment(Qt.AlignCenter)

        # 按钮相关
        self.Close_qt.resize(30, 30)
        self.Close_qt.move(290, 20)
        self.Close_qt.setText("×")
        self.Close_qt.setFont(QFont("arial", 16, QFont.Bold))
        self.Close_qt.clicked.connect(lambda x: self.close())


    def SetUp(self):
        self.SetQt()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = AlertBox("本月已查询 5000000 字符\n请注意使用")  # 创建窗体对象
    MainWindow.SetDay()
    MainWindow.show()  # 显示窗体
    sys.exit(app.exec_())  # 程序关闭时退出进程