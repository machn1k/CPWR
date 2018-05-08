@ECHO OFF

echo Parsing RCPTT results for Code Coverage tests...

c:\python27\python c:\python\RCPTTResultsFileParser.py C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.codecoverage-test\target\results\out.txt KB_CC "Topaz Workbench" 19.01.01 C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.codecoverage-test\target\results\results.properties

echo Updating Zephyr tests...

c:\python27\python c:\python\UpdateZephyrRCPTT.py C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.codecoverage-test\target\results\results.properties

echo Done!