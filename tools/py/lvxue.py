# -*- coding: utf-8 -*-
# 律學相關算法

HUANGZHONG = 900    # 黃鐘管長度
PITCH_NAME = ['C','C♯','D','D♯','E','F','F♯','G','G♯','A','A♯','B']    # 標準音名
PITCH_NAME_ZH = ['黃鐘','大呂','太簇','夾鐘','姑冼','中呂','蕤賓','林鐘','夷則','南呂','無射','應鐘']   # 十二律音名

SANFENSUNYI_TO_EQUAL_ORDER = [0,7,2,9,4,11,6,1,8,3,10,5] # 五度相生順序
MILV = 2 ** (1/12)  # 朱載堉新法密律

def sanfensunyi(first_value, times = 13):
    '''
    中國古代三分損益法或畢達哥拉斯學派五度相生律，2/3 4/3輪換
    first_value: 首音值
    times: 計算執行次數，首音為第0次，不足一個八度的會補全
    return: 計算後值的List[float]，以音名高低順序排列
    '''
    result = []
    for i in range(times):
        if i == 0:
            this_value = first_value
        elif i % 2 == 1:
            this_value = last_value * 2/3   # 三分損一
        else:
            this_value = last_value * 4/3   # 三分益一
        this_value = octave_clamp(this_value, first_value)  # 約束在一個八度內
        result.append(this_value)
        last_value = this_value
    return _rearrange_list(result, SANFENSUNYI_TO_EQUAL_ORDER, is_forward = True)

def hechengtian_xinlv(first_value, times = 13):
    '''
    何承天新律，將三分損益法的黃鐘差值均分回十二音中
    first_value: 首音值
    times: 計算執行次數，首音為第0次，不足一個八度的會補全
    return: 計算後值的List[float]，以音名高低順序排列
    '''
    result = []
    sanfensunyi_result = sanfensunyi(first_value, 13)
    sanfensunyi_result = _rearrange_list(sanfensunyi_result, SANFENSUNYI_TO_EQUAL_ORDER, is_forward = False) # 三分損益計算順序還原
    delta = abs(sanfensunyi_result[12] - sanfensunyi_result[0]) # 三分損益法差值
    add_value = delta / 12  # 均分差值
    for i in range(times):
        ori_value = sanfensunyi_result[i % 12]
        this_value = ori_value + add_value * (i % 12)   # 差值補回十二律中
        result.append(this_value)
    return _rearrange_list(result, SANFENSUNYI_TO_EQUAL_ORDER, is_forward = True)

def equal_temperament(first_value, times = 13):
    '''
    朱載堉十二平均律
    first_value: 首音值
    times: 計算執行次數，首音為第0次
    return: 計算後值的List[float]，以音名高低順序排列
    '''
    result = []
    for i in range(times):
        this_value = first_value * (MILV ** i)
        this_value = octave_clamp(this_value, first_value)  # 約束在一個八度內
        result.append(this_value)
    return result

def output_list(list_value, list_name, order_equal = True):
    '''
    輸出結果，匹配音名
    list_value: 使用律學算法計算出的List[float]
    list_name: 音名字符串列表
    order_equal: 是否按音名高低順序排列，否則按五度相生順序排列
    return: 結果字符串
    '''
    result = ''
    if not order_equal: # 使用五度相生順序排列
        list_value = _rearrange_list(list_value, SANFENSUNYI_TO_EQUAL_ORDER, is_forward = False)
        list_name = _rearrange_list(list_name, SANFENSUNYI_TO_EQUAL_ORDER, is_forward = False)
    for i, value in enumerate(list_value):
        if value is None:
            continue
        name = list_name[i % len(list_name)]
        result += f'[{i + 1}]{name}: {value}\n'
    return result

def _rearrange_list(list_raw, order, is_forward = True):
    '''
    按列表下標指定位置分段重新排序，如[a,b,c]以[3,1,2]的規則排序，則變為[b,c,a]
    使用相同的order，可以還原排序前的列表
    list_raw: 原list
    order: 分段排序規則，如果list長度不足一個排序規則的長度，則自動補0
    is_forward: 重新排序為True，還原排序為False
    return: 排序後的新列表
    '''
    result = []
    block_size = len(order)
    blocks = [
        list_raw[i:i+block_size]
        for i in range(0, len(list_raw), block_size)]
    if is_forward:  # 正向處理
        using_order = order
    else:   # 逆向還原
        using_order = [0] * block_size
        for idx, pos in enumerate(order):
            using_order[pos] = idx
    for block in blocks:
        new_block = [0] * block_size
        for idx, pos in enumerate(using_order):
            if idx < len(block):
                new_block[pos] = block[idx]
            else:
                new_block[pos] = None  # 找不到的元素默認填充None
        result.extend(new_block)
    return result

def octave_clamp(this_value, first_value, is_add = False):
    '''
    八度約束，使新的音在首音所在八度之內
    this_value: 當前值
    first_value: 首音數值
    is_add: 八度範圍為[first_value, first_value * 2]，否則為[first_value / 2, first_value]
    return: 約束後的新值
    '''
    if (is_add):
        min_value = first_value
        max_value = first_value * 2
    else:
        min_value = first_value / 2
        max_value = first_value
    
    if this_value < min_value:
        return this_value * 2
    elif this_value > max_value:
        return this_value / 2
    else:
        return this_value

if __name__ == '__main__':
    print('三分損益法')
    list_value = sanfensunyi(HUANGZHONG, 13)
    list_str = output_list(list_value, PITCH_NAME_ZH, order_equal = False)  # 五度相生排列
    print(list_str)

    print('何承天新律')
    list_value = hechengtian_xinlv(HUANGZHONG, 13)
    list_str = output_list(list_value, PITCH_NAME_ZH, order_equal = False)  # 五度相生排列
    print(list_str)

    print('十二平均律')
    list_value = equal_temperament(HUANGZHONG, 13)
    list_str = output_list(list_value, PITCH_NAME_ZH)
    print(list_str)