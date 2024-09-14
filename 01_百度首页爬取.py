# 使用Python自带的库urllib进行最简单的爬取测试
from urllib.request import urlopen

url = f'http://www.baidu.com'
res = urlopen(url)        # 对要爬取的网址进行请求

# 打印一下，查看爬取到的结果
# print(res.read().decode('utf-8'))

# 打开文件并把爬取到的结果存储到本地
file_path = './result/01_baidu.html'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(res.read().decode('utf-8'))
print('爬取完成')
res.close()
