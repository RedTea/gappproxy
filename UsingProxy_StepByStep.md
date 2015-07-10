**说明**：本文介绍使用浏览器访问网站时如何使用代理，其它应用您可能需要参考其它文章。

# 一、什么是代理 #

通常来说，您是直接向网站服务器发送请求，并接受数据的，就像下面这个图一样：

![http://gappproxy.googlecode.com/svn/wiki/images/surf-normally.png](http://gappproxy.googlecode.com/svn/wiki/images/surf-normally.png)

使用代理后，您不再直接与网站服务器通信，而是通过一个代理服务器作为中转：

![http://gappproxy.googlecode.com/svn/wiki/images/surf-through-proxy.png](http://gappproxy.googlecode.com/svn/wiki/images/surf-through-proxy.png)


# 二、为什么要使用代理 #

如您所见，使用代理有点多此一举的味道。但它有时能给您带来额外的好处，或者，您不得不使用代理。比如：

  * 如果您处于教育网内，使用 GAppProxy 提供的代理也许能帮您节约国际流量费用；

  * 如果您没有使用某一项服务的权限，那么一个具备相应权限的代理可以帮助您解决这个问题；

  * 如果有人在你和目标服务器之间阻扰您的通信，您可以使用代理绕过这一限制；

  * 有些代理会将您的信息加密后再传输，一定程度上提高了安全性；

  * 有些网站会试图记录您的信息，如果您不希望被记录，可以使用代理达到匿名的效果。

# 三、设置代理的通用方法 #

### 1. 常见的浏览器，都可以通过菜单设置代理 ###

**Firefox** 浏览器：工具/编辑 --> 选项/首选项 --> 高级 --> 网络 --> 连接 --> 设置

**Internet Explorer** 浏览器：工具 --> Internet 选项 --> 连接 --> 局域网设置

> 其它浏览器也大抵若是。

> 请记住 GAppProxy 的配置：
```
HTTP 代理: 127.0.0.1
端口: 8000 
```

> ![http://gappproxy.googlecode.com/svn/wiki/images/browser-setting-proxy.png](http://gappproxy.googlecode.com/svn/wiki/images/browser-setting-proxy.png)

### 2. 使用 PAC 文件，强大、智能 ###

> 请回顾上一种方法：如果您设置了浏览器的代理，那么您所有的浏览都将通过代理访问，不管您需不需要。是不是很麻烦？PAC（Proxy Auto-Config，代理自动配置）即为此而生。PAC 定义了各种测试条件，只有满足条件的访问才会使用代理。**或者说，您可以自由定义哪些网站使用代理、使用哪个代理**。

> 首先，您需要创建一个文本文件，名称随意，但扩展名必须为 pac。如：proxy.pac

> PAC 采用的是 JavaScript 的语法。您必须定义一个 FindProxyForURL 函数，它就像 C语言 中的 main 函数。看起来应该像这个样子：
```
function FindProxyForURL(url, host){
   if ()
      return "";
   else
      return "";
}
```

> 浏览器通过调用这个函数而获知是否应该使用代理。它将当前访问信息通过 url 和 host 两个参数传递给 FindProxyForURL 函数，进而进行判断。

**url:** 指完整的网址，如：http://www.example.com:8080/abc/def/g/hij.html

**host:** 指从 "://" 到其后第一个 "/" 之间的内容，不包括端口号。如上面 url 的 host 是：www.example.com

> 有十几个内置函数可供您根据 url 和 host 参数进行判断，下面为您介绍两个最常用的：
**dnsDomainIs():** “dns Domain Is”，主要用来判断域名是否满足条件，常用格式为 dnsDomainIs(host, "xxx.com")。

上面的表达式，host="xxx.com" 或者 host="yyy.xxx.com" 时返回值均为 true。当然，host="xxxx.com" 时，返回 false。

**shExpMatch():** “shell Expression Match”，使用通配符判断 url 或 host 是否满足条件。

> 以下是一个实际的例子，意思是：用 GAppProxy 提供的代理（127.0.0.1:8000）访问美国高校网站、用 Tor 提供的代理（127.0.0.1:9050）访问百度和中国政府网站，其它的则直接连接。您可以在此基础上稍做修改，使之符合您的个性化需求。
```
function FindProxyForURL(url, host){
   if ( dnsDomainIs(host, ".edu") )
      return "PROXY 127.0.0.1:8000";
   else if ( dnsDomainIs(host, "www.baidu.com") || shExpMatch(url, "*.gov.cn/*") )
      return "SOCKS 127.0.0.1:9050";
   else
      return "DIRECT";
}
```

> 关于 PAC 更详尽的说明，请参见这里：http://en.wikipedia.org/wiki/Proxy_auto-config

# 四、Firefox 扩展可助您更方便地使用代理 #

如果您是 Firefox 的用户，那么恭喜您，您有更多、更好的选择！

### 1. MultiProxy Switch ###

> MultiProxy Switch 是一款国人开发的、支持多个代理的、简单易用的 Firefox 扩展。

> 它的安装地址是：https://addons.mozilla.org/zh-CN/firefox/addon/7330

> 安装后，设置界面如下：

> ![http://gappproxy.googlecode.com/svn/wiki/images/multiproxy-switch-setting.png](http://gappproxy.googlecode.com/svn/wiki/images/multiproxy-switch-setting.png)

> 请记住 GAppProxy 的配置：
```
HTTP 代理: 127.0.0.1
端口: 8000 
```

> 它会在状态栏添加一个小图标，您随时可以通过这个图标选择使用哪个，或者是否使用代理：

> ![http://gappproxy.googlecode.com/svn/wiki/images/multiproxy-switch-status.png](http://gappproxy.googlecode.com/svn/wiki/images/multiproxy-switch-status.png)


### 2. AutoProxy ###

> 专为国内网络环境设计，自动化代理扩展。内置 GAppProxy 的信息，无需设置。

> http://www.autoproxy.org/zh-CN/


> http://www.geektang.com/2009/03/autoproxy.html


# Enjoy :) #