import re

# 1. match
"""
match 从开头开始匹配，只返回一个匹配结果；如果开头不一致，返回None
"""
string_example = "hello, my name is hello"
pattern_example = "hello"
match_result = re.match(pattern_example, string_example)
print(match_result)
print(match_result.group())         # hello
string_example = "1hello, my name is hello"
match_result = re.match(pattern_example, string_example)
print(match_result)                 # None

# 2. search
"""
search 从任意位置开始匹配，只返回一个匹配结果；如果找不到匹配结果，返回None
"""
string_example = "hello, my name is hello"
pattern_example = "hello"
search_result = re.search(pattern_example, string_example)
print(search_result.group())

# 3. findall
"""
findall 找到字符串中所有的匹配结果，返回一个列表
"""
string_example = "hello, my name is hello"
pattern_example = "hello"
findall_result = re.findall(pattern_example, string_example)
print(findall_result)

# 4. finditer
"""
finditer 找到字符串中所有的匹配结果，返回一个迭代器，比前一个方法更省内存，效率更高
"""
string_example = "hello, my name is hello"
pattern_example = "hello"
finditer_result = re.finditer(pattern_example, string_example)
for item in finditer_result:
    print(item.group())

# 5. 预加载正则表达式
"""
re.compile 预加载正则表达式，这样表达式可以重复使用，并且提前加载好，效率更高
补充： re.compile(pattern, flag)，re.S是一个flag，表示 * 可以匹配任意字符，包括换行符
"""
string_example = r"hello, my name is hello"
pattern_example = r"hello"
obj = re.compile(pattern_example)
findall_result = obj.findall(string_example)
print(findall_result)
findall_result = obj.finditer(string_example)
for item in findall_result:
    print(item.group())

# 6. (?P<name>pattern) 可以单独从正则匹配的内容中提取到相关的部分
"""
非捕获组在正则表达式中使用 (?: ... ) 的语法来表示，它与捕获组 ( ... ) 类似，但不会在匹配中创建一个捕获组
捕获组的内容可以通过 group(name) 方法来获取，非捕获组的匹配结果无法通过 group(name) 方法来获取
"""
string_example = r"""
    <div class='123'>
        呵呵呵
    </div>
    <span>这是一行</span>
    <div>
        嘿嘿嘿
    </div>
"""
pattern_example = r"<div(?: class='.*?')?>\s*(?P<content>.*?)\s*</div>"
obj = re.compile(pattern_example)
finditer_result = obj.finditer(string_example)
for item in finditer_result:
    print(item.group("content"))
