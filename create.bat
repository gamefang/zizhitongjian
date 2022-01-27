@echo off

REM 验证模板
cd template
	python update_template.py
cd ..

REM 1 -------------------
cd 1_主要數據
	csvtotable 通鑑目錄.csv 通鑑目錄.html -o -c 通鑑目錄 -vs -1 -e -dl 100
	csvtotable 人物總表.csv 人物總表.html -o -c 人物總表 -vs -1 -e -dl 100
	REM csvtotable 事件表.csv 事件表.html -o -c 事件表 -e -dl 100
	cd 政權年代表
		REM csvtotable 戰國秦.csv 戰國秦.html -o -c 戰國秦 -e
		csvtotable 漢.csv 漢.html -o -c 漢 -e
	cd ..
cd ..

REM 2 -------------------
REM cd 2_世系圖表
	REM cd 2.1_中國
	REM cd ..
	REM cd 2.2_四夷
		REM csvtotable 匈奴世系表.csv 匈奴世系表.html -o -c 匈奴世系表 -e
	REM cd ..
	REM cd 2.9_雜項
	REM cd ..
REM cd ..

REM 3 -------------------
REM cd 3_年代專項
	REM cd 3.5_東漢
		REM csvtotable 雲臺二十八將表.csv 雲臺二十八將表.html -o -c 雲臺二十八將表 -e
	REM cd ..
REM cd ..

REM 4 -------------------
cd 4_通用專項
	csvtotable 和親列表.csv 和親列表.html -o -c 和親列表 -e
cd ..

pause