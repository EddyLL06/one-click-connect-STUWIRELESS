import requests

url = "http://sjauth.ykpaoschool.cn/ajaxlogout?"

response = requests.get(url)

print(response.text)