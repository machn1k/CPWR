@ECHO OFF

echo Parsing RCPTT results for Host Services tests...

c:\python27\python c:\python\RCPTTResultsFileParser.py C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.hostservices-test\target\results\out.txt KB_HS "Topaz Workbench" 19.01.01 C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.hostservices-test\target\results\results.properties

echo Updating Zephyr tests...

c:\python27\python c:\python\UpdateZephyrRCPTT.py C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.hostservices-test\target\results\results.properties


echo Done!
