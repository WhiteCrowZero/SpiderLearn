# 步骤：
# 1.找到未加密的参数
# 2,想办法把参数进行加密（必须参考网易的逻辑），params, encSecKey(解密后就能得到任意歌曲的评论了)
# 3,请求到网易，拿到评论信息
import json
import random
import requests
import base64
import csv
from Crypto.Cipher import AES

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
    'Referer': 'https://music.163.com/song?id=27203936',
    'User-Agent': random.choice(UAList),
}

url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='

# 基本数据
data = {
    "cursor": -1,
    "offset": 0,
    "orderType": 1,
    "pageNo": 1,
    "pageSize": 20,
    "rid": "R_SO_4_27203936",
    "threadId": "R_SO_4_27203936",
}

# 处理加密过程
'''
# 网页源代码：
var bVi6c = window.asrsea(JSON.stringify(i0x), bse6Y(["流泪", "强"]), bse6Y(Qu1x.md), bse6Y(["爱心", "女孩", "惊恐", "大笑"]));
e0x.data = j0x.cr1x({
    params: bVi6c.encText,
    encSecKey: bVi6c.encSecKey
})

# 所以：
params -> encText
encSecKey -> encSecKey

# 在接着，找到 window.asrsea 加密过程
# 网页源代码
!function() {
    function a(a) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)              # 循环16次
            e = Math.random() * b.length,       # 生成随机值
            e = Math.floor(e),                  # 取整
            c += b.charAt(e);                   # 从上面的字符串取值
        return c                                # 最终生成一个长度为 16 的，含字母和数字的随机字符串
    }
    function b(a, b) {                          # a是要加密的数据
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {    # AES加密算法   c是密钥，所以b是密钥
            iv: d,
            mode: CryptoJS.mode.CBC             # 模式为 CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    ####################################################################
    # d:就是data数据    e:就是bse6Y(["流泪", "强"])，在控制台试验后，发现就是个定值，为‘010001’   f:就是bse6Y(Qu1x.md)，同e，也是个定值
    # g:就是bse6Y(["爱心", "女孩", "惊恐", "大笑"])，同e，也是个定值
    function d(d, e, f, g) {
        var h = {}
          , i = a(16);                  # i 就是一个 16 位的随机值
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),    # 得到的就是params
        h.encSecKey = c(i, e, f),       # 得到的就是encSecKey，e和f是固定的，如果i也是固定的，且c这个函数本身不会产生随机数，那么encSecKey也是固定的
        h
    }
    #####################################################################
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    # 因为是把 d 赋值给 window.asrsea，所以这里 d 是核心，找到上面关于 d 的代码进行分析
    window.asrsea = d,
    window.ecnonasr = e
}();
'''

d = data
e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = '0OuwaPPhMGn5qafz'


def get_encSecKey():
    return "b1065c3775b5a71f7052ec7de6d0409e14532c6dcb2dd2712c9ed799e655d07a2dfd2570c861199bd3d9fb64cb66c72e8db36584a383786c44cb3e30282515ede5422bbdfda86bada0c5a180fb94e48f2d20697f6ecc260886209fcfbb77afcb2c32fd4e679f3f7926ce4c88b0bba3915bd93e89241304d220c87749148ec4a3"


def get_params(data):
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second


def pad_to_16(data):
    pad_num = 16 - (len(data) % 16)
    res = data + chr(pad_num) * pad_num
    return res


# 还原上面 b 的加密过程
def enc_params(data, key):
    # 注意，所有参数加密的时候都是字节的形式，所以要先转成字节再传参
    aes = AES.new(key=key.encode('utf-8'), mode=AES.MODE_CBC, iv='0102030405060708'.encode('utf-8'))
    # 注意，这里有个要求，就是加密的长度必须是16的倍数，所以这里需要补全
    data = pad_to_16(data)
    bs = aes.encrypt(data.encode('utf-8'))
    # 最后要把字节转换成字符串返回
    res = base64.b64encode(bs).decode('utf-8')
    return res


# 这里把字典处理成字符串，方便后面加密处理
data = json.dumps(data)
params = get_params(data)
encSecKey = get_encSecKey()
encrypted_data = {
    'params': params,
    'encSecKey': encSecKey,
}
# print(encrypted_data)

# 请求方式post
resp = requests.post(url, headers=header, data=encrypted_data)
print(resp.text)
resp.close()

hot_comments = resp.json()['data']['hotComments']

path = './result/网易《YMCA》热评.csv'
with open(path, 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['nickname', 'content', 'like', 'time'])
    for comment in hot_comments:
        csv_writer.writerow(
            [comment['user']['nickname'], comment['content'], comment['likedCount'], comment['timeStr']])
