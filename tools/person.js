const ONLY_NOT_EXACT_PARAMS = ['簡述', '記載年備註', '備註'];

// 加载CSV数据为嵌套字典
function load_data_as_dict(rawData) {
    const lines = rawData.split('\n');
    const headers = lines[0].split(',');
    const data = {};
    let nokeyCount = 1; // 移动到函数外部声明
    lines.slice(1).forEach((line, index) => {
        const row = line.split(',');
        let key = parseInt(row[0], 10);
        if (isNaN(key) || key === -1) { // 默认无编号索引
            key = `x${nokeyCount}`;
            nokeyCount += 1;
        } else if (data.hasOwnProperty(key)) { // 重复索引号
            console.warn(`WARNING: key ${key} used more than one time!`);
        }
        data[key] = headers.reduce((obj, header, n) => {
            obj[header] = row[n + 1] || ''; // 跳过第一个元素（索引）
            return obj;
        }, {});
    });
    return data;
}

// 检查慣用名是否有重复
function check_name(dicPerson) {
    const listNames = [];
    const wrongKeys = [];
    Object.keys(dicPerson).forEach(key => {
        const name = dicPerson[key]["慣用名"];
        if (listNames.includes(name)) { // 重复出现
            const usedIndex = listNames.indexOf(name);
            const usedKey = Object.keys(dicPerson)[usedIndex];
            if (!wrongKeys.includes(usedKey)) {
                wrongKeys.push(usedKey);
            }
            wrongKeys.push(key);
        } else {
            listNames.push(name); // 添加所有，确保下标对齐
        }
    });
    return wrongKeys;
}

// 查询功能
function query(dicPerson, inputStr) {
    let queryMode = 0;
    let exactKey = 0;
    let likely = new Set();
    let relative = new Set();
    // 确定查询模式
    inputStr = inputStr.trim().replace('：', ':'); // 也支持中文冒号
    const [paramName, queryStr] = inputStr.includes(':') ? inputStr.split(':').map(s => s.trim()) : ['', inputStr];
    
    if (paramName) {
        if (!(paramName in dicPerson[Object.keys(dicPerson)[0]])) {
            console.log(`【${paramName}】字段名不存在！`);
            return {queryMode, exactKey, likely, relative};
        }
    }
    
    // 姓名查询模式
    if (paramName === '') {
        queryMode = 1;
        Object.keys(dicPerson).forEach((key) => {
            const value = dicPerson[key];
            // 找精确索引号
            if (_match(queryStr, value['慣用名'], true)) { // 精确匹配慣用名
                exactKey = key;
            }
            // 找可能索引号
            if (_match(queryStr, value['慣用名'], false) && exactKey !== key) { // 模糊匹配慣用名
                likely.add(key);
            }
            if (_match(queryStr, value['通鑑名'], true) && exactKey !== key) { // 精确匹配通鑑名
                likely.add(key);
            }
            if (_match(queryStr, value['別稱'], true) && exactKey !== key) { // 精确匹配別稱
                likely.add(key);
            }
            // 找相关索引号
            if (_match(queryStr, value['簡述'], false)) { // 模糊匹配簡述
                relative.add(key);
            }
            if (_match(queryStr, value['備註'], false)) { // 模糊匹配備註
                relative.add(key);
            }
        });
    } else { // 字段查询模式
        queryMode = 2;
        Object.keys(dicPerson).forEach((key) => {
            const isExact = ONLY_NOT_EXACT_PARAMS.indexOf(paramName) === -1; // 默认精确匹配
            if (_match(queryStr, dicPerson[key][paramName], isExact)) {
                likely.add(key);
            }
        });
    }
    return {queryMode, exactKey, likely, relative};
}

// 判断输入内容是否符合条件
function _match(input, check, isExact = true) {
    if (check.includes('|')) { // 数组
        const listCheck = check.split('|');
        if (isExact) {
            return listCheck.includes(input);
        } else {
            return listCheck.some(item => input.includes(item));
        }
    } else { // 单一    
        if (isExact) {
            return input === check;
        } else {
            return input.includes(check);
        }
    }
}

function view_query(dicPerson, queryStr) {
    let result = '';
    const { queryMode, exactKey, likely, relative } = query(dicPerson, queryStr);
    if (queryMode === 1) {
        if (exactKey !== 0) {
            result += `【${queryStr}】的索引號：${exactKey}\n`;
        }
        if (likely.size !== 0) {
            result += `【${queryStr}】可能是：\n`;
            likely.forEach(key => {
                result += `${key} ${dicPerson[key]["慣用名"]}\n`;
            });
        }
        if (relative.size !== 0) {
            result += `【${queryStr}】相關人物：\n`;
            relative.forEach(key => {
                result += `${key} ${dicPerson[key]["慣用名"]}\n`;
            });
        }
    } else if (queryMode === 2) {
        result += `【${queryStr}】的符合的索引：\n`;
        likely.forEach(key => {
            result += `${key} ${dicPerson[key]["慣用名"]}\n`;
        });
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