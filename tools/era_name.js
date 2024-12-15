// 数字对应汉字
const NUM_IN_HAN = '十一二三四五六七八九';
const NUM_UNIQUE = {1: '元', 10: '十', 11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五', 16: '十六', 17: '十七', 18: '十八', 19: '十九'};

// 加载CSV数据为嵌套字典
function load_data_as_dict(csvContent) {
    const lines = csvContent.split('\n');
    const headers = lines[0].split(',');
    const data = [];
    lines.slice(1).forEach(line => {
        const row = {};
        const columns = line.split(',');
        headers.forEach((header, index) => {
            row[header] = columns[index] || ''; // 确保空值转为字符串
        });
        data.push(row);
    });
    return data;
}

// 年号表内的查询及输出
function query(data, inputStr) {
    let result = '';
    const queryYear = parseInt(inputStr.trim());
    data.forEach(row => {
        const beginYear = parseInt(row['起始年']);
        const endYear = parseInt(row['結束年']);
        if (queryYear >= beginYear && queryYear <= endYear) {
            const delta = yearDelta(beginYear, queryYear);
            const eraNum = delta + 1; // 纪年时间为差值加一年
            let eraHan = NUM_UNIQUE[eraNum];
            if (!eraHan) {
                eraHan = Array.from(String(eraNum), digit => NUM_IN_HAN[digit]).join('');
            }
            result += `【${row['政權']}】${row['領袖']}-${row['年號名稱']}${eraHan}年\n`;
        }
    });
    return result.slice(0, -1);
}

// 求两个年代的年份差值，主要用于适配公元切换情况
function yearDelta(inputYear, compYear) {
    if (inputYear * compYear > 0) {
        return compYear - inputYear;
    } else {
        return compYear - inputYear - 1;
    }
}

// 执行查询
function era_name() {
    const inputStr = document.getElementById('searchQuery').value;
    const resultsDiv = document.getElementById('results');
    const data = load_data_as_dict(RAW_DATA);
    const result = query(data, inputStr);
    resultsDiv.textContent = result || '未找到任何數據！';
}

// 按鈕綁定回車按鍵
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchQuery').addEventListener('keypress', function(event) {
        // 检查按下的是否是回车键
        if (event.key === "Enter") {
            event.preventDefault();
            era_name();
        }
    });
});