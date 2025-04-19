// js僅負責初始化pyodide及python腳本加載
async function main() {
    const txt_result = document.getElementById("txt_result");
    // 初始化 Pyodide
    txt_result.innerHTML = "正在初始化……";
    let pyodide = await loadPyodide({
        indexURL: "../../utils/pyodide/",
    });
    // 實際的import
    pyodide.runPythonAsync( await (await fetch("../../utils/scripts/pyodidex.py")).text() );
    pyodide.runPythonAsync( await (await fetch("person.py")).text() );
    pyodide.runPythonAsync( await (await fetch("main.py")).text() );
    txt_result.innerHTML = "初始化完成";
}
main();