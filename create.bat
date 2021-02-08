@echo off
REM pip install csvtotable

REM 1
cd 主要數據
csvtotable 通鑒目錄.csv 通鑒目錄.html -o -c 通鑒目錄 -e -dl 100
csvtotable 人物總表.csv 人物總表.html -o -c 人物總表 -e -dl 100

cd 政權年代表
csvtotable 戰國秦.csv 戰國秦.html -o -c 戰國秦 -e
csvtotable 漢.csv 漢.html -o -c 漢 -e
cd ..

cd ..

REM 2
cd 年代專項

cd 秦末楚漢
csvtotable 秦末楚漢政權.csv 秦末楚漢政權.html -o -c 秦末楚漢政權 -e
cd ..

cd 西漢
csvtotable 西漢開國功臣列表.csv 西漢開國功臣列表.html -o -c 西漢開國功臣列表 -e
cd ..

cd ..

REM 3
cd 通用專項

cd 雜項
csvtotable 干支表.csv 干支表.html -o -c 干支表 -e
csvtotable 攝提對照表.csv 攝提對照表.html -o -c 攝提對照表 -e
csvtotable 和親列表.csv 和親列表.html -o -c 和親列表 -e
csvtotable 被詛咒的趙王.csv 被詛咒的趙王.html -o -c 被詛咒的趙王 -e
cd ..

cd ..


pause