# -*- coding: utf-8 -*-
# 年號總表相關的分析工具

# 輸入的查詢字符串
QUERY_STR = '*自立'

# 年號總表文件路徑
FP = '1_數據表/1.3_各類通表/年號總表.csv'
# 必定模糊匹配的字段
ONLY_NOT_EXACT_PARAMS = ['備註']
# 數字對應漢字
NUM_IN_HAN = '十一二三四五六七八九'
NUM_UNIQUE = {1:'元',10:'十',11:'十一',12:'十二',13:'十三',14:'十四',15:'十五',16:'十六',17:'十七',18:'十八',19:'十九'}

__doc__ = '''
查詢指令示例：
220年的所有年號: 220
名為永寧的所有年號: 永寧
新朝的所有年號：政權：新朝
孫權用過的年號: 領袖：孫權
詳情查詢: *自立

1. 年份或年號定位
    輸入：年份數值，示例-220
    輸出：位於該年期間的所有年號
    輸入：年號，示例-永寧
    輸出：名為永寧的所有年號
    返回：(1, 0, 可能的索引號列表)
2. 字段篩選
    輸入：[字段名：XXX]，示例-領袖：孫權
    輸出：所有符合篩選的年號
    返回：(2, 0, 可能的索引號列表)
3. 顯示詳情
    輸入：@順序號，示例@3
    輸出：該年號的所有信息
    返回：(3, 精確的順序號, None)
4. 邏輯篩選
    暫不支持
5. 模糊匹配
    輸入：*內容，示例-*自立
    輸出：所有包含此內容的年號
    返回：(5, 0, 可能的索引號列表)

'''

def load_data_as_dict(csv_data):
    '''
    加載csv多行文本數據為嵌套字典，格式：
    {
        1 : {'起始年': '-179', '結束年': '-164', ...},
        2 : {'起始年': '-163', '結束年': '-157', ...},
        ...
    }
    '''
    dic_era = {}
    list_params = []
    lines = csv_data.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    for i, row in enumerate(lines):
        row_items = row.split(',')
        if i == 0:
            list_params = row_items
        else:
            dic_era[i] = {
                list_params[n] : row_items[n]
                for n in range(0, len(list_params))
            }
    return dic_era

def query(dic_era, input_str):
    '''
    年號表內的查詢功能
    '''
    query_mode = 0
    exact_key = 0
    likely = set()
    # 確定查詢模式
    input_str = input_str.strip().replace('：', ":")    # 也支持中文冒號
    if input_str.startswith('*') or input_str.endswith('*'):   # 模糊匹配
        query_mode = 5
        query_str = input_str.replace('*', '')

        for key, value in dic_era.items():
            for k,v in value.items():
                if query_str in v:
                    likely.add(key)
    elif input_str.startswith('@') or input_str.endswith('@'): # 顯示詳情
        query_mode = 3
        query_str = input_str.replace('@', '')

        if int(query_str) in dic_era.keys():
            exact_key = int(query_str)
    elif ':' in input_str:  # 字段篩選
        query_mode = 2
        param_name, query_str = input_str.split(':')

        param_name = param_name.strip()
        if param_name not in dic_era[1].keys():
            print(f'【{param_name}】字段名不存在！')
            return (query_mode, exact_key, likely)
        query_str = query_str.strip()

        for key, value in dic_era.items():
            is_exact = True # 默認精確匹配
            if param_name in ONLY_NOT_EXACT_PARAMS:  # 除部分字段只能模糊匹配
                is_exact = False
            if _match(query_str, value[param_name], is_exact):
                likely.add(key)
    else:   # 年代年號定位
        query_mode = 1
        param_name = ''
        query_str = input_str

        if query_str.isnumeric():   # 年份定位
            query_year = int(query_str)
            for key, value in dic_era.items():
                begin_year = int(value['起始年'])
                end_year = int(value['結束年'])
                if query_year >= begin_year and query_year <= end_year:
                    likely.add(key)
        else:   # 年號定位
            return query(dic_era, f'年號名稱：{query_str}')
    return (query_mode, exact_key, likely)

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

def year_delta(input_year, comp_year):
    '''
    求兩個年代的年份差值，主要用於適配公元切換情況
    '''
    if input_year * comp_year > 0:
        return comp_year - input_year
    else:
        return comp_year - input_year - 1

def view_query(dic_era, query_str):
    '''
    query方法的輸出
    '''
    query_str = query_str.strip()
    if (query_str == ""):   # 無查詢內容則輸出文檔
        return __doc__
    result = ''
    query_mode, exact_key, likely = query(dic_era, query_str)
    if query_mode == 3: # 顯示詳情
        if exact_key != 0:
            result += f'順序號：{exact_key}\n'
            data = dic_era[exact_key]
            for key, value in data.items():
                if value != '':
                    result += f'{key}: {value}\n'
    else:   # 其他情況
        result += f'【{query_str}】的符合的年號({len(likely)})：\n'
        if query_str.isnumeric():   # 年份定位
            for key in likely:
                value = dic_era[key]
                begin_year = int(value['起始年'])
                delta = year_delta(begin_year, int(query_str))
                era_num = delta + 1 # 紀年時間為差值加一年
                if era_num in NUM_UNIQUE.keys():
                    era_han = NUM_UNIQUE[era_num]
                else:
                    era_han = ''.join(NUM_IN_HAN[int(digit)] for digit in str(era_num))
                result += f"【{value['政權']}】{value['領袖']}-{value['年號名稱']}{era_han}年\n"
        else:
            for key in likely:
                value = dic_era[key]
                result += f'{key}【{value["年號名稱"]}】 {value["起始年"]}至{value["結束年"]} {value["政權"]}-{value["領袖"]}\n'
    return result[:-1] or f'【{query_str}】未找到數據！'

def mainjs(str_csv, input_str):
    '''
    供js調用的函數
    '''
    dic_era = load_data_as_dict(str_csv)
    result = view_query(dic_era, input_str)
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
        dic_era = load_data_as_dict(result_str)
        # 年號查詢
        print(view_query(dic_era, QUERY_STR))