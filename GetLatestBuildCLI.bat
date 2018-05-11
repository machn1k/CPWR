@echo off
 setlocal
 
 echo started...
 
 for /f "tokens=*" %%a in ('dir "X:\Daily\Topaz\trunk\archive" /b /od /t:c /ad-h') do set latest=%%a
 
 echo Latest Build %latest%
 
 echo Starting silent install...

 
 rem echo installdir "Z:\Daily\Topaz\trunk\archive\%latest%\CD image\Disk 1\cpwr\Topaz\Windows\Disk1\InstData\VM\install.exe"
 
 rem "\\10.10.4.39\buildsenterprise\Daily\Topaz\trunk\archive\%latest%\CD image\Disk 1\cpwr\Topaz\Windows\Disk1\InstData\VM\install.exe" -f c:\\automated\\scriptData\\response.txt -i silent
 "x:\Daily\Topaz\trunk\archive\%latest%\CD image\Disk 1\cpwr\TopazCLI\Windows\Disk1\InstData\noVM\install.exe" -f c:\\automated\\scriptData\\installer.properties -i silent
 

 
 echo Finished silent install.