# -*- coding: utf-8 -*-
# 年號總表相關的分析工具

from common import *    # 部分通用方法

# 輸入的查詢字符串
QUERY_STR = '250'

# 年號總表文件路徑
FP = '1_數據表/1.3_各類通表/年號總表.csv'
# 數字對應漢字
NUM_IN_HAN = '十一二三四五六七八九'
NUM_UNIQUE = {1:'元',10:'十',11:'十一',12:'十二',13:'十三',14:'十四',15:'十五',16:'十六',17:'十七',18:'十八',19:'十九'}

# 路徑修正
FP = this_to_main_page(FP)

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
                for n in range(0, len(list_params) - 1)
            }
    return dic_era

def query(dic_era, input_str):
    '''
    年號表內的查詢及輸出
    輸入公元年，返回當年所有年號信息: 西漢-孺子嬰-居攝三年\n西漢-孺子嬰-始初元年\n新朝-王莽-始建國元年
    '''
    result = ''
    query_year = int(input_str.strip())
    for key, value in dic_era.items():
        begin_year = int(value['起始年'])
        end_year = int(value['結束年'])
        if query_year >= begin_year and query_year <= end_year:
            delta = year_delta(begin_year, query_year)
            era_num = delta + 1 # 紀年時間為差值加一年
            if era_num in NUM_UNIQUE.keys():
                era_han = NUM_UNIQUE[era_num]
            else:
                era_han = ''.join(NUM_IN_HAN[int(digit)] for digit in str(era_num))
            result += f"【{value['政權']}】{value['領袖']}-{value['年號名稱']}{era_han}年\n"
    return result[:-1]

def year_delta(input_year, comp_year):
    '''
    求兩個年代的年份差值，主要用於適配公元切換情況
    '''
    if input_year * comp_year > 0:
        return comp_year - input_year
    else:
        return comp_year - input_year - 1
    
if __name__ == '__main__':
    # 加載數據
    result_str = csv_loader(FP)
    dic_era = load_data_as_dict(result_str)
    # 年號查詢
    print(query(dic_era, QUERY_STR))
