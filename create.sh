#!/bin/bash
# 复制bat中内容，替换 REM 为 # 即可

# 验证模板
cd template
	python update_template.py
cd ..

# 1 -------------------
cd 1_數據表
	cd 1.1_通鑑目録
		csvtotable 時代表.csv 時代表.html -o -c 時代表 -e
		csvtotable 卷目表.csv 卷目表.html -o -c 卷目表 -e
		csvtotable 章節表.csv 章節表.html -o -c 章節表 -vs -1 -e -dl 100
	cd ..
	cd 1.2_政權年代表
		csvtotable 戰國秦.csv 戰國秦.html -o -c 戰國秦 -e
		csvtotable 漢.csv 漢.html -o -c 漢 -e
		csvtotable 魏晉南北朝.csv 魏晉南北朝.html -o -c 魏晉南北朝 -e
		
		csvtotable 年號總表.csv 年號總表.html -o -c 年號總表 -vs -1 -e -dl 100
	cd ..
	cd 1.3_各類通表
		csvtotable 人物總表.csv 人物總表.html -o -c 人物總表 -vs -1 -e -dl 100
	cd ..
cd ..

# 2 -------------------

csvtotable 2_世系圖表/2.2_并立政權/秦朝楚漢/秦末楚漢政權.csv 2_世系圖表/2.2_并立政權/秦朝楚漢/秦末楚漢政權.html -o -c 秦末楚漢政權 -e
csvtotable 2_世系圖表/2.2_并立政權/漢/東漢末年勢力列表.csv 2_世系圖表/2.2_并立政權/漢/東漢末年勢力列表.html -o -c 東漢末年勢力列表 -e

# 3 -------------------
csvtotable 3_專項研究/3.1_時代/西漢/西漢開國功臣列表.csv 3_專項研究/3.1_時代/西漢/西漢開國功臣列表.html -o -c 西漢開國功臣列表 -e
csvtotable 3_專項研究/3.1_時代/西漢/張騫通西域諸國概況.csv 3_專項研究/3.1_時代/西漢/張騫通西域諸國概況.html -o -c 張騫通西域諸國概況 -e
csvtotable 3_專項研究/3.1_時代/新/王莽寶貨制.csv 3_專項研究/3.1_時代/新/王莽寶貨制.html -o -c 王莽寶貨制 -e
csvtotable 3_專項研究/3.1_時代/東漢/雲臺二十八將表.csv 3_專項研究/3.1_時代/東漢/雲臺二十八將表.html -o -c 雲臺二十八將表 -e
csvtotable 3_專項研究/3.1_時代/東晉/五胡十六國列表.csv 3_專項研究/3.1_時代/東晉/五胡十六國列表.html -o -c 五胡十六國列表 -e

cd 3_專項研究/3.2_通用
	csvtotable 粗線條歷史朝代表.csv 粗線條歷史朝代表.html -o -c 粗線條歷史朝代表 -e
	csvtotable 和親列表.csv 和親列表.html -o -c 和親列表 -e
	csvtotable 被詛咒的趙王.csv 被詛咒的趙王.html -o -c 被詛咒的趙王 -e
	csvtotable 百越各國.csv 百越各國.html -o -c 百越各國 -e
	csvtotable 匈奴語對照表.csv 匈奴語對照表.html -o -c 匈奴語對照表 -e
cd ..
cd ..

echo "Press any key to exit..."
read -n 1