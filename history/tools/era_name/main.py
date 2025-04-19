# 年號總表查詢網頁邏輯
from pyodide.http import pyfetch # type: ignore
import asyncio

def main():
    # 全局變量
    class glo:
        csv_text = ''
    # 加載csv
    async def load_csv():
        csv_path = '/1_數據表/1.3_各類通表/年號總表.csv'
        response = await pyfetch(csv_path)
        glo.csv_text = await response.text()
    asyncio.ensure_future(load_csv())
    # 緩存ui對象
    txt_result = get_by_id('txt_result')
    txt_input = get_by_id('txt_input')
    btn_run = get_by_id('btn_run')
    # 綁定按鈕
    def on_click(event):
        if glo.csv_text == '':
            result = '數據尚未加載完成，請稍候'
        else:
            dic_era = load_data_as_dict(glo.csv_text)
            result = view_query(dic_era, txt_input.value)
        txt_result.innerHTML = result
    bind_click_event(btn_run, on_click)
    # 綁定回車
    def on_keypress(event):
        if event.key == 'Enter':
            on_click(event)
    bind_event(txt_input, 'keypress', on_keypress)
main()

if __name__ == "__main__":
    # 假import，僅用於編譯器顯示懸停提示
    try:
        from history.utils.scripts.pyodidex import *
        from era_name import *
    except:
        pass