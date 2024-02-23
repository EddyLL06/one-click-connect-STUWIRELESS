# -*- coding: utf-8 -*-
# @Time    : 2022/1/13 22:01
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : login_network.py
# @Software: PyCharm

# Modified by Eddy on 2023/9/10
# To fit the need of using MacOS
# Email: eddyll06@outlook.com

import requests
import keyring
import time
import json
import os

# 检查用户的家目录下是否有.wifi_login文件夹，如果没有则创建
secret_dir = os.path.join(os.path.expanduser("~"), ".wifi_login")
if not os.path.exists(secret_dir):
    os.makedirs(secret_dir)

# 设置username.json文件的路径，存储在.wifi_login文件夹中
file_name = os.path.join(secret_dir, "username.json")

# 检查username.json文件是否存在
if not os.path.exists(file_name):
    print("请注意，如果你输错了账号密码，目前版本下修改较为麻烦，请尽量一次输对。")
    print("你的密码会被安全的保存在苹果系统自带的Keychain Access内。")
    username = input("请输入您的账号: ")
    password = input("请输入您的密码: ")
    # 将账号密码存入keychain
    keyring.set_password("wifi_login", username, password)
    res = {
        'username': username,
    }
    print(res)
    # 将账号保存到username.json文件中
    with open(file_name, "w+") as fp:
        fp.write(json.dumps(res))
else:
    # 从username.json文件中读取账号
    with open(file_name, "r")as fp:
        res = json.loads(fp.read())
        username = res['username']
        password = keyring.get_password("wifi_login", username)

# RC4加密函数


def do_encrypt_rc4(src: str, passwd: str) -> str:
    i, j, a, b, c = 0, 0, 0, 0, 0
    key, sbox = [], []
    plen = len(passwd)
    size = len(src)
    output = ""

    # 初始化密钥和sbox
    for i in range(256):
        key.append(ord(passwd[i % plen]))
        sbox.append(i)
    for i in range(256):
        j = (j + sbox[i] + key[i]) % 256
        temp = sbox[i]
        sbox[i] = sbox[j]
        sbox[j] = temp
    for i in range(size):
        a = (a + 1) % 256
        b = (b + sbox[a]) % 256
        temp = sbox[a]
        sbox[a] = sbox[b]
        sbox[b] = temp
        c = (sbox[a] + sbox[b]) % 256
        temp = ord(src[i]) ^ sbox[c]
        temp = str(hex(temp))[-2:]
        temp = temp.replace('x', '0')
        output += temp
    return output


# 登录的URL
url = "http://10.2.20.106/ac_portal/login.php"
# 请求头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Length": "102",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "sjauth.ykpaoschool.cn",
    "Origin": "http://sjauth.ykpaoschool.cn",
    "Referer": "http://sjauth.ykpaoschool.cn/ac_portal/default/pc.html?tabs=pwd",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
    "X-Requested-With": "XMLHttpRequest"
}
# 获取时间戳
tag = int(time.time()*1000)
# 使用RC4加密密码
pwd = do_encrypt_rc4(password, str(tag))
# 创建payload
payload = f"opr=pwdLogin&userName={username}&pwd={pwd}&auth_tag={tag}&rememberPwd=1"

while True:
    try:
        # 提交登录请求
        res = requests.post(url, data=payload, headers=headers)
        # 检查登录是否成功
        if res.status_code == 200 and res.text.find("true") > 0:
            print(f"\033[7;32;47m{res.content.decode('utf-8')} \033[0m")
        else:
            print(f"\033[7;31;47m{res.content.decode('utf-8')} \033[0m")
            print("\033[7;31;47m", "登录失败！请确保输入正确的账号信息！", "\033[0m")
            os.remove(file_name)
            print("\033[7;36;47m", "已清除账号文件。\n 重新启动并重新输入。", "\033[0m")
        input("按任意键退出...")
        break
    except Exception as err:
        print("\033[7;31;47m", "登录错误！\t可能需要先连接wifi?", "\033[0m")
        print("\033[7;33;40m", err, "\033[0m")
        decision = input("按 'R' 重新开始，或按其他键退出...")
        if decision.lower() != 'r':
            break
