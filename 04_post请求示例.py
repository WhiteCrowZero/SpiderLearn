# 百度翻译的 post 请求案例
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}
url = 'https://fanyi.baidu.com/sug'
word = 'hello'

# 构建 data 参数字典，发送的参数必须是 json 格式
data = {
    'kw': word
}

# 通过 data 参数传递 post 请求需要的相应参数
res = requests.post(url, headers=headers, data=data)
print(res.json())
res.close()
