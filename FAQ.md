## 1、为什么下载后文件打不开/出错？ ##

这是因为下载的原因，请换用一个支持续传的下载工具试试（专门的下载工具基本上都支持续传），不要用浏览器直接下载。

每个下载的文件，点击说明后，都会有一个校验码。如果在 SHA1 Checksum 匹配的情况下，仍然出现错误，请和我们联系，谢谢。：）

## 2、Fetch Server 是什么东西？ ##

GAppProxy 的代理分为两部分：

客户端：要使用 GAppProxy 的代理，这个是必须的。它运行在您的电脑上，随时准备为您服务；

服务端：这个是可选的。它运行在 Google App Engine(GAE) 上，为 GAppProxy 的客户端提供服务。

您下载客户端后即可立即使用 GAppProxy 的代理，它会使用默认的 Fetch Server。但是基于以下理由，我们建议您架设自己的 Fetch Server：

  * 默认的 Fetch Server 是很多人公用的，因此没有您自己的 Fetch Server 速度快；

  * 您能对自己的 Fetch Server 进行更多的控制，了解它的运行状况；

  * 给默认的 Fetch Server 减点压：）

## 3、建自己的 Fetch Server 收费的吗？ ##

不收：）

  * GAppProxy 的服务端程序和客户端一样是自由/开源的；

  * Google App Engine 是免费注册的。

## 4、怎么建自己的 Fetch Server？ ##

  * Windows用户请参考此文章：http://groups.google.com/group/gappproxy/browse_thread/thread/fafe05eb15395c0

  * Linux用户请参考此文章：http://groups.google.com/group/gappproxy/browse_thread/thread/3d0ad3dd6331311

## 5、GAppProxy 的代理安全吗？ ##

  * **请特别注意：GAppProxy提供的HTTPS服务并不安全。** 因为GAE的局限性，GAppProxy提供的HTTPS服务实际是在GAE端将真正的HTTPS页面内容取下，然后编码传回，在客户端将其再度包装为HTTPS样子，所以中间网络上是可能侦听到你的数据内容的。而真正的HTTPS代理提供的是端到端的安全性，中间网络上是不可能获取实际数据内容。

## 6、安全连接失败 / 安全证书有问题？ ##

  * 安全连接失败可能是因为你使用的Python或GAppProxy客户端版本过低，Windows用户请将GAppProxy客户端更新到1.0.0beta或更高版本。

  * GAE平台不支持数字证书验证，所以必然存在证书错误，继续浏览就是。

## 7、出错了怎么办？ ##

您别看见出来一堆英文就怕怕呵呵。**大部分\*都是提示信息，告诉您一些情况，**不影响\*继续使用。当然，也有的是错误。不管是提示还是错误，您只要阅读下输出的文字，大概都能明白是怎么回事。

常见的有：

```
socket.error: (98, 'Address already in use')
```
已经有一个在运行了，不用再重复打开了。：）



```
Message: Fetch server error, The target server may be down or not
exist. Another possibility: try to request the URL directly.
```
您要使用代理访问的网站下线了，或者已经不存在了~。

还有种可能是，某些国内的网站，因为某个原因 GAE 访问不到。既然是国内的网站，您就直接访问吧：）。

主要是前一种情况。



```
Error response

Error code 403.

Message: Forbidden.

Error code explanation: 403 = Request forbidden -- authorization will not help.
```

默认的／公共的 fetch server 流量超标了，建一个您自己的 fetch server 吧。


## 8、无法登录网站？ ##

是的，有些网站无法使用 GAppProxy 代理登录。这是因为目标网站和 GAE 平台双重限制的原因，除非两者中有一方放松限制……。

## 9、无法下载文件／观看视频？ ##

同上。

  * GAE 限制文件大小上限为1MB。

  * 有些网站会把来自 GAE 的请求当着盗链，拒绝提供下载。


## 10、GAppProxy 的客户端在 python 3.0 下运行出错？ ##

目前还不支持 py3.0，建议使用 2.6 的版本。 ：-）