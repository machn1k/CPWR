@echo off
 setlocal
 
 echo started...
 
rem  for /f "tokens=*" %%a in ('dir "\\10.10.4.39\buildsenterprise\Daily\Topaz\trunk\archive" /b /od /t:c /ad-h') do set latest=%%a
for /f "tokens=*" %%a in ('dir "Z:\Daily\Topaz\trunk\archive" /b /od /t:c /ad-h') do set latest=%%a
 
 echo Latest Build %latest%
 
 echo Starting silent install...

 
"Z:\Daily\Topaz\trunk\archive\%latest%\CD image\Disk 1\cpwr\Topaz\Windows\Disk1\InstData\VM\install.exe" -f c:\\automated\\scriptData\\response.txt -i silent
 
rem "\\10.10.4.39\buildsenterprise\Daily\Topaz\trunk\archive\%latest%\CD image\Disk 1\cpwr\Topaz\Windows\Disk1\InstData\VM\install.exe" -f c:\\automated\\scriptData\\response.txt -i silent
 

 
 echo Finished silent install.