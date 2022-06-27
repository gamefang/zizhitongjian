#!/bin/bash
# 复制bat中内容，替换 # 为 # 即可

# 验证模板
cd template
	python update_template.py
cd ..

# 1 -------------------
cd 1_主要數據
	csvtotable 通鑑目錄.csv 通鑑目錄.html -o -c 通鑑目錄 -vs -1 -e -dl 100
	csvtotable 人物總表.csv 人物總表.html -o -c 人物總表 -vs -1 -e -dl 100
	# csvtotable 事件表.csv 事件表.html -o -c 事件表 -e -dl 100
	cd 政權年代表
		csvtotable 戰國秦.csv 戰國秦.html -o -c 戰國秦 -e
		csvtotable 漢.csv 漢.html -o -c 漢 -e
		csvtotable 魏晉南北朝.csv 魏晉南北朝.html -o -c 魏晉南北朝 -e
	cd ..
cd ..

# 2 -------------------
# cd 2_世系圖表
	# cd 2.1_中國
	# cd ..
	# cd 2.2_四夷
		# csvtotable 匈奴世系表.csv 匈奴世系表.html -o -c 匈奴世系表 -e
	# cd ..
	# cd 2.9_雜項
	# cd ..
# cd ..

# 3 -------------------
# cd 3_年代專項
	# cd 3.5_東漢
		# csvtotable 東漢末年勢力列表.csv 東漢末年勢力列表.html -o -c 東漢末年勢力列表 -e
	# cd ..
# cd ..

# 4 -------------------
cd 4_通用專項
	csvtotable 和親列表.csv 和親列表.html -o -c 和親列表 -e
	csvtotable 年號總表.csv 年號總表.html -o -c 年號總表 -vs -1 -e -dl 100
cd ..

echo "Press any key to exit..."
read -n 1