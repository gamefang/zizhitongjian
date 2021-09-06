@echo off
REM pip install csvtotable

REM 1 -------------------
cd 1_主要數據

csvtotable 通鑒目錄.csv 通鑒目錄.html -o -c 通鑒目錄 -e -dl 100
csvtotable 人物總表.csv 人物總表.html -o -c 人物總表 -vs -1 -e -dl 100
REM csvtotable 事件表.csv 事件表.html -o -c 事件表 -e -dl 100

cd 政權年代表
csvtotable 戰國秦.csv 戰國秦.html -o -c 戰國秦 -e
csvtotable 漢.csv 漢.html -o -c 漢 -e
cd ..

cd ..
REM -------------------

REM 2 -------------------
cd 2_世系圖表

REM cd 2.1_中國
REM cd ..

cd 2.2_四夷
csvtotable 匈奴世系表.csv 匈奴世系表.html -o -c 匈奴世系表 -e
cd ..

REM cd 2.9_雜項
REM cd ..

cd ..
REM -------------------

REM 3 -------------------
cd 3_年代專項

cd 3.5_東漢
csvtotable 雲臺二十八將表.csv 雲臺二十八將表.html -o -c 雲臺二十八將表 -e
cd ..

cd ..
REM -------------------

REM 4 -------------------
cd 4_通用專項
csvtotable 和親列表.csv 和親列表.html -o -c 和親列表 -e
cd ..
REM -------------------

pause