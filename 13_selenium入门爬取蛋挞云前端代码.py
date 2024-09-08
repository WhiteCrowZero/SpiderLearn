'''
# selenium 的作用：
能不能让我的程序连接到浏览器，让浏览器来完成各种复杂的操作，我们只接受最终的结果
selenium: 自动化测试江具
可以打开浏览器，然后像人一样去操作浏览器
程序员可以从 selenium 中直接提取网页上的各种信息

# 环境搭建：
pip install selenium
下载浏览器 chrome 驱动：https://registry.npmmirror.com/binary.html?path=chromedriver/
把解压缩的浏览器驱动 chromedriver 放在 python 解释器所在的文件夹（注意，这个项目我用的是虚拟环境，所以需要放左我的虚拟环境下的 Python 解释器下）
补充：当然，可以不把 chromedriver 放在 python 解释器所在的文件夹，在调用 webdriver.Chrome() 的时候，可以指定 chromedriver 的路径
例如：
s = Service('/path/to/chromedriver')
driver = webdriver.Chrome(service=s)

# # 测试代码：
from selenium.webdriver import Chrome
# 1. 创建浏览器对象
web = Chrome()
# 2. 打开一个网址
web.get('https://www.baidu.com')
print(web.title)
'''

# 获取蛋挞云的前端网页源代码
# 蛋挞云网站的 html 都是通过 js 动态生成的，所以直接用 requests 获取到的 html 都是空的
# 这里我们就通过 selenium 打开浏览器，然后让浏览器去访问蛋挞云网站，从而获取到蛋挞云网站的 html 源代码
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

save_path = 'result/13_蛋挞云.html'
url = 'https://eggtartcloud.biz/zh/#/subscription'
account_dict = {
    'email': '3633850267@qq.com',
    'password': 'zero1984xyzwzw'
}


chrome_options = Options()
# chrome_options.add_argument("--headless")
s = Service("D:\somesoftware\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chrome_options)

try:
    driver.get(url)
    time.sleep(10)  # 等待页面加载完成

    # 输入登录信息，登录账号
    user_name = driver.find_element(By.XPATH, "/html/body/agl-root/div/agl-auth/div/div/main/agl-auth-login/form/div[2]/agl-text-field[1]/div/input")
    user_name.send_keys(account_dict['email'])
    password = driver.find_element(By.XPATH, "/html/body/agl-root/div/agl-auth/div/div/main/agl-auth-login/form/div[2]/agl-text-field[2]/div[1]/input")
    password.send_keys(account_dict['password'])
    time.sleep(1)
    login_button = driver.find_element(By.XPATH, "/html/body/agl-root/div/agl-auth/div/div/main/agl-auth-login/form/button")
    login_button.click()
    time.sleep(15)

    # 获取整个网页的源代码
    html_source = driver.page_source
    # print(html_source)
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(html_source)
    print('爬取完成')
finally:
    driver.quit()
