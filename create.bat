@echo off

REM ��֤ģ��
cd template
	python update_template.py
cd ..

REM 1 -------------------
cd 1_��Ҫ����
	csvtotable ͨ�aĿ�.csv ͨ�aĿ�.html -o -c ͨ�aĿ� -vs -1 -e -dl 100
	csvtotable ���ￂ��.csv ���ￂ��.html -o -c ���ￂ�� -vs -1 -e -dl 100
	REM csvtotable �¼���.csv �¼���.html -o -c �¼��� -e -dl 100
	cd ���������
		REM csvtotable ������.csv ������.html -o -c ������ -e
		csvtotable �h.csv �h.html -o -c �h -e
	cd ..
cd ..

REM 2 -------------------
REM cd 2_��ϵ�D��
	REM cd 2.1_�Ї�
	REM cd ..
	REM cd 2.2_����
		REM csvtotable ��ū��ϵ��.csv ��ū��ϵ��.html -o -c ��ū��ϵ�� -e
	REM cd ..
	REM cd 2.9_�s�
	REM cd ..
REM cd ..

REM 3 -------------------
REM cd 3_������
	REM cd 3.5_�|�h
		REM csvtotable ��_��ʮ�ˌ���.csv ��_��ʮ�ˌ���.html -o -c ��_��ʮ�ˌ��� -e
	REM cd ..
REM cd ..

REM 4 -------------------
cd 4_ͨ�Ì��
	csvtotable ���H�б�.csv ���H�б�.html -o -c ���H�б� -e
cd ..

pause