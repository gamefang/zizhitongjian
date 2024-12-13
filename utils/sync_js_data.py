# -*- coding: utf-8 -*-
# 協助同步工具中js所需的數據

import os

# 需要同步的源文件、js文件路徑字典
DIC_TO_SYNC = {
    r'../1_數據表/1.3_各類通表/年號總表.csv': r'../tools/raw_data/data_era_name.js',
    r'../1_數據表/1.3_各類通表/人物總表.csv': r'../tools/raw_data/data_person.js',
}
# js文件樣式
JS_TEMPLATE = '''const RAW_DATA = `{0}`;'''

def sync_files(dic_to_sync, js_template):
    '''
    同步源文件為js文件數據
    '''
    for src_path, dest_path in dic_to_sync.items():
        with open(src_path, 'r', encoding='utf-8') as src_file:
            file_content = src_file.read()
        formatted_content = js_template.format(file_content)
        
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        with open(dest_path, 'w', encoding='utf-8') as dest_file:
            dest_file.write(formatted_content)
        print(f"JS file synchronized: {dest_path}")

if __name__ == '__main__':
    sync_files(DIC_TO_SYNC, JS_TEMPLATE)