# -*- coding: utf-8 -*-
# 部分通用方法

import os

def csv_loader(fp):
    '''
    加載csv數據為多行文本，不使用csv模塊，便於轉化為js
    '''
    with open(fp, 'r', encoding='utf8', newline='') as f:
        lines = f.readlines()
    return '\n'.join(lines)

def this_to_main_page(fp):
    '''
    找到此文件以主頁起始的路徑
    '''
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), fp)