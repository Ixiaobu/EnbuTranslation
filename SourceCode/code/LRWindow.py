from collections import deque
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QThread
from PyQt5.QtGui import QCursor, QFont, QTextCursor
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QScrollBar, QTextEdit
from playsound import playsound

from EnbuToolFun import written_file
import pyperclip
import time


# 自定义线程 检测用户粘贴板
class Auto_Thread(QThread):
    #自定义信号声明
    KeySignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Auto_Thread, self).__init__(parent)
        self.text = ""
        self.auto = 1

    #run函数是子线程中的操作，线程启动后开始执行
    def run(self):
        while True and self.auto:
            temp = pyperclip.paste()
            if temp != self.text:
                self.text = temp
                self.KeySignal.emit("0")
            time.sleep(1)


# 缩放按钮
class MoveButton(QPushButton):
    siteChanged = pyqtSignal(str)

    def __init__(self, dad):
        super(MoveButton, self).__init__(dad)
        self.dad = 0
        self.m_flag = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):

        if Qt.LeftButton and self.m_flag:
            try:
                self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
                if self.x() < 200 or self.y() < 50:
                    x = max(self.x(), 201)
                    y = max(self.y(), 51)
                    self.move(x, y)

                QMouseEvent.accept()
                self.siteChanged.emit("0")
                self.change_window_emit(self.x(), self.y())
            except:
                return

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


class LRWindow(QLabel):
    def __init__(self, dad, data):
        super(LRWindow, self).__init__(dad)
        self.dad = dad
        self.Month = data["Month"]
        self.Count = data["Count"]
        self.ColorMode = data["Mode"]
        self.FontSize = data["FontSize"]
        self.timi = data["timi"]
        self.SecretId = data["SecretId"]
        self.SecretKey = data["SecretKey"]
        self.TranslationFun = data["TranslationFun"]
        self.Tray_qt = data["Tray"]
        self.mode = "day"
        self.resize(0, 0)
        self.Setup()

    # =======窗口移动相关=======
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
    # =======窗口移动相关=======

    # 定义初始变量
    def SetVariable(self):
        self.MoveBig_deque = deque(maxlen=10)  # 动画队列
        self.Mode = "close"
        self.m_flag = True

    # 动画
    def MyMoveBig(self, name, before, after, time=150):
        MoveBig = QPropertyAnimation(name, b'geometry')
        self.MoveBig_deque.append(MoveBig)
        MoveBig.setDuration(time)
        MoveBig.setStartValue(before)
        MoveBig.setEndValue(after)
        MoveBig.setEasingCurve(QEasingCurve.InOutCubic)  # 设置缓动函数
        MoveBig.start()

    # 初始加载控件
    def SetQt(self):
        self.ChangeMode_qt = QPushButton(self)  # 昼夜切换
        self.CreaseFont_qt = QPushButton(self)  # 减小字体
        self.IncreaseFont_qt = QPushButton(self)  # 增大字体
        self.TextEdit = QTextEdit(self)  # 文本编辑
        self.Resize_qt = MoveButton(self)  # 缩放按钮
        self.Counts_qt = QLabel(self)  # 显示个数
        self.AutoThread_qt = Auto_Thread(self)  # 自动翻译

        # 初始属性
        self.ChangeMode_qt.resize(50, 12)

        self.CreaseFont_qt.resize(20, 20)
        self.CreaseFont_qt.setText("-")
        self.CreaseFont_qt.setFont(QFont("arial", 16))

        self.IncreaseFont_qt.resize(20, 20)
        self.IncreaseFont_qt.setText("+")
        self.IncreaseFont_qt.setFont(QFont("arial", 16))

        self.TextEdit.resize(0, 0)
        self.TextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) # 去除滚动条
        self.TextEdit.setFont(QFont("等线", self.FontSize))

        self.Resize_qt.resize(20, 20)
        self.Resize_qt.setText("⇲")
        self.Resize_qt.setFont(QFont("arial", 15))

        self.Counts_qt.resize(180, 20)
        self.Counts_qt.setText("本月已使用 %d 字符" % self.Count)
        self.Counts_qt.setFont(QFont("等线", 10, QFont.Bold))


    # 安装槽函数
    def SetFun(self):
        # 昼夜切换
        def ChangeMode_fun():
            if self.mode == "day":
                self.SetNight()
                self.mode = "night"
                self.ColorMode = 0
            else:
                self.SetDay()
                self.mode = "day"
                self.ColorMode = 1
        self.ChangeMode_qt.clicked.connect(ChangeMode_fun)

        # 减小
        def CreaseFont_fun():
            self.FontSize = max(10, self.FontSize - 1)
            self.TextEdit.setFont(QFont("等线", self.FontSize))
        self.CreaseFont_qt.clicked.connect(CreaseFont_fun)

        # 增大
        def IncreaseFont_fun():
            self.FontSize = min(50, self.FontSize + 1)
            self.TextEdit.setFont(QFont("等线", self.FontSize))
        self.IncreaseFont_qt.clicked.connect(IncreaseFont_fun)

        # 文本编辑器
        def TextEdit_fun():
            text = self.TextEdit.toPlainText()
            if text and text[-1] == "\n":
                text = text.replace("\n", " ")
                text2 = self.TranslationFun(text)
                self.TextEdit.setText(text2)
                self.TextEdit.moveCursor(QTextCursor.End)

                # 更新计数
                self.Count += int(len(text2) * 2)
                self.Counts_qt.setText("本月已使用 %d 字符" % self.Count)

                # 储存信息
                temp = {'Month': self.Month,
                        'Count': self.Count,
                        'Mode': self.ColorMode,
                        'FontSize': self.FontSize,
                        'timi': self.timi,
                        'SecretId': self.SecretId,
                        'SecretKey': self.SecretKey}
                written_file(temp)
        self.TextEdit.textChanged.connect(TextEdit_fun)

        # 自动翻译
        def AutoThread_fun():
            if self.Mode == "close":
                return
            text = pyperclip.paste()
            text = text.replace("\n", " ")
            text2 = self.TranslationFun(text)
            self.TextEdit.setText(text2)
            self.TextEdit.moveCursor(QTextCursor.End)

            # 更新计数
            self.Count += int(len(text2) * 2)
            self.Counts_qt.setText("本月已使用 %d 字符" % self.Count)

            # 储存信息
            temp = {'Month': self.Month,
                    'Count': self.Count,
                    'Mode': self.ColorMode,
                    'FontSize': self.FontSize,
                    'timi': self.timi,
                    'SecretId': self.SecretId,
                    'SecretKey': self.SecretKey}
            written_file(temp)
        self.AutoThread_qt.KeySignal.connect(AutoThread_fun)

        # 缩放
        def Resize_fun():
            # 本体缩放
            w = self.Resize_qt.x() + 20
            h = self.Resize_qt.y() + 20
            self.resize(w, h)

            # 文本编辑器缩放
            w = self.Resize_qt.x() - 20
            h = self.Resize_qt.y() - 20
            self.TextEdit.resize(w, h)

            # 其他移动
            self.CreaseFont_qt.move(self.width() - 50, 0)  # 减小字体
            self.IncreaseFont_qt.move(self.width() - 30, 0)  # 增大字体
            self.Resize_qt.move(self.width() - 20, self.height() - 20)  # 缩放按钮
            self.Counts_qt.move(self.width() - 30, 0)  # 个数
            self.Counts_qt.move(10, self.height() - 20)
        self.Resize_qt.siteChanged.connect(Resize_fun)

        # 与托盘交流
        def Tray_fun(val):
            if val == "关闭timi":
                self.timi = 0
                # 储存信息
                temp = {'Month': self.Month,
                        'Count': self.Count,
                        'Mode': self.ColorMode,
                        'FontSize': self.FontSize,
                        'timi': self.timi,
                        'SecretId': self.SecretId,
                        'SecretKey': self.SecretKey}
                written_file(temp)
            elif val == "开启timi":
                playsound(r"..\data\timi\timi.mp3")
                self.timi = 1
                # 储存信息
                temp = {'Month': self.Month,
                        'Count': self.Count,
                        'Mode': self.ColorMode,
                        'FontSize': self.FontSize,
                        'timi': self.timi,
                        'SecretId': self.SecretId,
                        'SecretKey': self.SecretKey}
                written_file(temp)
            elif val == "开启自动翻译":
                self.AutoThread_qt.auto = 1
                self.AutoThread_qt.start()
            else:
                self.AutoThread_qt.auto = 0
                self.AutoThread_qt.wait()

        self.Tray_qt.KeySignal.connect(Tray_fun)


    # 日间
    def SetDay(self):
        self.setStyleSheet("background-color:#ecf4ff;border-radius:15;")
        self.TextEdit.setStyleSheet("background-color:#ecf4ff; color:#150430")
        self.ChangeMode_qt.setStyleSheet(
            '''QPushButton{background:#ffcb5c;border-radius:6px}QPushButton:hover{background:#ffb10d}''')
        self.CreaseFont_qt.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);border-radius:8px;color:#393b3e}QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''')
        self.IncreaseFont_qt.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);border-radius:8px;color:#393b3e}QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''')
        self.Resize_qt.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);border-radius:8px;color:#adb3bb}QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''')
        self.Counts_qt.setStyleSheet("color:#393b3e")
        self.Tray_qt.SetDay()

        self.mode = "day"

    # 夜间
    def SetNight(self):
        self.setStyleSheet("background-color:#150430;border-radius:15;")
        self.TextEdit.setStyleSheet("background-color:#150430; color:#ffffff")
        self.ChangeMode_qt.setStyleSheet(
            '''QPushButton{background:#0b006d;border-radius:6px}QPushButton:hover{background:#1f0046}''')
        self.CreaseFont_qt.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);border-radius:8px;color:rgb(255,255,255)}QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''')
        self.IncreaseFont_qt.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);border-radius:8px;color:rgb(255,255,255)}QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''')
        self.Resize_qt.setStyleSheet(
            '''QPushButton{background:rgb(0,0,0,0);border-radius:8px;color:rgb(255,255,255)}QPushButton:hover{background:rgb(0,0,0,0);color:rgb(244,71,53)}''')
        self.Counts_qt.setStyleSheet("color:#D0D0D0")
        self.Tray_qt.SetNight()

        self.mode = "night"

    # 启动！
    def OpenUp(self):

        temp_h1 = 0
        temp_w1 = 200
        temp_h2 = 70
        temp_w2 = 350
        a = QtCore.QRect((QCursor.pos().x() + 200) - temp_w1 // 2, 0, temp_w1, temp_h1)
        b = QtCore.QRect((QCursor.pos().x() + 200) - temp_w2 // 2, 20 + 200, temp_w2, temp_h2)
        self.MyMoveBig(self, a, b, time=300)

        # 展开文本编辑器
        self.TextEdit.move(20, 20)
        self.TextEdit.resize(temp_w2 - 40, temp_h2 - 40)

        # 展开各个按钮
        self.ChangeMode_qt.move(10, 6)  # 昼夜切换
        self.CreaseFont_qt.move(temp_w2 - 50, 0)  # 减小字体
        self.IncreaseFont_qt.move(temp_w2 - 30, 0)  # 增大字体
        self.Resize_qt.move(temp_w2 - 20, temp_h2 - 20)  # 缩放按钮
        self.Counts_qt.move(10, temp_h2 - 20)
        self.Mode = "open"


    # 启动！
    def OpenLeft(self):
        temp_h1 = int((self.dad.height() - 400))
        temp_w1 = 100
        temp_h2 = int((self.dad.height() - 400) * 0.8)
        temp_w2 = 350
        a = QtCore.QRect(0, (self.dad.height() - temp_h1) // 2, temp_w1, temp_h1)
        b = QtCore.QRect(20 + 200, (self.dad.height() - temp_h2) // 2, temp_w2, temp_h2)
        self.MyMoveBig(self, a, b, time=300)

        # 展开文本编辑器
        self.TextEdit.move(20, 20)
        self.TextEdit.resize(temp_w2 - 40, temp_h2 - 40)

        # 展开各个按钮
        self.ChangeMode_qt.move(10, 6)  # 昼夜切换
        self.CreaseFont_qt.move(temp_w2 - 50, 0)  # 减小字体
        self.IncreaseFont_qt.move(temp_w2 - 30, 0)  # 增大字体
        self.Resize_qt.move(temp_w2 - 20, temp_h2 - 20)  # 缩放按钮
        self.Counts_qt.move(10, temp_h2 - 20)
        self.Mode = "open"

    # 启动！
    def OpenRight(self):
        temp_h1 = int((self.dad.height() - 400))
        temp_w1 = 100
        temp_h2 = int((self.dad.height() - 400) * 0.8)
        temp_w2 = 350
        a = QtCore.QRect(self.dad.width() - 100, (self.dad.height() - temp_h1) // 2, temp_w1, temp_h1)
        b = QtCore.QRect(self.dad.width() - (20 + 200 + temp_w2), (self.dad.height() - temp_h2) // 2, temp_w2, temp_h2)
        self.MyMoveBig(self, a, b, time=300)


        # 展开文本编辑器
        self.TextEdit.move(20, 20)
        self.TextEdit.resize(temp_w2 - 40, temp_h2 - 40)

        # 展开各个按钮
        self.ChangeMode_qt.move(10, 6)  # 昼夜切换
        self.CreaseFont_qt.move(temp_w2 - 50, 0)  # 减小字体
        self.IncreaseFont_qt.move(temp_w2 - 30, 0)  # 增大字体
        self.Resize_qt.move(temp_w2 - 20, temp_h2 - 20) # 缩放按钮
        self.Counts_qt.move(temp_h2 - 30, 0)  # 个数
        self.Counts_qt.move(10, temp_h2 - 20)
        self.Mode = "open"

    # 关闭
    def CloseLeft(self):
        temp_h1 = int((self.dad.height() - 400) * 0.6)
        temp_w1 = 100
        a = QtCore.QRect(self.x(), self.y(), self.width(), self.height())
        b = QtCore.QRect(0, (self.dad.height() - temp_h1) // 2, temp_w1, temp_h1)
        self.MyMoveBig(self, a, b, time=500)
        self.Mode = "close"

    # 关闭
    def CloseRight(self):
        temp_h1 = int((self.dad.height() - 400) * 0.6)
        temp_w1 = 100
        a = QtCore.QRect(self.x(), self.y(), self.width(), self.height())
        b = QtCore.QRect(self.dad.width() - 100, (self.dad.height() - temp_h1) // 2, temp_w1, temp_h1)
        self.MyMoveBig(self, a, b, time=500)
        self.Mode = "close"

    def CloseUp(self):
        temp_h1 = 0
        temp_w1 = int(self.width() * 0.5)
        a = QtCore.QRect(self.x(), self.y(), self.width(), self.height())
        b = QtCore.QRect((self.x() + (self.width() -temp_w1) // 2), 0, temp_w1, temp_h1)
        self.MyMoveBig(self, a, b, time=500)
        self.Mode = "close"

    # 初始化
    def Setup(self):
        self.SetVariable()
        self.SetQt()
        self.SetFun()