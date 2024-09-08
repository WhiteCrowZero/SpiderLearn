import re
import csv
import random
import requests

# 准备网址、请求头和相关参数
url = 'https://movie.douban.com/top250'
UAList = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/84.0.4316.125",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/50.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36"
]
params = {
    'start': 0,
    'filter': ''
}

# 预加载正则表达式
pattern = (
    r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)</span>.*?<div class="bd">.*?<br>(?P<year>.*?)&nbsp;'
    r'.*?<div class="star">.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>'
    r'.*?<p class="quote">.*?<span class="inq">(?P<quote>.*?)</span>.*?</li>')
obj = re.compile(pattern, re.S)

# 写如文件标题
path = './result/07_豆瓣电影排行榜top250.csv'
with open(path, 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['电影名称', '电影年份', '电影评分', '电影引用'])

# 开始爬取
while True:
    # 获取网页源代码（包含数据），并提取
    headers = {
        'User-Agent': random.choice(UAList)
    }
    response = requests.get(url, headers=headers, params=params)
    content = response.text
    results = obj.finditer(content)
    # for result in results:
    #     print(result.group('name'))
    #     print(result.group('year').strip())
    #     print(result.group('score'))
    #     print(result.group('quote'))

    # 写入文件，保存数据
    with open(path, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        for result in results:
            dic = result.groupdict()
            dic['year'] = dic['year'].strip()
            csv_writer.writerow(dic.values())

    # 爬取满250条后自动退出并关闭请求
    if params['start'] < 250:
        print('已爬取第%d页' % (params['start'] // 25 + 1))
        params['start'] += 25
    else:
        response.close()
        print('爬取完成')
        break

