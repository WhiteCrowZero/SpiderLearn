import requests
# 豆瓣的这个是“客户端渲染”，这个只是爬取数据，不爬取网页代码
# 同时，前面的urlopen库比较低级，为了爬取网页，需要使用requests库，并且需要加上 请求头headers 的伪装

url = 'https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start=0&limit=20'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    file_path = 'result/02_douban_movie.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print('爬取完成')
else:
    print(f'HTTP Error: {response.status_code}')
response.close()
