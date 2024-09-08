import csv
import time
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 爬取 绿果网 山东枣庄部分的价格信息
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
    # 注意，这个网站的http协议非常严格，是'strict-origin-when-cross-origin'，要检查来路，所以这里请求头要写明来自他的上一级网站
    'Referer': "https://www.lvguo.net/baojia",      # 这个是防盗链，用来溯源
    'User-Agent': random.choice(UAList)
}
count = 0
page = ''

current_date = datetime.now().strftime("%Y年%m月%d日")
path = f'./result/08_绿果网山东农产品价格_{current_date}.csv'
with open(path, 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['时间', '地区', '产品', '价格详情', '商户'])

while True:
    if count > 0:
        page = 't' + str(count // 20 + 1)
    url = "https://www.lvguo.net/baojia/area/4500/" + page
    # print(url)
    main_resp = requests.get(url, headers=header)
    # print(main_resp.status_code)

    # 拿到网页主体的表格部分
    main_page = BeautifulSoup(main_resp.text, 'html.parser')
    main_table = main_page.find('table')
    # print(main_table)
    child_tr_list = main_table.find_all('tr')

    with open(path, 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        for each_tr in child_tr_list[1:]:
            td_list = each_tr.find_all('td')
            # for each_td in td_list:
            #     print(each_td.text)
            priceDate = td_list[0].text
            area = td_list[1].text
            name = td_list[2].text
            data = td_list[3].text.replace('\n', '')
            merchant = td_list[4].text
            csv_writer.writerow([priceDate, area, name, data, merchant])
            count += 1

    print(f'第{count // 20}页爬取完成')
    time.sleep(1)
    if count >= 100:
        break

print('爬取完成')
main_resp.close()
