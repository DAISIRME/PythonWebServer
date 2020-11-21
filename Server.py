import threading
from socket import *
import _thread

from threading import Thread
DEFAULT_FILE = '/index.html'
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive.")
local_cache = {}
param = {}
LOG_IN_SUCCESS = 'succ.html'

def get_request_type(file_request):
    if file_request.endswith("html") or file_request.endswith("htm"):
        return "text/html"
    else:
        return "text/plain"


def file_not_found(error_html,error_html_path):
    data, content = get_file_content(error_html, error_html_path)
    print(error_html_path)
    return data, content
    # connectSocket.send("HTTP/1.1 404 NOT FOUND".encode())
    # connectSocket.send("Server: Python HTTP Server from DDH : 1.0".encode())
    # connectSocket.send(b'')
    # connectSocket.send(data.encode())


def get_local_file(file_request):
    # 获得默认路径
    if file_request == '/':
        file_request += DEFAULT_FILE
    # 获得本地文件位置
    root = "D://WebServer"
    filepath = root+file_request
    result = file_request.split('?')
    # i = result[1]
    # for j in i.split('&'):
    #         print(j)
    #         h = j.split('=')
    #         param[h[0]] = h[1]
    #         print(h)
    # print(param)
    # if param['usr']=='1' and param['pwd'] == '2':
        # data, content =get_file_content(LOG_IN_SUCCESS,root+LOG_IN_SUCCESS)
        # file_request = LOG_IN_SUCCESS
        # filepath = root+LOG_IN_SUCCESS
    try:
        # 获取具体内容
        return get_file_content(file_request, filepath)
    except:
        # 页面不存在
        print(1)
        error_html = "/404.html"

        return file_not_found(error_html, root+error_html)


def get_file_content(file_request, filepath):
    # 缓存机制 加快访问速度
    # 若请求文件不在缓存中 访问硬盘资源
    # if file_request not in local_cache:
        File = open(filepath)
        data = File.read(-1)
        content = get_request_type(file_request)
        # print(content)
        # local_cache[file_request] = {}
        # local_cache[file_request]['data'] = data
        # local_cache[file_request]['content'] = content
        return data, content
    # 若在缓存中 直接返回
    # else:
    #     data = local_cache[file_request]['data']
    #     content = local_cache[file_request]['content']
        # print(data,content)
        # print(local_cache)
        return data, content


def handle(modifiedmessage):
    # 分离信息
    request_infor = modifiedmessage.split( )
    # 获得请求方法
    request_method = request_infor[0]
    # 获得请求文件
    request_file = request_infor[1]
    if request_method == 'GET' or request_method == 'POST':
            data, content = get_local_file(request_file)
            print(data)
            connectSocket.send("HTTP/1.1 200 OK".encode())
            connectSocket.send("Server: Python HTTP Server from DDH : 1.0".encode())
            connectSocket.send(("Content type:").encode())
            # print('---------------------------------------------------------------')
            connectSocket.send(b'')
            connectSocket.send(data.encode())
    else:
            connectSocket.send("HTTP/1.1 METHOD NOT SUPPORTED".encode())


if __name__ == "__main__":
    while True:
        connectSocket, addr = serverSocket.accept()
        # print(addr)
        # print(connectSocket)
        modifiedmessage = connectSocket.recv(9999999).decode()
        # print(modifiedmessage)
        if not modifiedmessage:
            continue
        if modifiedmessage.split( )[0] != 'GET':
            continue
        _thread.start_new_thread(handle, (modifiedmessage, ))
        # print("Current Thread is ")