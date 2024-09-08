import os
import time
import random
import requests
from bs4 import BeautifulSoup

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
header = {'User-Agent': random.choice(UAList)}

root_path = f'./result/09_img/'
page = ''

# 想要爬取其他的图片，更改成其他图片的缩率图主页即可
main_url = "https://www.umeituku.com/tags/zhoudongyu.htm"
main_resp = requests.get(main_url, headers=header)
main_resp.encoding = 'utf-8'
# print(main_resp.status_code)

# 获取主页面中子页面的链接
main_page = BeautifulSoup(main_resp.text, 'html.parser')
a_list = main_page.find('div', class_='TypeList').find_all('a', class_='TypeBigPics')

for a in a_list:
    count = 1
    href = a.get('href')
    # print(href)

    # 获取子页面中开始页面的链接
    header = {'User-Agent': random.choice(UAList)}
    child_resp = requests.get(href, headers=header)
    child_resp.encoding = 'utf-8'
    child_page = BeautifulSoup(child_resp.text, 'html.parser')
    folder_name = child_page.find('div', class_='ArticleTitle').find('strong').get_text()
    save_path = root_path + folder_name
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    while True:
        # 根据开始页，获得每一页图片的链接
        if count > 1:
            child_url = '.'.join(href.split('.')[:-1]) + '_' + str(count) + '.htm'
            header = {'Referer': href, 'User-Agent': random.choice(UAList)}
            child_resp = requests.get(child_url, headers=header)
            child_resp.encoding = 'utf-8'
            child_page = BeautifulSoup(child_resp.text, 'html.parser')

        # 当访问的文件不存在时，就退出不再爬取
        if child_page.find_all('meta')[1].get('http-equiv') is not None:
            break

        img_src = child_page.find('div', class_='ImageBody').find('img').get('src')
        if img_src == '':
            print('图片链接为空')
            continue
        header = {'User-Agent': random.choice(UAList)}
        img_resp = requests.get(img_src, headers=header)

        # 保存图片
        with open(save_path + '/' + str(count) + '.jpg', 'wb') as f:
            f.write(img_resp.content)
        count += 1
        time.sleep(1)
        if count > 5:
            break

    child_resp.close()
    print('已爬取 ' + folder_name)
    time.sleep(1)

print('爬取完成')
main_resp.close()
