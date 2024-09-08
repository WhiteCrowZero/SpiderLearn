from urllib.request import urlopen

url = f'http://www.baidu.com'
res = urlopen(url)

# print(res.read().decode('utf-8'))

file_path = './result/01_baidu.html'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(res.read().decode('utf-8'))
print('爬取完成')
res.close()
