# 人物總表查詢網頁邏輯
from pyodide.http import pyfetch # type: ignore
import asyncio

def main():
    # 全局變量（新增 dic_person 快取解析後的字典，提升即時查詢性能）
    class glo:
        csv_text = ''
        dic_person = {}

    # 緩存ui對象
    txt_result = get_by_id('txt_result')
    txt_input = get_by_id('txt_input')
    btn_run = get_by_id('btn_run')

    # 生成 HTML 查詢結果
    def render_html(query_str):
        if glo.csv_text == '':
            return '數據尚未加載完成，請稍候……'
        
        # 第一次查詢時解析 CSV
        if not glo.dic_person:
            glo.dic_person = load_data_as_dict(glo.csv_text)

        query_str = query_str.strip()
        
        # 空值顯示說明文檔
        if query_str == "":
            doc_text = view_query(glo.dic_person, "")
            doc_esc = str(doc_text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f'<pre class="doc-text">{doc_esc}</pre>'

        # 調用 person.py 原有的 query 方法
        query_mode, exact_key, likely, relative = query(glo.dic_person, query_str)
        html_parts = []

        # 輔助生成帶跳轉按鈕的單行 HTML
        def make_item(key, name):
            k_esc = str(key).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            n_esc = str(name).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f'<div class="result-item"><span>{k_esc} {n_esc}</span><button class="btn-detail" data-key="{k_esc}">詳情</button></div>'

        if query_mode == 1:  # 人物定位
            if exact_key != 0:
                html_parts.append(f'<div class="result-title">【{query_str}】精確匹配：</div>')
                html_parts.append(make_item(exact_key, glo.dic_person[exact_key]["慣用名"]))
            if len(likely) != 0:
                html_parts.append(f'<div class="result-title">【{query_str}】可能是 ({len(likely)})：</div>')
                for item in likely:
                    html_parts.append(make_item(item, glo.dic_person[item]["慣用名"]))
            if len(relative) != 0:
                html_parts.append(f'<div class="result-title">【{query_str}】相關人物 ({len(relative)})：</div>')
                for item in relative:
                    html_parts.append(make_item(item, glo.dic_person[item]["慣用名"]))

        elif query_mode in (2, 4, 5):  # 字段篩選、邏輯篩選、模糊匹配
            if len(likely) != 0:
                html_parts.append(f'<div class="result-title">【{query_str}】符合的索引 ({len(likely)})：</div>')
                for item in likely:
                    html_parts.append(make_item(item, glo.dic_person[item]["慣用名"]))

        elif query_mode == 3:  # 顯示詳情
            if exact_key != 0:
                data = glo.dic_person[exact_key]
                k_esc = str(exact_key).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_parts.append(f'<div class="result-title">【{query_str}】的索引號：{k_esc}</div>')
                html_parts.append('<table class="detail-table"><tbody>')
                for k, v in data.items():
                    if v != '':
                        k_s = str(k).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        v_s = str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        html_parts.append(f'<tr><th>{k_s}</th><td>{v_s}</td></tr>')
                html_parts.append('</tbody></table>')

        if not html_parts:
            return f'<div class="no-data">【{query_str}】未找到數據！</div>'

        return ''.join(html_parts)

    # 觸發查詢更新 UI
    def do_search(event=None):
        txt_result.innerHTML = render_html(txt_input.value)

    # 點擊結果區域內的「詳情」按鈕觸發精確查詢
    def on_result_click(event):
        target = event.target
        if target and hasattr(target, 'getAttribute'):
            key = target.getAttribute('data-key')
            if key:
                txt_input.value = f'@{key}'
                do_search()

    # 加載 CSV
    async def load_csv():
        csv_path = '/1_數據表/1.3_各類通表/人物總表.csv'
        response = await pyfetch(csv_path)
        glo.csv_text = await response.text()
        do_search()  # 加載完成後顯示初始畫面/說明文檔
    asyncio.ensure_future(load_csv())

    # 綁定按鈕點擊、鍵盤輸入 (即時查詢) 與結果點擊代理
    bind_click_event(btn_run, do_search)
    bind_event(txt_input, 'input', do_search)
    bind_event(txt_result, 'click', on_result_click)

main()

if __name__ == "__main__":
    # 假import，僅用於編譯器顯示懸停提示
    try:
        from history.utils.scripts.pyodidex import *
        from person import *
    except:
        pass