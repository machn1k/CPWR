@ECHO OFF

echo zipping-up Code Coverage HTML results file...
echo ------------------------------------------

cd C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.codecoverage-test\target\results
"c:\Program Files\7-Zip\7z.exe" a -mx "cc.zip" "*.html" "images\*"
copy cc.zip C:\jenkins\workspace\RCPTT-Topaz-Nightly\reports 
echo Done!

echo zipping-up Host Services HTML results file...
echo ------------------------------------------

cd C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.hostservices-test\target\results
"c:\Program Files\7-Zip\7z.exe" a -mx "hs.zip" "*.html" "images\*" 
copy hs.zip C:\jenkins\workspace\RCPTT-Topaz-Nightly\reports
echo Done!

echo zipping-up Xpediter HTML results file...
echo ------------------------------------------

cd C:\jenkins\workspace\RCPTT-Topaz-Nightly\com.compuware.mf.topaz.rcptt.xpediter-test\target\results
"c:\Program Files\7-Zip\7z.exe" a -mx "xt.zip" "*.html" "images\*" 
copy xt.zip C:\jenkins\workspace\RCPTT-Topaz-Nightly\reports
echo Done!
