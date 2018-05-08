@echo off
 setlocal
 rem for /f "tokens=*" %%a in ('dir %1 /b /od /a-d') do set latest=%%a

 for /r %1 %%g in (*.txt) do set latest=%%~nxg
 echo Latest File: %latest%

 echo build_number: %2
 
c:\python27\python c:\python\UpdateTestResultsPROD.py ..\Tests\results\%latest% %2