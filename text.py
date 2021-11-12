import requests

url = 'https://blog.csdn.net/huangpin815/article/details/70194492'

response = requests.get(url).text
print (response)
print ('hello')