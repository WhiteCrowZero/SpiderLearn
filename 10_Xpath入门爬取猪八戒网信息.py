import requests
import random
from lxml import etree
import csv

'''
Xpath使用后个人感觉：
特别容易写错，还有信息提取不出来，也不能及时查看
感觉不如 re ，更不如 bs4 方便直观
'''

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
header = {
    'Referer': 'https://www.zbj.com',
    'User-Agent': random.choice(UAList),
}

kw = 'python'
url = f'https://www.zbj.com/fw/?k={kw}'
resp = requests.get(url, headers=header)
# print(resp.text)

html = etree.HTML(resp.text)
divs = html.xpath('/html/body/div[1]/div/div/div[3]/div/div[4]/div/div[2]/div/div[2]/div')
# print(divs)

with open('result/10_Xpath入门爬取猪八戒网信息.csv', 'a', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['business_name', 'price', 'sales'])
    for div in divs:
        sales = div.xpath('./div/div[5]/div/div/div/text()')[0]
        price = div.xpath('./div/div[3]/div[1]/span/text()')[0].strip('¥')
        business_name = kw.join(div.xpath('./div/div[3]/div[2]/a/span/text()')).replace('*', '')
        if business_name == '':
            business_name = f'提供{kw}相关服务'
        csv_writer.writerow([business_name, price, sales])

        # 不知道为什么，下面的变量Xpath路径正确，但是获取不到相应的数据
        # local = div.xpath('./div/div[4]/div[2]/span[2]/text()')
        # sales_volume = div.xpath('./div/div[3]/div[3]/div[1]/div[1]/span[2]/text()')
        # favorable_comment = div.xpath('./div/div[3]/div[3]/div[2]/div[1]/span[2]/text()')

print('爬取完成')
resp.close()
