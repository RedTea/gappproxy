#summary GAppProxy Windows客户端的使用说明
#labels Deprecated,Phase-Deploy

# 简介 #
为方便Windows用户使用，GAppProxy从svn r38版开始为其客户端（proxy.py）增加了一个简单图形界面（GUI）。该图形界面使用PyQt4编写，主要目的是避免Windows下的黑窗口（command）运行模式。

# 下载安装 #
GAppProxy的新Windows软件包因为其体积较大，所以采用7zip格式压缩，为了避免客户端安装7zip压缩软件，压缩包使用自解压的方式，即为一个可执行文件（exe）。下载后双击执行，选择目录解压即可，GAppProxy客户端本身为绿色软件，不需要安装。

**特别提醒：安全起见，请到GAppProxy项目的下载页下载: http://code.google.com/p/gappproxy/downloads/list**

# 使用 #
使用设置包括两步:

  * 双击运行gui.exe。
  * 设置浏览器使用代理，代理地址端口为127.0.0.1:8000。

详细步骤及操作说明如下：

1，双击解压后目录下的gui.exe文件运行GAppProxy，默认初始界面如图，整体内容分两部分：

http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/2.PNG

## setup栏 ##
  * **setup栏可根据用户自身的网络状况进行设置，对于大部分用户来说不需要改动，默认配置即可。**

  * 如果你的电脑平常需要设置代理才能上网，请选中“Use Local Proxy”并在其后的输入框中填写代理地址，例如：

http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/6.PNG

  * 如果你需要使用指定的GAppProxy FetchServer，（这种情况一般发生在你自己在GAE上架设了FetchServer之后，如果你看不懂我说的意思，请略过这个选项。）请选中“Use Fetch Server”并填写其后的输入框，例如：

http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/7.PNG

  * 以上两部分填写完成后必须分别点击“Save”、“Quit”保存设置并重新启动GAppProxy方可生效。

## 其他按钮 ##
  * Status按钮：点击显示当前Proxy核心的运行状态，“running”表示Proxy运行正常，“exit”表示Proxy运行异常已退出，可能原因主要是网络不通等，具体可查看运行文件目录下的.log文件，显示分别如图：

http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/3.PNG
http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/4.PNG

  * Hide按钮：点击隐藏主窗口并且在系统右下角托盘栏增加一个绿圈状图标，在该图标上点击右键菜单的“Restore”项可以恢复显示主窗口，如图：

http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/5.PNG

  * Help按钮：点击显示一个简要帮助。

http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/8.PNG

  * About按钮：点击显示当前GAppProxy版本等相关信息。

http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/9.PNG

  * Quit按钮：点击弹出确认退出对话框，确认则退出GAppProxy。

2，正确设置浏览器使用代理，以IE为例（GAppProxy的默认地址端口为127.0.0.1:8000），IE中菜单选择 工具-->Internet选项-->连接-->局域网设置，如图：

http://gappproxy.googlecode.com/svn/wiki/images/GAppProxy_Manual_for_Windows/10.PNG

至此，如果能通过IE访问网页则GAppProxy设置成功。这时要是访问 http://www.ip138.com 等显示自身IP的网页，你会发现你来自不知道是哪了，呵呵。

有问题请到 http://groups.google.com/group/gappproxy 留言，谢谢。