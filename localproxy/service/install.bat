sc stop GAppProxy
sc delete GAppProxy
sc create GAppProxy binPath= "%~dp0srvany.exe" start= auto
sc description GAppProxy "HTTP 代理服务 - GAppProxy 为您效劳。"
reg add HKLM\SYSTEM\CurrentControlSet\Services\GAppProxy\Parameters /v Application /d "%~dp0..\proxy.exe" /f
reg add HKLM\SYSTEM\CurrentControlSet\Services\GAppProxy\Parameters /v AppDirectory /d "%~dp0..\" /f
sc start GAppProxy
::@echo.
::@echo 安装已完成，GAppProxy 服务已经启动。
::@echo.
::@echo 您可以关闭这个窗口，开始使用代理了。
::@echo.
::@echo Enjoy it :-)
::@echo.
::@pause