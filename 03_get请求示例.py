"""
注意：地址栏里面的网址，一定都是 GET 方式提交
"""
import requests

# 1.找到目标URL（F12检查获得）
url = 'https://img1.baidu.com/it/u=2390790660,1806672130&fm=253&fmt=auto&app=120&f=JPEG?w=1280&h=800'

# 构建请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

# 2.添加请求头，模拟浏览器，发送请求，获取响应（看清请求方式）
# headers参数用于添加请求头，接收字典形式的请求头
response = requests.get(url, headers=headers)
# print(response.content)

# 3.保存响应内容（注意是二进制形式）
with open('result/03_test.jpg', 'wb') as f:
    f.write(response.content)

# 4.其他属性
print(response.url)                 # 打印 HTTP 响应的 URL
print(response.status_code)         # 打印 HTTP 响应的状态码
print(response.headers)             # 打印 HTTP 响应的头信息
print(response.request.headers)     # 打印 HTTP 请求的头信息
print(response.cookies)             # 打印 HTTP 响应的 Cookies
print(response.history)             # 打印 HTTP 响应的历史记录
print(response.encoding)            # 打印 HTTP 响应的字符编码

response.close()
