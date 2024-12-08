# -*- coding: utf-8 -*-
# 人物總表相關的分析工具

import csv

# 輸入的查詢字符串
QUERY_STR = '人物組合：湯武'

# 人物總表文件路徑
FP_PERSON = '../1_數據表/1.3_各類通表/人物總表.csv'
# 必定模糊匹配的字段
ONLY_NOT_EXACT_PARAMS = ['簡述', '記載年備註', '備註']


def load_data(fp):
    '''
    加載csv數據為嵌套字典，格式：
    {
        1 : {'慣用名': '周威烈王', '通鑑目録': '10101', ...},
        2 : {'慣用名': '魏文侯', '通鑑目録': '10101', ...},
        ...
    }
    '''
    dic_person = {}
    list_params = []
    nokey_count = 1
    with open(fp, encoding='utf8', newline='') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:
                list_params = row
            else:
                key = int(row[0])
                if key == -1:   # 默認無編號索引
                    key = f'x{nokey_count}'
                    nokey_count += 1
                elif key in dic_person.keys():  # 重複索引號
                    print(f'WARNING: key {key} used more than one time!')
                dic_person[key] = {
                    list_params[n] : row[n]
                    for n in range(1, len(list_params))
                }
    return dic_person

def check_name(dic_person):
    '''
    檢查慣用名是否有重複，返回可能有問題的所有相關索引編號
    '''
    list_names = []
    wrong_keys = []
    dic_person_keys = list(dic_person.keys())
    for key, value in dic_person.items():
        name = value["慣用名"]
        if name in list_names:  # 重複出現
            used_index = list_names.index(name)
            used_key = dic_person_keys[used_index]
            if used_key not in wrong_keys:
                wrong_keys.append(used_key)
            wrong_keys.append(key)
        list_names.append(name) # 添加所有，確保下標對齊
    return wrong_keys

def query(dic_person, input_str):
    '''
    人物表內的查詢功能
    XXX -> 姓名查詢模式1：僅針對姓名進行查詢，返回：(1, 精確索引號, 可能的索引號列表, 相關的索引號列表)
    字段名：XXX -> 字段查詢模式2：找到固定字段符合表達式的內容，返回：(2, 0, 索引號列表, None)
    '''
    query_mode = 0
    exact_key = 0
    likely = set()
    relative = set()
    # 確定查詢模式
    input_str = input_str.strip().replace('：', ":")    # 也支持中文冒號
    if ':' in input_str:
        param_name, query_str = input_str.split(':')
        param_name = param_name.strip()
        if param_name not in dic_person[1].keys():
            print(f'【{param_name}】字段名不存在！')
            return (query_mode, exact_key, likely, relative)
        query_str = query_str.strip()
    else:
        param_name = ''
        query_str = input_str
    # 姓名查詢模式
    if (param_name == ''):
        query_mode = 1
        for key, value in dic_person.items():
            # 找精確索引號
            if _match(query_str, value['慣用名'], True):    # 精確匹配慣用名
                exact_key = key
                continue
            # 找可能索引號
            if _match(query_str, value['慣用名'], False): # 模糊匹配慣用名
                likely.add(key)
                continue
            if _match(query_str, value['通鑑名'], True): # 精確匹配通鑑名
                likely.add(key)
                continue
            if _match(query_str, value['別稱'], True): # 精確匹配別稱
                likely.add(key)
                continue
            # 找相關索引號
            if _match(query_str, value['簡述'], False): # 模糊匹配簡述
                relative.add(key)
                continue
            if _match(query_str, value['備註'], False): # 模糊匹配備註
                relative.add(key)
                continue
    # 字段查詢模式
    else:
        query_mode = 2
        for key, value in dic_person.items():
            is_exact = True # 默認精確匹配
            if param_name in ONLY_NOT_EXACT_PARAMS:  # 除部分字段只能模糊匹配
                is_exact = False
            if _match(query_str, value[param_name], is_exact):
                likely.add(key)
    return (query_mode, exact_key, likely, relative)

def _match(input, check, is_exact = True):
    '''
    判斷輸入內容是否符合條件
    input: 輸入條件
    check: 待檢查條件，可能為以|分隔的數組
    is_exact: 是否精確匹配字符串
    return: bool
    '''
    if '|' in check:    # 數組
        list_check = check.split('|')
        if is_exact:
            return input in list_check
        else:
            for item in list_check:
                if input in item:
                    return True
            return False
    else:   # 單一    
        if is_exact:
            return input == check
        else:
            return input in check
    
# 輸出方法
def view_check_name(dic_person):
    '''
    check_name方法的輸出
    '''
    wrong_name_keys = check_name(dic_person)
    if len(wrong_name_keys) != 0:
        print('檢查到可能重複的慣用名：')
        for item in wrong_name_keys:
            print(f'{item} {dic_person[item]["慣用名"]}')

def view_query(dic_person, query_str):
    '''
    query方法的輸出
    '''
    query_mode, exact_key, likely, relative = query(dic_person, query_str)
    if query_mode == 1:
        if exact_key != 0:
            print(f'【{query_str}】的索引號：{exact_key}')
        if len(likely) != 0:
            print(f'【{query_str}】可能是：')
            for item in likely:
                print(f'{item} {dic_person[item]["慣用名"]}')
        if len(relative) != 0:
            print(f'【{query_str}】相關人物：')
            for item in relative:
                print(f'{item} {dic_person[item]["慣用名"]}')
    elif query_mode == 2:
        print(f'【{query_str}】的符合的索引：')
        for item in likely:
            print(f'{item} {dic_person[item]["慣用名"]}')

            
if __name__ == '__main__':
    # 加載數據
    dic_person = load_data(FP_PERSON)
    # 檢查慣用名是否有重複
    view_check_name(dic_person)
    # 人物查找
    view_query(dic_person, QUERY_STR)
