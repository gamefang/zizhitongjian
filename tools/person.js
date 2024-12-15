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

// 检查慣用名是否有重复
function checkName(dicPerson) {
    /*
    檢查慣用名是否有重複，返回可能有問題的所有相關索引編號
    */
    let listNames = [];
    let wrongKeys = [];
    let dicPersonKeys = Object.keys(dicPerson);
    
    for (let key in dicPerson) {
        let name = dicPerson[key]["慣用名"];
        if (listNames.includes(name)) {  // 重複出現
            let usedIndex = listNames.indexOf(name);
            let usedKey = dicPersonKeys[usedIndex];
            if (!wrongKeys.includes(usedKey)) {
                wrongKeys.push(usedKey);
            }
            wrongKeys.push(key);
        }
        listNames.push(name); // 添加所有，確保下標對齊
    }
    return wrongKeys;
}

// 查询功能
function query(dic_person, input_str) {
    /*
    人物表內的查詢功能
    XXX -> 姓名查詢模式1：僅針對姓名進行查詢，返回：(1, 精確索引號, 可能的索引號列表, 相關的索引號列表)
    字段名：XXX -> 字段查詢模式2：找到固定字段符合表達式的內容，返回：(2, 0, 索引號列表, None)
    */
    let query_mode = 0;
    let exact_key = 0;
    let likely = new Set();
    let relative = new Set();
    
    // 確定查詢模式
    input_str = input_str.trim().replace('：', ":"); // 也支持中文冒號
    let param_name = '';
    let query_str = input_str;
    
    if (input_str.includes(':')) {
        [param_name, query_str] = input_str.split(':').map(s => s.trim());
        if (!(param_name in dic_person[1])) {
            console.log(`【${param_name}】字段名不存在！`);
            return [query_mode, exact_key, Array.from(likely), Array.from(relative)];
        }
        query_str = query_str.trim();
    }
    
    // 姓名查詢模式
    if (param_name === '') {
        query_mode = 1;
        for (const [key, value] of Object.entries(dic_person)) {
            // 找精確索引號
            if (_match(query_str, value['慣用名'], true)) { // 精確匹配慣用名
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
    // 字段查詢模式
    else {
        query_mode = 2;
        for (const [key, value] of Object.entries(dic_person)) {
            let is_exact = true; // 默認精確匹配
            if (ONLY_NOT_EXACT_PARAMS.includes(param_name)) { // 除部分字段只能模糊匹配
                is_exact = false;
            }
            if (_match(query_str, value[param_name], is_exact)) {
                likely.add(key);
            }
        }
    }
    return [query_mode, exact_key, Array.from(likely), Array.from(relative)];
}

// 判断输入内容是否符合条件
function _match(input, check, isExact = true) {
    /*
    判斷輸入內容是否符合條件
    input: 輸入條件
    check: 待檢查條件，可能為以|分隔的數組
    isExact: 是否精確匹配字符串
    return: bool
    */
    if (check.includes('|')) { // 數組
        const listCheck = check.split('|');
        if (isExact) {
            return listCheck.includes(input);
        } else {
            for (const item of listCheck) {
                if (item.includes(input)) {
                    return true;
                }
            }
            return false;
        }
    } else { // 單一    
        if (isExact) {
            return input === check;
        } else {
            return check.includes(input);
        }
    }
}

function view_query(dicPerson, queryStr) {
    /*
    query方法的輸出
    */
    let result = '';
    const [queryMode, exactKey, likely, relative] = query(dicPerson, queryStr);
    if (queryMode === 1) {
        if (exactKey !== 0) {
            result += `【${queryStr}】的索引號：${exactKey}\n`;
        }
        if (likely.length !== 0) {
            result += `【${queryStr}】可能是：\n`;
            for (const item of likely) {
                result += `${item} ${dicPerson[item]["慣用名"]}\n`;
            }
        }
        if (relative.length !== 0) {
            result += `【${queryStr}】相關人物：\n`;
            for (const item of relative) {
                result += `${item} ${dicPerson[item]["慣用名"]}\n`;
            }
        }
    } else if (queryMode === 2) {
        result += `【${queryStr}】的符合的索引：\n`;
        for (const item of likely) {
            result += `${item} ${dicPerson[item]["慣用名"]}\n`;
        }
    }
    return result.slice(0, -1);
}

// 执行查询
function person() {
    const inputStr = document.getElementById('searchQuery').value;
    const resultsDiv = document.getElementById('results');
    const data = load_data_as_dict(RAW_DATA);
    const result = view_query(data, inputStr);
    resultsDiv.textContent = result || '未找到任何數據！';
}