async function main() {
    // 初始化 Pyodide
    let pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/",
    });
    const btn_run = document.getElementById("btn_run");
    const txt_input = document.getElementById("txt_input");
    // 點擊按鈕
    btn_run.addEventListener("click", async () => {
        try {
            // 获取用户输入
            const input_str = txt_input.value;
            // 加载 CSV 文件
            const obj_csv = await fetch("../../1_數據表/1.3_各類通表/人物總表.csv");
            const csv_str = await obj_csv.text();
            // 加载 Python 文件
            const py_response = await fetch("../py/person.py");
            const py_str = await py_response.text();
            // 运行 Python 代码
            await pyodide.runPythonAsync(py_str);
            // 调用 Python 函数
            const mainjs = pyodide.globals.get("mainjs");
            const result = mainjs(csv_str, input_str);
            // 将结果输出到页面
            document.getElementById("txt_result").innerHTML = result;
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("txt_result").innerHTML = "An error occurred. Please check the console.";
        }
    });
    // 輸入框回車
    txt_input.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            btn_run.click();
        }
    });
}
// 启动 Pyodide 运行时
main();