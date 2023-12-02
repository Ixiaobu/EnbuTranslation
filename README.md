# EnbnTranslation

这是一个简洁、轻量、乖巧的桌面翻软件。内核采用腾讯翻译，使用之前请查阅readme文件获得使用方法。

<figure class="half">
    <img src="http://m.qpic.cn/psc?/V528xuCj2kwtt20rnvvx1PVwKf3jQ9T6/ruAMsa53pVQWN7FLK88i5mvUcX9LjAarmMgCGNbuiUbO3CsomgGMI69PcpSGBgMg2ZiG0IiyzQ9BWfiUbuDQFy6yicNDjfGx*7eOXiPOMyI!/b&bo=xQHcAAAAAAADBzo!&rf=viewer_4">
    <img src="http://m.qpic.cn/psc?/V528xuCj2kwtt20rnvvx1PVwKf3jQ9T6/ruAMsa53pVQWN7FLK88i5mvUcX9LjAarmMgCGNbuiUZINUbVJZaHZq6zoqeO*VJ9QuDwxjd9J.0aQeQpdfrr1MckTcWmEHDkYrxqLqzg3LQ!/b&bo=xgHhAAAAAAADBwQ!&rf=viewer_4">
</figure>

# 主要功能

1.用户输入：回车确定后显示翻译结果

2.自动翻译：开启自动翻译后，自动翻译并显示当前用户粘贴板的内容

3.自动计数：统计用户当月的使用量，防止超出限制产生费用

4.深色模式：一键切换深色/浅色模式

5.快捷交互：ALt+Z/X/C 分别对应从屏幕的左、上、右呼入呼出

6.字体适应：一键控制显示的字体大小

# 申请腾讯翻译

### 1.申请腾讯翻译SecretId 和 SecretKey

申请教程网站：[https://blog.csdn.net/weixin_44253490/article/details/126365385](https://)

注意：记得仔细阅读注意事项，大概意思就是每月可以免费查5000000个字符， 超过之后每一百万字符五十几块钱，普通人一般超不了，软件下面也有计数，那个计数会比实际使用的多0.5倍左右，起警示作用，想知道详细的还得去管网自己查哦

申请好后把申请得到的 SecretId 和 SecretKey 复制到 data/model.txt 对应位置后面，就可以正常运行喽！

# 交互逻辑

运行之后程序会保留在右下角托盘，右键可以进行简单设置。

### 打开方式：

alt + z， 从左边出现（收回）
alt + x， 从上边出现（收回）
alt + c， 从右边出现（收回）

### 自动翻译：

默认关闭，防止用超
开启后程序会自动翻译用户粘贴板内容

### **按钮作用：**

拖动右下角”↘“符号处可以缩放
拖动界面边缘可以移动
点击右上角“-”、“+”分别可以缩小放大字体
点击左上角色块可以深色/浅色模式切换
输入回车后可以翻译

# 写在最后

这是我第一次分享自己的项目，希望大家喜欢。如有bug或问题欢迎大家评论，我会一一回复！

