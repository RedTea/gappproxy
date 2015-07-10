# GAppProxy #

  * ## 请先留意这里 ##
    * GAppProxy设计的初衷是为教育网用户提供一个免费的国际代理。
    * http://fetchserver1.appspot.com/fetch.py 等FetchServer的存在只是提供一个试用服务点，请需要Proxy的朋友自己设置fetch服务。
    * 感谢WCM、chijiao共享试用站点。
    * 感谢各位支持！

  * ## 什么是GAppProxy？ ##
    * 一个开源的HTTP Proxy软件。
    * 使用Python编写，运行于Google App Engine上。

  * ## GAppProxy的优势： ##
    * **是一个完整的Proxy解决方案：与常见的HTTP Proxy不同，GAppProxy运行在Google App Engine上，不需要专门的服务器，这是最大优势。**
    * 个人的Proxy：自己管理，自己使用。
    * 依托于Google App Engine：Google的网络比较可靠。

  * ## GAppProxy的劣势: ##
    * 仅支持标准80端口的HTTP协议和443端口的HTTPS协议,其他端口均不支持。
    * 需要安装客户端。

  * ## GAppProxy的设想用户: ##
    * 教育网用户(不能直接访问国外网络者)。
    * 其他需代理的用户。

  * ## GAppProxy目前的状态: ##
    * HTTP(S) Proxy功能已经可用,我们也在不断调整优化。
    * 最新版本：2.0.0

  * ## GAppProxy将要做的: ##
    * 完善Proxy的细节功能,提高用户体验。

  * ## 如何安装使用： ##
    * ### 普通Windows用户： ###
      * 下载GAppProxy的[Windows版客户端软件](http://gappproxy.googlecode.com/files/localproxy-2.0.0-win.zip)并解压，然后执行localproxy目录下的proxy.exe。
      * 配置浏览器,设置HTTP代理为127.0.0.1:8000。
    * ### 有Python 2.5以上版本解释器的Windows/Linux用户： ###
      * 下载GAppProxy的[Python版客户端](http://gappproxy.googlecode.com/files/localproxy-2.0.0.zip)并解压，运行localproxy目录下的proxy.py。
      * 配置浏览器，设置HTTP代理为127.0.0.1:8000。
      * 注意：支持HTTPS需要Python 2.6版本。
    * ### 拥有Google App帐号并且希望自己搭Proxy服务的用户： ###
      * 下载GAppProxy的[服务端源码包＋自动上传工具](http://gappproxy.googlecode.com/files/uploader-2.0.0-win.zip)和[GAppProxy安装使用手册](http://gappproxy.googlecode.com/files/GAppProxy使用手册.doc)，按照手册提示完成服务器部署。

  * ## 目前GAppProxy存在的问题: ##
    * 1,Web 登录问题: 部分Web系统无法正常登录,这个原因主要是和待登录网站要求的安全性以及GAE平台的局限性相关。
    * 2,为支持HTTPS,GAppProxy使用了一种妥协的方式,该方式从原理上破坏了HTTPS固有的安全性,将HTTPS的安全级别降到了HTTP级,所以如果你要传输重要数据,请不要使用该HTTPS代理.此外HTTPS不支持服务器/客户认证,这也和GAE有关。
    * 3,不支持大尺寸的文件上传,GAE 对上传文件尺寸有限制。
    * 最后,如果你还发现GAppProxy的什么问题或者有好的建议,请在 http://groups.google.com/group/gappproxy 留言,谢谢。

  * ## 其他 ##
    * 每个客户端(proxy.py/proxy.exe)我都会在Windows+IE/Firefox和Linux+Firefox下测试正常后再提交。

  * ## 有何更新?(详细内容请关注svn) ##
    * (10-10-06)**发布2.0.0版安装使用手册，包括和自动部署工具相关的内容。**
    * (10-10-06)**发布windows平台服务器自动部署工具，彻底不再需要安装python环境。**
    * (10-09-12)**发布2.0.0版，包含windows客户端。**
    * (09-02-27)**发布1.0.0beta版,windows版客户端支持HTTPS.**
    * (08-10-25)**Windows上Proxy客户端的运行模式由命令行窗口改为图形界面.**
    * (08-10-19)更新服务器负载均衡方式,由服务端选择FetchServer.
    * (08-09-18)**根据GAE API的变化做了一些功能增强,推荐使用r22以上版本.**
    * (08-07-01)支持本地代理,支持多fetch做负载均衡.
    * (08-06-30)从fetch.py服务代码中彻底删除记录用户源IP等全部日志相关功能.
    * (08-06-28)lovelywcm写了一篇详细的Proxy使用介绍文档,详情见本页wiki.
    * (08-06-26)给运行在GAE上的fetch服务添加了一个可显示页面,方便调试.
    * (08-06-26)lovelywcm将proxy.[r7](https://code.google.com/p/gappproxy/source/detail?r=7).py在windows下编译成系统服务.
    * (08-06-23)添加HTTPS支持,但需要Python 2.6版本支持.
    * (08-06-18)使用py2exe为没有安装Python解释器的用户提供直接可执行的proxy.exe.
    * (08-06-17)解决了proxy.py在Windows上运行不正常的问题,请更新proxy.py版本到r7以上.
    * (08-06-14)更加简化了统计功能,GAE提供的datastore当数据库用还是很弱的.
    * (08-06-14)修改了传输编码方式,使用zlib压缩,并且只针对text/×××文件类型.
    * (08-06-13)数据传输用base64做了简单编码.
    * (08-06-13)给服务器加了点统计功能,记录访问源IP,目的Host及是否成功.