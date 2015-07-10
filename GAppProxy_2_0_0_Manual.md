#summary GAppProxy-2.0.0安装使用说明
#labels Featured,Phase-Deploy

# GAppProxy-2.0.0安装使用手册 #
**GAppProxy基于Google App Engine，所以首先需要准备一个google账号（即gmail账号）。**

## 申请GAE空间并创建新的的app\_id： ##
**1，打开浏览器，输入http://appengine.google.com/ 输入gmail用户密码登入。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/1.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/1.png)

**2，点击“Create an Application”。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/2.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/2.png)

**3，申请GAE需要用手机认证，输入自己的手机号，注意前面需要写+86。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/3.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/3.png)

**4，手机收到验证码后输入验证，验证成功后GAE申请完成。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/4.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/4.png)

**5，创建新app\_id，比如这里我使用了gappproxy200，注意记下该app\_id，后面还会再用到。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/5.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/5.png)

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/6.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/6.png)

## 部署GAppProxy服务器： ##
**1，从GAppProxy项目下载页 http://code.google.com/p/gappproxy/downloads/list 下载服务器源码包+自动部署工具，即uploader-2.0.0-win.zip。**

**2，解压下载文件，双击执行该目录下的uploader.exe，在AppID提示后输入刚才创建的app\_id，然后分别按提示输入自己的gmail用户名和密码（注意，输入密码时不会有任何显示）：**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/7.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/7.png)

**3，等待直到出现如下图的“ready to…”字样，表示部署完成。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/8.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/8.png)

**4，在浏览器中输入http://xxx.appspot.com/fetch.py ，注意将其中的xxx换成刚才创建的app\_id，如果显示如下图，说明服务器已经生效，否则可以多刷新几次试试。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/12.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/12.png)

## 安装客户端： ##
**1，从GAppProxy项目下载页 http://code.google.com/p/gappproxy/downloads/list 下载windows客户端，即localproxy-2.0.0-win.zip。**

**2，解压下载文件，用记事本打开并修改该目录下的proxy.conf文件，增加如下图的最后一行，特别注意红字部分改成刚才创建的app\_id，另外注意这行前面没有“#”。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/9.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/9.png)

**3，执行该目录下的proxy.exe，并设置浏览器代理，分别如下图：**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/10.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/10.png)

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/11.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/11.png)

**4，至此代理设置全部完成，在浏览器中输入http://www.geoiptool.com/ ，看看自己的ip在哪里。**

![http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/13.png](http://gappproxy.googlecode.com/svn/wiki/images/2.0.0Manual/13.png)