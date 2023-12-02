import ctypes
import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QApplication, QSystemTrayIcon, QMenu, QAction, qApp
from pynput import keyboard

from EnbuToolFun import read_file
from EnbuTranslation import CreateEnbuTranslation
from LRWindow import LRWindow
from playsound import playsound

# pyinstaller -F -w -i code\logo.ico code\main.py
# 自定义线程 检测组合键
class New_Thread(QThread):
    #自定义信号声明
    KeySignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(New_Thread, self).__init__(parent)

    #run函数是子线程中的操作，线程启动后开始执行
    def run(self):
        def up():
            self.KeySignal.emit("up")

        def left():
            self.KeySignal.emit("left")

        def right():
            self.KeySignal.emit("right")

        with keyboard.GlobalHotKeys({"<alt>+x": up,
                                     "<alt>+z": left,
                                     "<alt>+c": right}) as listener:
            listener.join()

# 托盘图标实现
class TrayModel(QSystemTrayIcon):

    KeySignal = pyqtSignal(str)

    def __init__(self, Window, data):
        super(TrayModel, self).__init__()
        self.window = Window
        self.Timi_kind = data
        self.Auto_kind = 0
        self.init_ui()

    def init_ui(self):
        # 初始化菜单
        self.menu = QMenu()

        self.auto = QAction('开启自动翻译', self, triggered=self.ReverseAuoto)
        self.timi = QAction('关闭timi' if self.Timi_kind else '开启timi', self, triggered=self.ReverseTimi)
        self.close_all = QAction('退出应用', self, triggered=self.quit_clock)
        # self.button = QPushButton(self)

        self.menu.addAction(self.auto)
        self.menu.addAction(self.timi)
        self.menu.addAction(self.close_all)
        # self.menu.addAction(self.button)

        self.setContextMenu(self.menu)

        self.setIcon(QIcon(r"..\data\logo\logo.ico"))
        self.icon = self.MessageIcon()

    # 自动翻译
    def ReverseAuoto(self):
        self.Auto_kind ^= 1
        if self.Auto_kind:
            self.auto.setText("关闭自动翻译")
            self.KeySignal.emit("开启自动翻译")
        else:
            self.auto.setText("开启自动翻译")
            self.KeySignal.emit("关闭自动翻译")

    # timi
    def ReverseTimi(self):
        self.Timi_kind ^= 1
        if self.Timi_kind:
            self.timi.setText("关闭timi")
            self.KeySignal.emit("开启timi")
        else:
            self.timi.setText("开启timi")
            self.KeySignal.emit("关闭timi")

    # 关闭程序
    def quit_clock(self):
        qApp.quit()

    def SetDay(self):
        self.menu.setStyleSheet("background-color:#ecf4ff; color:#150430")

    def SetNight(self):
        self.menu.setStyleSheet("background-color:#150430; color:#ffffff")

class EnbuMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(EnbuMainWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SplashScreen)
        # 去掉窗口标题栏和按钮, 使窗口置顶， 使窗口不显示在任务栏
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口真透明
        self.setWindowIcon(QIcon(r"..\data\logo\logo.ico"))  # 窗口图标设置
        desktop = QApplication.desktop()
        temp = 200  # 出血
        self.move(-temp, -temp)
        self.resize(desktop.width() + temp * 2, desktop.height() + temp * 2)

        self.go()

    # 背景阴影
    def Get_Shaow(self):
        shadow = QGraphicsDropShadowEffect(self)  # 创建阴影
        shadow.setBlurRadius(20)  # 设置阴影大小为9px
        shadow.setOffset(0, 0)  # 阴影偏移距离为0px
        return shadow

    # 定义初始变量以及相关检测
    def Set_variable(self):
        temp = read_file()
        self.Month = temp["Month"]
        self.Count = temp["Count"]
        self.Mode = temp["Mode"]
        self.FontSize = temp["FontSize"]
        self.timi = temp["timi"]
        self.SecretId = temp["SecretId"]
        self.SecretKey = temp["SecretKey"]
        self.Translation = CreateEnbuTranslation(self.SecretId, self.SecretKey)  # 创建翻译函数

        # 检测是否换月
        today = datetime.datetime.today()
        nowmonth = today.month
        if nowmonth != self.Month:
            self.Month = nowmonth
            self.Count = 0

    # 初始加载控件
    def Set_qt(self):
        # 监听键盘
        self.ReadKey = New_Thread()
        self.ReadKey.KeySignal.connect(self.keyPressEvent)
        self.ReadKey.start()

        # 托盘窗口
        self.Tray_qt = TrayModel(self, self.timi)
        self.Tray_qt.show()

        # 左右窗口
        temp = {'Month': self.Month,
                'Count': self.Count,
                'Mode': self.Mode,
                'FontSize': self.FontSize,
                'timi': self.timi,
                'SecretId': self.SecretId,
                'SecretKey': self.SecretKey,
                'TranslationFun': self.Translation,
                'Tray': self.Tray_qt}
        self.MainLR_qt = LRWindow(self, temp)
        self.MainLR_qt.SetDay()
        self.MainLR_qt.setGraphicsEffect(self.Get_Shaow())

        # 调整昼夜
        if self.Mode:
            self.MainLR_qt.SetDay()
        else:
            self.MainLR_qt.SetNight()

    def SetDay(self):
        pass

    def SetNight(self):
        pass

    # 监听键盘按下事件
    def keyPressEvent(self, val):
        if val == "left":
            if self.MainLR_qt.Mode == "close":
                self.MainLR_qt.OpenLeft()
            else:
                self.MainLR_qt.CloseLeft()

        elif val == "right":
            if self.MainLR_qt.Mode == "close":
                self.MainLR_qt.OpenRight()
            else:
                self.MainLR_qt.CloseRight()

        elif val == "up":
            if self.MainLR_qt.Mode == "open":
                self.MainLR_qt.CloseUp()
            else:
                self.MainLR_qt.OpenUp()


    def go(self):
        self.Set_variable()
        self.Set_qt()
        if self.timi:
            playsound(r"..\data\timi\timi.mp3")



if __name__ == "__main__":
    import sys
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid") # 任务栏图标实现
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = EnbuMainWindow()  # 创建窗体对象
    MainWindow.show()
    sys.exit(app.exec_())  # 程序关闭时退出进程