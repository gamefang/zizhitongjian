# pyodide封裝的一些工具
from js import document # type: ignore
from pyodide.ffi import create_proxy # type: ignore
import asyncio

def get_by_id(id):
    '''
    根據html中的id獲取對象
    '''
    return document.getElementById(id)

def create_text(
    text : str,
    text_id : str = None,
    is_append : bool = True,
) -> object:
    '''
    創建文本
    '''
    div = document.createElement('div')
    div.innerHTML = text
    if text_id:
        div.id = text_id
    if is_append:
        document.body.appendChild(div)
    else:
        document.body.prepend(div)

def create_button(text: str, parent_id: str = "body", button_id: str = None) -> dict:
    """
    极简按钮创建方法

    :param text: 按钮显示文本
    :param parent_id: 父容器ID (默认body)
    :param button_id: 按钮自定义ID
    :return: 包含元素的字典 {'element': button, 'remove': cleanup_func}
    """
    parent = document.body if parent_id == 'body' else document.getElementById(parent_id)
    if not parent:
        raise ValueError(f"Parent container #{parent_id} not found")

    btn = document.createElement("button")
    btn.innerHTML = text
    if button_id:
        btn.id = button_id
        
    parent.appendChild(btn)
    return {"element": btn, "remove": lambda: btn.remove()}

def bind_event(element, event_type: str, callback, async_callback: bool = False) -> callable:
    """
    通用事件绑定方法

    :param element: DOM元素
    :param event_type: 事件类型（如 'click'）
    :param callback: 回调函数
    :param async_callback: 是否异步执行
    :return: 清理函数（解除绑定）
    """
    def handler_wrapper(event):
        try:
            if async_callback:
                future = asyncio.ensure_future(callback(event))
                future.add_done_callback(lambda f: f.exception() and None)
            else:
                callback(event)
        except Exception as e:
            print(f"Event error: {str(e)}")

    proxy = create_proxy(handler_wrapper)
    element.addEventListener(event_type, proxy)
    
    def cleanup():
        element.removeEventListener(event_type, proxy)
        proxy.destroy()
    
    return cleanup

def bind_click_event(element, callback, async_callback: bool = False) -> callable:
    '''
    綁定點擊事件

    :param element: DOM元素
    :param callback: 回调函数
    :param async_callback: 是否异步执行
    :return: 清理函数（解除绑定）
    '''
    return bind_event(element, 'click', callback, async_callback)