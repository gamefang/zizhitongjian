# brython腳本
from browser import aio,document,html,alert # type: ignore
# 導入分析工具
import era_name

# 導入數據
csv_str = ''
async def import_data():
    req = await aio.get('../../1_數據表/1.3_各類通表/年號總表.csv')
    global csv_str
    csv_str = req.data
aio.run(import_data())

# UI
document <= html.A('返回首頁', href='../../index.html')
document <= html.HR()
document <= html.H2('年號查詢工具')
document <= '查詢' + html.A('年號總表', href='../../1_數據表/1.3_各類通表/年號總表.html') + '中的年號相關信息。' \
    + html.BR() + '輸入空值可查看說明。'
document <= html.BR() + html.BR()
document <= html.INPUT(id='txt_input', type='text', placeholder='輸入查詢指令')
document <= html.BUTTON('查詢', id='btn_run')
document <= html.BR() + html.BR()
document <= html.H3(html.PRE('', id='txt_result'))

# 鍵盤事件
def on_txt_input_press_key(ev):
    if ev.key == 'Enter':
        ev.preventDefault()
        on_btn_run_click(ev)
txt_input = document['txt_input']
txt_input.bind('keypress', on_txt_input_press_key)
# 按鈕點擊事件
def on_btn_run_click(ev):
    if csv_str == '':
        alert('數據正在加載中，請稍候……')
    else:
        result = era_name.main(csv_str, document['txt_input'].value)
        document['txt_result'].text = result
btn_run = document['btn_run']
btn_run.bind('click', on_btn_run_click)