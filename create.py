import history.utils.csvtotable.convert as csvtotable   # csvtotable已內置
import os

CSV_FILES = [
r'1_數據表/1.1_通鑑目録/時代表.csv',
r'1_數據表/1.1_通鑑目録/卷目表.csv',
r'1_數據表/1.1_通鑑目録/章節表.csv',

r'1_數據表/1.2_政權年代表/戰國秦.csv',
r'1_數據表/1.2_政權年代表/漢.csv',
r'1_數據表/1.2_政權年代表/魏晉南北朝.csv',

r'1_數據表/1.3_各類通表/人物總表.csv',
r'1_數據表/1.3_各類通表/年號總表.csv',
]

def convert_one(input_file):
    '''
    使用csvtotable轉化一個csv文件
    '''
    output_file = input_file.replace('.csv', '.html')
    caption = os.path.basename(input_file).replace('.csv', '')
    kwargs = {
        "caption": caption, # 標題名
        "overwrite": True,
        "export": True,
        "delimiter": ",",
        "quotechar": '"',
        "display_length": 100,  # 每頁行數
        "serve": False,
        "height": None,
        "pagination": True,
        "virtual_scroll": -1,   # -1為關閉
        "no_header": False,
        "export_options": ['copy']  # 搜索旁邊的按鈕
    }
    html_content = csvtotable.convert(input_file, **kwargs)
    csvtotable.save(output_file, html_content)
    print(f'Converted: {output_file}')

if __name__ == "__main__":
    for fp in CSV_FILES:
        convert_one(fp)