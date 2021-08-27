@echo off
REM pip install csvtotable

REM 1
cd 主要數據
csvtotable 通鑒目錄.csv 通鑒目錄.html -o -c 通鑒目錄 -e -dl 100
csvtotable 人物總表.csv 人物總表.html -o -c 人物總表 -vs -1 -e -dl 100
csvtotable 事件表.csv 事件表.html -o -c 事件表 -e -dl 100

cd 政權年代表
csvtotable 戰國秦.csv 戰國秦.html -o -c 戰國秦 -e
csvtotable 漢.csv 漢.html -o -c 漢 -e
cd ..

cd ..

REM 2
cd 年代專項

REM cd 秦末楚漢
REM csvtotable 秦末楚漢政權.csv 秦末楚漢政權.html -o -c 秦末楚漢政權 -e
REM cd ..

cd 西漢
REM csvtotable 西漢開國功臣列表.csv 西漢開國功臣列表.html -o -c 西漢開國功臣列表 -e
REM csvtotable 張騫通西域諸國概況.csv 張騫通西域諸國概況.html -o -c 張騫通西域諸國概況 -e
cd ..

cd 新朝
REM csvtotable 王莽寶貨制.csv 王莽寶貨制.html -o -c 王莽寶貨制 -e
cd ..

cd 東漢
csvtotable 云臺二十八將表.csv 云臺二十八將表.html -o -c 云臺二十八將表 -e
cd ..

cd ..

REM 3
cd 通用專項

cd 歷代世系圖
REM csvtotable 西漢世系表.csv 西漢世系表.html -o -c 西漢世系表 -e
cd ..

cd 雜項
REM csvtotable 干支表.csv 干支表.html -o -c 干支表 -e
REM csvtotable 攝提對照表.csv 攝提對照表.html -o -c 攝提對照表 -e
csvtotable 和親列表.csv 和親列表.html -o -c 和親列表 -e
REM csvtotable 被詛咒的趙王.csv 被詛咒的趙王.html -o -c 被詛咒的趙王 -e
REM csvtotable 百越各國.csv 百越各國.html -o -c 百越各國 -e
REM csvtotable 匈奴語對照表.csv 匈奴語對照表.html -o -c 匈奴語對照表 -e
cd ..

cd ..


pause