import requests

url = 'https://movie.douban.com/j/chart/top_list'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

params = {
    "type": 24,
    'interval_id': '100:90',
    'action': '',
    'start': 0,
    'limit': 100
}

res = requests.get(url=url, headers=header, params=params)
# print(res.json())

path = './result/05_豆瓣喜剧电影数据100条.json'
with open(path, 'w', encoding='utf-8') as f:
    f.write(res.text)
print('爬取数据写入成功')
res.close()
