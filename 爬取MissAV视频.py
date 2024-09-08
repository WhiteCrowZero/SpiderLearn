import os
import re
import time
import random
import asyncio
import aiohttp
import aiofiles
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
1. 通过网络请求，获得主网页源代码，找到其中的 m3u8 链接
2. 通过网络请求，获得 m3u8 链接源代码，找到其中的 ts 链接
# 注：这里的 MissAV 网站的第一个 m3u8 里面嵌套了多个 m3u8 链接，需要再访问其中的链接进行解析，获得ts链接
3. 下载 ts 链接的文件，保存到本地
4. 合并 ts 文件为一个 mp4 文件
"""

r'''
# 网页源代码
p:  'e=\'8://7.6/5-4-3-2-1/d.0\';c=\'8://7.6/5-4-3-2-1/a/9.0\';b=\'8://7.6/5-4-3-2-1/a/9.0\';',
a:  15,
c:  15,
k:  'm3u8|7921d18d64c4|977e|48d1|20d6|fc90cf5e|com|surrit|https|video|842x480|source1280|source842|playlist|source'.split('|'),
e:  0,
d:  {}
eval(function(p,a,c,k,e,d){
    // 定义一个函数 e，用于将数字转换为 36 进制字符串
    e=function(c){return c.toString(36)};           # 15 -> 36位字符串                           
    // 如果 ''.replace(/^/,String) 不成立，则执行以下逻辑
    if(!''.replace(/^/,String)){                    # 一定执行，这个匹配的结果一定是空字符串
        // 循环处理替换数组 k 和 d
        while(c--){
            d[c.toString(a)]=k[c]||c.toString(a)    # || 就是 or
        }
        // 重新定义 k 数组，只包含一个返回 d[e] 的函数
        k=[function(e){return d[e]}];               # function(e){...}: 数组中的元素是一个匿名函数，该函数接受一个参数e。
                                                    # return d[e]: 函数返回对象d中键为e的值。
        // 重新定义 e 函数，返回匹配单词字符的正则表达式
        e=function(){return'\\w+'};                 
        // 重新定义 c 为 1
        c=1
    }
    // 再次循环处理替换字符串 p                        #  c 就是1，所以就执行一次，循环体内部c就是0了
    while(c--){
        // 如果存在 k[c]，则通过正则表达式替换 p 中的 e(c)
        if(k[c]){
            p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])
        }
    }
    // 返回处理后的字符串 p
    return p
}

'''

"""
# 详细解释的版本
def handle_m3u8_url(p, a, c, k, d):
    # 定义一个lambda函数，用于将数字转换为36进制字符串
    e = lambda num: format(num, '36')

    # 循环处理字典d，其中a是格式化字符串，c是循环次数
    for i in range(c, 0, -1):
        # 将循环变量i格式化为字符串a，并作为键存储在字典d中
        # 如果k中有i对应的值，则使用该值，否则使用格式化后的字符串
        d[format(i, a)] = k.get(i, format(i, a))

    # 重新定义k为一个列表，其中包含一个lambda函数
    # 这个lambda函数接受一个key参数，并从字典d中返回对应的值
    k = [lambda key: d[key]]

    # 重新定义e为一个lambda函数，返回匹配单词字符的正则表达式字符串
    e = lambda: r'\w+'

    # 将c重置为1，用于后续的循环
    c = 1

    # 再次循环，这次用于处理字符串p
    for i in range(c, 0, -1):
        # 如果k列表中的函数存在（这里始终存在，因为已经重新定义过k），则执行替换操作
        if k[0]:
            # 创建一个正则表达式对象，用于匹配字符串p中的单词字符
            regex = e()
            # 使用re.sub函数替换p中的所有匹配项，替换为k[0]函数返回的值
            p = re.sub(regex, k[0], p)
    return p
"""

UAList = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/84.0.4316.125",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/50.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36"
]
header = {
    'Referer': 'https://missav.com/dm12/en',
    'User-Agent': random.choice(UAList)
}
root_path = 'result/1111/'

def get_current_time():
    # 获取当前时间戳
    current_time = time.time()
    # 将时间戳转换为本地时间
    local_time = time.localtime(current_time)
    # 格式化时间字符串，例如："2024-08-05 12:34:56"
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return time_str

# 精简版（所有 m3u8 字符串的处理以这个函数的操作为准）
# 其实也不用那么麻烦，最简单粗暴的一种方法就是直接把 d 里面的元素组合起来就是链接，组合顺序还是固定的
# 这里主要练习了 js 的逆向
# 不过这个也有个好处，就是直接获得所有的 m3u8 链接，不用再去找第二层了
def handle_m3u8_url(p, a, c, k, e, d):
    for i in range(c - 1, -1, -1):
        d[int(format(i, a))] = k[i or int(format(i, a))]
        # print(i,k[i])
    # print(d)

    def replace_url(key):
        num = key.group(0)
        if num not in d.keys():
            num = int(num, 16)
        return d[num]

    new_p = re.sub(r"\w+", lambda key: replace_url(key), p)
    return new_p


# 注意，这个网站的 html 是经过 js 处理过的，所以直接用正则表达式是找不到 m3u8 链接的
# 所以这里要使用 selenium 模拟浏览器来请求到含有 m3u8 字符串的 html
def get_first_m3u8_url(url):
    chrome_options = Options()
    # 可以添加更多的选项，例如无头模式（无界面模式）
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(5)  # 等待页面加载完成
        # 获取整个网页的源代码
        html_source = driver.page_source
    finally:
        driver.quit()
    # 测试用
    # html = "eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('e=\'8://7.6/5-4-3-2-1/d.0\';c=\'8://7.6/5-4-3-2-1/a/9.0\';b=\'8://7.6/5-4-3-2-1/a/9.0\';',15,15,'m3u8|7921d18d64c4|977e|48d1|20d6|fc90cf5e|com|surrit|https|video|842x480|source1280|source842|playlist|source'.split('|'),0,{}))"

    pattern = r"return p}(?P<m3u8_str>.*?)0,{}"
    match = re.search(pattern, html_source)
    m3u8_str = match.group('m3u8_str')
    list = m3u8_str.strip('(').split(',')
    # print(list)

    p = list[0]
    a = list[1]
    c = int(list[2])
    k = list[3].split(r'.s')[0].strip("'").split('|')
    e = 0
    d = {}

    first_m3u8_url_list = handle_m3u8_url(p, a, c, k, e, d).split(";")
    first_m3u8_url = first_m3u8_url_list[0].split("'")[2].strip('\\')
    return first_m3u8_url


def get_second_m3u8_url(first_url):
    with open(root_path + 'playlist.m3u8', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        second_m3u8_url_list = []
        for line in lines:
            if line.startswith('#'):
                continue
            second_m3u8_url = first_url.split("playlist.m3u8")[0] + line.strip()
            second_m3u8_url_list.append(second_m3u8_url)

    return (second_m3u8_url_list)


# 下载所需要的 m3u8 文件
def download_m3u8_file(url, title):
    # Ensure the directory exists
    directory = os.path.join(root_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = root_path + title
    with open(file_path, 'wb') as f:
        with requests.get(url, headers=header) as response:
            f.write(response.content)



# 单独下载每一个 ts 文件
async def download_ts(m3u8_url_up, ts_title, session):
    ts_dir = os.path.join(root_path, 'ts')
    os.makedirs(ts_dir, exist_ok=True)
    ts_file_path = os.path.join(ts_dir, ts_title)
    url = m3u8_url_up + ts_title

    try:
        async with session.get(url) as response:
            response.raise_for_status()
            async with aiofiles.open(ts_file_path, 'wb') as f:
                await f.write(await response.read())
                print(f"{ts_title} 下载完成")
    except aiohttp.ClientError as e:
        print(f"下载 {ts_title} 失败: {e}")
    except Exception as e:
        print(f"写入 {ts_title} 失败: {e}")


def merge_ts(m3u8_title):
    # 读取需要合并的文件的列表（一定要注意文件顺序，合并文件的顺序不能乱，所以这里不采用直接读取文件夹文件的形式）
    ts_list = []
    with open(os.path.join(root_path, m3u8_title), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            ts_title = line.strip()
            ts_list.append(os.path.join(root_path, 'ts', ts_title))

    # print(ts_list)
    output_file = os.path.join(root_path, '爬取MissAV视频.mp4')
    # 这里使用二进制写入的方式直接合并成 mp4 文件，没有平台限制和软件限制
    with open(output_file, 'wb') as outfile:
        for file_name in ts_list:
            with open(file_name, 'rb') as infile:
                outfile.write(infile.read())


async def main(url):
    first_url = get_first_m3u8_url(url)
    now_time = get_current_time()
    print(now_time + ": 获取到第一层m3u8链接: " + first_url)

    title = first_url.split('/')[-1]
    download_m3u8_file(first_url, title)
    second_m3u8_url_list = get_second_m3u8_url(first_url)
    now_time = get_current_time()
    print(now_time + ": 获取到第二层m3u8链接列表")

    for idx, second_m3u8_url in enumerate(second_m3u8_url_list):
        print(str(idx) + ':' + second_m3u8_url)
    input_idx = int(input('请输入要下载的视频文件序号：'))
    second_url = second_m3u8_url_list[input_idx]

    m3u8_url_up = second_url.split("video.m3u8")[0]
    title = second_url.split('/')[-1]
    download_m3u8_file(second_url, title)

    async with aiohttp.ClientSession(headers={'User-Agent': random.choice(UAList)}) as session:
        tasks = []
        with open(root_path + title, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('#'):
                    continue
                ts_title = line.strip()
                task = asyncio.create_task(download_ts(m3u8_url_up, ts_title, session))
                tasks.append(task)

            await asyncio.gather(*tasks)

    merge_ts(title)
    now_time = get_current_time()
    print(now_time + ": 视频合并完成")


if __name__ == '__main__':
    url = 'https://missav.com/dm13/en/avgp-109'
    asyncio.run(main(url))
    print('爬取完成')
