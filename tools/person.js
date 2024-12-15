const ONLY_NOT_EXACT_PARAMS = ['簡述', '記載年備註', '備註'];

// 加载CSV数据为嵌套字典
function load_data_as_dict(csvData) {
    /*
    加載csv多行文本數據為嵌套字典，格式：
    {
        1 : {'慣用名': '周威烈王', '通鑑目録': '10101', ...},
        2 : {'慣用名': '魏文侯', '通鑑目録': '10101', ...},
        ...
    }
    */
    const dicPerson = {};
    let listParams = [];
    let nokeyCount = 1;
    const lines = csvData.split('\n').map(line => line.trim()).filter(line => line);
    
    lines.forEach((row, i) => {
        const rowItems = row.split(',');
        if (i === 0) {
            listParams = rowItems;
        } else {
            let key = parseInt(rowItems[0]);
            if (key === -1) {   // 默認無編號索引
                key = `x${nokeyCount}`;
                nokeyCount++;
            } else if (dicPerson.hasOwnProperty(key)) {  // 重複索引號
                console.warn(`WARNING: key ${key} used more than one time!`);
            }
            dicPerson[key] = {};
            for (let n = 1; n < listParams.length; n++) {
                dicPerson[key][listParams[n]] = rowItems[n];
            }
        }
    });
    return dicPerson;
}

function query(dic_person, input_str) {
    /*
    人物表內的查詢功能
    */
    let query_mode = 0;
    let exact_key = 0;
    let likely = new Set();
    let relative = new Set();
    // 確定查詢模式
    input_str = input_str.trim().replace('：', ":");    // 也支持中文冒號
    if (input_str.startsWith('*')) {   // 模糊匹配
        query_mode = 5;
        let query_str = input_str.slice(1);

        for (let [key, value] of Object.entries(dic_person)) {   // 精確匹配索引號或慣用名
            if (_is_exact(query_str, key, value)) {
                exact_key = key;
                continue;
            }
            // 非精確匹配情況
            for (let [k, v] of Object.entries(value)) {
                if (v.includes(query_str)) {
                    likely.add(key);
                }
            }
        }
    } else if (input_str.startsWith('@')) { // 顯示詳情
        query_mode = 3;
        let query_str = input_str.slice(1);

        for (let [key, value] of Object.entries(dic_person)) {
            if (_is_exact(query_str, key, value)) {
                exact_key = key;
                break;
            }
        }
    } else if (input_str.includes('and')) { // 邏輯篩選
        query_mode = 4;
        let list_input = input_str.split('and');
        let list_query = list_input.map(input => query(dic_person, input)); // 遞歸調用字段篩選
        let non_empty_set = list_query.map(s => s[2]).filter(s => s.size > 0);
        if (non_empty_set.length > 0) {
            likely = new Set([...non_empty_set.reduce((acc, curr) => {
                return [...acc].filter(x => curr.has(x));
            })]);   // 交集
        }
    } else if (input_str.includes('or')) { // 邏輯篩選
        query_mode = 4;
        let list_input = input_str.split('or');
        let list_query = list_input.map(input => query(dic_person, input)); // 遞歸調用字段篩選
        let non_empty_set = list_query.map(s => s[2]).filter(s => s.size > 0);
        if (non_empty_set.length > 0) {
            likely = new Set([...non_empty_set.reduce((acc, curr) => {
                return [...acc, ...curr];
            })]);   // 並集
        }
    } else if (input_str.includes(':')) {  // 字段篩選
        query_mode = 2;
        let [param_name, query_str] = input_str.split(':');

        param_name = param_name.trim();
        if (!(param_name in dic_person[1])) {
            console.log(`【${param_name}】字段名不存在！`);
            return [query_mode, exact_key, likely, relative];
        }
        query_str = query_str.trim();

        for (let [key, value] of Object.entries(dic_person)) {
            let is_exact = true; // 默認精確匹配
            if (ONLY_NOT_EXACT_PARAMS.includes(param_name)) {  // 除部分字段只能模糊匹配
                is_exact = false;
            }
            if (_match(query_str, value[param_name], is_exact)) {
                likely.add(key);
            }
        }
    } else {   // 人物定位
        query_mode = 1;
        let param_name = '';
        let query_str = input_str;

        for (let [key, value] of Object.entries(dic_person)) {
            // 找精確索引號
            if (_is_exact(query_str, key, value)) {
                exact_key = key;
                continue;
            }
            // 找可能索引號
            if (_match(query_str, value['慣用名'], false)) { // 模糊匹配慣用名
                likely.add(key);
                continue;
            }
            if (_match(query_str, value['通鑑名'], true)) { // 精確匹配通鑑名
                likely.add(key);
                continue;
            }
            if (_match(query_str, value['別稱'], true)) { // 精確匹配別稱
                likely.add(key);
                continue;
            }
            // 找相關索引號
            if (_match(query_str, value['簡述'], false)) { // 模糊匹配簡述
                relative.add(key);
                continue;
            }
            if (_match(query_str, value['備註'], false)) { // 模糊匹配備註
                relative.add(key);
                continue;
            }
        }
    }
    return [query_mode, exact_key, likely, relative];
}

function _match(input, check, is_exact = true) {
    /*
    判斷輸入內容是否符合條件
    input: 輸入條件
    check: 待檢查條件，可能為以|分隔的數組
    is_exact: 是否精確匹配字符串
    return: bool
    */
    if (typeof input === 'number') {  // 數值
        if (is_exact) {
            return input === check;
        } else {
            return String(input).includes(String(check));
        }
    } else if (check.includes('|')) {    // 數組
        let list_check = check.split('|');
        if (is_exact) {
            return list_check.includes(input);
        } else {
            return list_check.some(item => item.includes(input));
        }
    } else {   // 單一    
        if (is_exact) {
            return input === check;
        } else {
            return check.includes(input);
        }
    }
}

function _is_exact(queryStr, key, value) {
    /*
    判斷是否精確匹配
    queryStr: 查詢字符串或數值
    key: 數據字典條目的key
    value: 數據字典條目的value
    return: bool
    */
    const isNum = !isNaN(queryStr);
    if (isNum && _match(parseInt(queryStr), parseInt(key), true)) { // 精確匹配索引號
        return true;
    }
    if (!isNum && _match(queryStr, value['慣用名'], true)) { // 精確匹配慣用名
        return true;
    }
    return false;
}

function view_query(dicPerson, queryStr) {
    /*
    query方法的輸出
    */
    let result = '';
    const [queryMode, exactKey, likely, relative] = query(dicPerson, queryStr);
    if (queryMode === 1) { // 人物定位
        if (exactKey !== 0) {
            result += `【${queryStr}】的索引號：${exactKey} 慣用名：${dicPerson[exactKey]['慣用名']}\n`;
        }
        if (likely.length !== 0) {
            result += `【${queryStr}】可能是：\n`;
            for (const item of likely) {
                result += `${item} ${dicPerson[item]['慣用名']}\n`;
            }
        }
        if (relative.length !== 0) {
            result += `【${queryStr}】相關人物：\n`;
            for (const item of relative) {
                result += `${item} ${dicPerson[item]['慣用名']}\n`;
            }
        }
    } else if ([2, 4, 5].includes(queryMode)) { // 字段篩選、邏輯篩選、模糊匹配
        result += `【${queryStr}】的符合的索引：\n`;
        for (const item of likely) {
            result += `${item} ${dicPerson[item]['慣用名']}\n`;
        }
    } else if (queryMode === 3) { // 顯示詳情
        if (exactKey !== 0) {
            result += `【${queryStr}】的索引號：${exactKey}\n`;
            const data = dicPerson[exactKey];
            for (const [key, value] of Object.entries(data)) {
                if (value !== '') {
                    result += `${key}：${value}\n`;
                }
            }
        }
    }
    return result.slice(0, -1) || '未找到數據！';
}

// 执行查询
function person() {
    const inputStr = document.getElementById('searchQuery').value;
    const resultsDiv = document.getElementById('results');
    const data = load_data_as_dict(RAW_DATA);
    const result = view_query(data, inputStr);
    resultsDiv.textContent = result;
}

// 按鈕綁定回車按鍵
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchQuery').addEventListener('keypress', function(event) {
        // 检查按下的是否是回车键
        if (event.key === "Enter") {
            event.preventDefault();
            person();
        }
    });
});