@echo off
REM pip install csvtotable

REM 1 -------------------
cd 1_��Ҫ����

csvtotable ͨ�bĿ�.csv ͨ�bĿ�.html -o -c ͨ�bĿ� -e -dl 100
csvtotable ���ￂ��.csv ���ￂ��.html -o -c ���ￂ�� -vs -1 -e -dl 100
REM csvtotable �¼���.csv �¼���.html -o -c �¼��� -e -dl 100

cd ���������
csvtotable ������.csv ������.html -o -c ������ -e
csvtotable �h.csv �h.html -o -c �h -e
cd ..

cd ..
REM -------------------

REM 2 -------------------
cd 2_��ϵ�D��

REM cd 2.1_�Ї�
REM cd ..

cd 2.2_����
csvtotable ��ū��ϵ��.csv ��ū��ϵ��.html -o -c ��ū��ϵ�� -e
cd ..

REM cd 2.9_�s�
REM cd ..

cd ..
REM -------------------

REM 3 -------------------
cd 3_������

cd 3.5_�|�h
csvtotable ��_��ʮ�ˌ���.csv ��_��ʮ�ˌ���.html -o -c ��_��ʮ�ˌ��� -e
cd ..

cd ..
REM -------------------

REM 4 -------------------
cd 4_ͨ�Ì��
csvtotable ���H�б�.csv ���H�б�.html -o -c ���H�б� -e
cd ..
REM -------------------

pause