# Written by Eddy Liu-Lin on 2023/9/10
# For logging out of STUWIRELESS
# Email: eddyll06@outlook.com

import requests

url1 = "http://sjauth.ykpaoschool.cn/ajaxlogout?"
url2 = "http://10.2.20.106/homepage/logout"

response = requests.get(url1)
response = requests.get(url2)

print(response.text)