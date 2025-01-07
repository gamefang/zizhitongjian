# -*- coding: utf-8 -*-
# 人物總表相關的分析工具

# 輸入的查詢字符串
QUERY_STR = '*後漢書'

# 人物總表文件路徑
FP = '1_數據表/1.3_各類通表/人物總表.csv'
# 必定模糊匹配的字段
ONLY_NOT_EXACT_PARAMS = ['簡述', '記載年備註', '備註']

__doc__ = '''
查詢指令示例：
查詢張讓的信息：張讓
司馬遷的詳細信息：@司馬遷
只知道人物和後漢書有關，不知道哪方面有關：*後漢書
蜀漢的統治者：統治政權：蜀漢
表字為仲達或子上的：字：仲達or字：子上
和仇池政權有關的：統治政權：仇池or從屬政權：仇池
北魏的女性：從屬政權：北魏and女性：1

1. 人物定位
    輸入：[慣用名]或[索引號]，示例-司馬遷 或 2008
    輸出：精確匹配的索引號、可能的索引號列表、與輸入相關聯的索引號列表
    返回值：(1, 精確索引號, 可能的索引號列表, 相關的索引號列表)
2. 字段篩選
    輸入：[字段名：XXX]，示例-統治政權：新朝
    輸出：符合字段關鍵字的所有索引號
    返回值：(2, 0, 索引號列表, None)
3. 顯示詳情
    輸入：[@慣用名]或[@索引號]，示例-@司馬遷 或 @2008 或 2008@
    輸出：人物總表內記録的該詞條所有內容，必須精確匹配
    返回值：(3, 精確索引號, None, None)
4. 邏輯篩選
    輸入：[字段名1：XXX]and[字段名2：XXX]...，示例-女性：0and從屬政權：東漢
    輸出：類似字段篩選，但支持一重邏輯條件
    說明：支持and和or，可以多個and或多個or，但不支持混用
    返回值：(4, 0, 索引號列表, None)
5. 模糊匹配
    輸入：[*XXX]，示例-*敬仲 或 敬仲*
    輸出：列出所有包含輸入關鍵詞的索引號，模糊匹配
    返回值：(5, 0, 索引號列表, None)
'''

def load_data_as_dict(csv_data):
    '''
    加載csv多行文本數據為嵌套字典，格式：
    {
        1 : {'慣用名': '周威烈王', '通鑑目録': '10101', ...},
        2 : {'慣用名': '魏文侯', '通鑑目録': '10101', ...},
        ...
    }
    '''
    dic_person = {}
    list_params = []
    nokey_count = 1
    lines = csv_data.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    for i, row in enumerate(lines):
        row_items = row.split(',')
        if i == 0:
            list_params = row_items
        else:
            key = int(row_items[0])
            if key == -1:   # 默認無編號索引
                key = f'x{nokey_count}'
                nokey_count += 1
            elif key in dic_person.keys():  # 重複索引號
                print(f'WARNING: key {key} used more than one time!')
            dic_person[key] = {
                list_params[n] : row_items[n]
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
    '''
    query_mode = 0
    exact_key = 0
    likely = set()
    relative = set()
    # 確定查詢模式
    input_str = input_str.strip().replace('：', ":")    # 也支持中文冒號
    if input_str.startswith('*') or input_str.endswith('*'):   # 模糊匹配
        query_mode = 5
        query_str = input_str.replace('*', '')

        for key, value in dic_person.items():   # 精確匹配索引號或慣用名
            if _is_exact(query_str, key, value):
                exact_key = key
                continue
            # 非精確匹配情況
            for k, v in value.items():
                if query_str in v:
                    likely.add(key)
    elif input_str.startswith('@') or input_str.endswith('@'): # 顯示詳情
        query_mode = 3
        query_str = input_str.replace('@', '')

        for key, value in dic_person.items():
            if _is_exact(query_str, key, value):
                exact_key = key
                break
    elif 'and' in input_str: # 邏輯篩選
        query_mode = 4
        list_input = input_str.split('and')
        list_query = [query(dic_person, input_str) for input_str in list_input] # 遞歸調用字段篩選
        non_empty_set = [s[2] for s in list_query if s[2]]
        if non_empty_set:
            likely = set.intersection(*non_empty_set)   # 交集
    elif 'or' in input_str: # 邏輯篩選
        query_mode = 4
        list_input = input_str.split('or')
        list_query = [query(dic_person, input_str) for input_str in list_input] # 遞歸調用字段篩選
        non_empty_set = [s[2] for s in list_query if s[2]]
        if non_empty_set:
            likely = set.union(*non_empty_set)   # 並集
    elif ':' in input_str:  # 字段篩選
        query_mode = 2
        param_name, query_str = input_str.split(':')

        param_name = param_name.strip()
        if param_name not in dic_person[1].keys():
            print(f'【{param_name}】字段名不存在！')
            return (query_mode, exact_key, likely, relative)
        query_str = query_str.strip()

        for key, value in dic_person.items():
            is_exact = True # 默認精確匹配
            if param_name in ONLY_NOT_EXACT_PARAMS:  # 除部分字段只能模糊匹配
                is_exact = False
            if _match(query_str, value[param_name], is_exact):
                likely.add(key)
    else:   # 人物定位
        query_mode = 1
        param_name = ''
        query_str = input_str

        for key, value in dic_person.items():
            # 找精確索引號
            if _is_exact(query_str, key, value):
                exact_key = key
                query_mode = 3  # 精確索引號不需要@
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
    return (query_mode, exact_key, likely, relative)

def _match(input, check, is_exact = True):
    '''
    判斷輸入內容是否符合條件
    input: 輸入條件
    check: 待檢查條件，可能為以|分隔的數組
    is_exact: 是否精確匹配字符串
    return: bool
    '''
    if isinstance(input, int):  # 數值
        if is_exact:
            return str(input) == str(check)
        else:
            return str(input) in str(check)
    elif '|' in check:    # 數組
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
        
def _is_exact(query_str, key, value):
    '''
    判斷是否精確匹配
    query_str: 查詢字符串或數值
    key: 數據字典條目的key
    value: 數據字典條目的value
    return: bool
    '''
    is_num = query_str.isnumeric()
    if is_num and _match(int(query_str), key, True):    # 精確匹配索引號
        return True
    if not is_num and _match(query_str, value['慣用名'], True): # 精確匹配慣用名
        return True
    return False
    
# 輸出方法
def view_check_name(dic_person):
    '''
    check_name方法的輸出
    '''
    result = ''
    wrong_name_keys = check_name(dic_person)
    if len(wrong_name_keys) != 0:
        result += '檢查到可能重複的慣用名：\n'
        for item in wrong_name_keys:
            result += f'{item} {dic_person[item]["慣用名"]}\n'
    return result[:-1]

def view_query(dic_person, query_str):
    '''
    query方法的輸出
    '''
    query_str = query_str.strip()
    if (query_str == ""):   # 無查詢內容則輸出文檔
        return __doc__
    result = ''
    query_mode, exact_key, likely, relative = query(dic_person, query_str)
    if query_mode == 1: # 人物定位
        if exact_key != 0:
            result += f'【{query_str}】的索引號：{exact_key} 慣用名：{dic_person[exact_key]["慣用名"]}\n'
        if len(likely) != 0:
            result += f'【{query_str}】可能是({len(likely)})：\n'
            for item in likely:
                result += f'{item} {dic_person[item]["慣用名"]}\n'
        if len(relative) != 0:
            result += f'【{query_str}】相關人物({len(relative)})：\n'
            for item in relative:
                result += f'{item} {dic_person[item]["慣用名"]}\n'
    elif query_mode in (2, 4, 5):   # 字段篩選、邏輯篩選、模糊匹配
        result += f'【{query_str}】的符合的索引({len(likely)})：\n'
        for item in likely:
            result += f'{item} {dic_person[item]["慣用名"]}\n'
    elif query_mode == 3:   # 顯示詳情
        if exact_key != 0:
            result += f'【{query_str}】的索引號：{exact_key}\n'
            data = dic_person[exact_key]
            for key, value in data.items():
                if value != '':
                    result += f'{key}：{value}\n'
    return result[:-1] or f'【{query_str}】未找到數據！'

def mainjs(str_csv, input_str):
    '''
    供js調用的函數
    '''
    dic_person = load_data_as_dict(str_csv)
    result = view_query(dic_person, input_str)
    return result.replace('\n', '<br/>')

if __name__ == '__main__':
    try:    # js環境
        import js   # type: ignore  # 忽略 Pylance 的报错
    except: # py本地環境
        from common import *    # 部分通用方法
        # 路徑修正
        FP = this_to_main_page(FP)
        # 加載數據
        result_str = csv_loader(FP)
        dic_person = load_data_as_dict(result_str)
        # 檢查慣用名是否有重複
        print(view_check_name(dic_person))
        # 人物查找
        print(view_query(dic_person, QUERY_STR))
