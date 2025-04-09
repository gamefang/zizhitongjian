import http.server
import socketserver
import webbrowser
import threading

PORT = 8262  # 端口號

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    '''自定义MIME类型处理器'''
    def guess_type(self, path):
        # 修复WASM和特殊JS文件的MIME类型
        if path.endswith(".asm.js"):
            return "application/javascript"
        if path.endswith(".wasm"):
            return "application/wasm"
        if path.endswith(".js"):
            return "application/javascript"
        return super().guess_type(path)

def run_server():
    '''在子线程中运行服务器'''
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"\n服务器已启动，访问地址：http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    # 启动服务器线程
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # 用默认浏览器打开页面
    webbrowser.open(f"http://localhost:{PORT}")

    # 保持主线程存活（按Ctrl+C退出）
    try:
        while True: pass
    except KeyboardInterrupt:
        print("\n服务器已关闭")