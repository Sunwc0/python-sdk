"""使用urllib请求socks5代理服务器
请求http和https网页均适用
"""

import urllib.request
from urllib.parse import urlencode
import socks
import zlib
import json
import random
from sockshandler import SocksiPyHandler

# 要访问的目标网页
page_url = "https://dev.kdlapi.com/testproxy"

# API接口, 返回格式为json
api_url = "https://kps.kdlapi.com/api/getkps/?orderid=967449798518947&num=2&pt=2&format=json&sep=1"
# 用户名和密码(私密代理/独享代理)
username = "treezeng"
password = "nrfrqd5o"


# API接口返回的ip
response = urllib.request.urlopen(api_url)
json_dict = json.loads(response.read().decode('utf-8'))
ip_list = json_dict['data']['proxy_list']

# 随机选用一个代理ip
proxy_ip, proxy_port = random.choice(ip_list).split(":")
proxy_port = int(proxy_port)  # 端口是int，不能是str

rdns = False  # 是否在代理服务器上进行dns查询

opener = urllib.request.build_opener(SocksiPyHandler(socks.SOCKS5, proxy_ip, proxy_port, rdns, username, password))
opener.addheaders = [
    ("Accept-Encoding", "Gzip"),  # 使用gzip压缩传输数据让访问更快
]
r = opener.open(page_url)
# 发送post请求
# data = bytes(urlencode({"info": "send post request"}), encoding="utf-8")
# r = opener.open("http://dev.kdlapi.com/testproxy", data=data)
print(r.code)  # 获取Reponse的返回码
content = r.read()

content_encoding = r.headers.get_all("Content-Encoding") if r.headers.get_all("Content-Encoding") else []
if content_encoding and "gzip" in content_encoding:
    print(zlib.decompress(content, 16 + zlib.MAX_WBITS).decode('utf8'))  # 有gzip压缩时获取页面内容
else:
    print(content.decode('utf-8'))  # 无gzip压缩时获取页面内容
