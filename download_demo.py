import requests
import os
import time
from requests.adapters import HTTPAdapter

def not_404(url):
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        response = s.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print(i, e)
        return False, ""
    if response.status_code != 404:
        return True, response.text
    else:
        return False, ""

for i in range(64116,65622): #(49255,65622)
    str_i = str(i)
    url = "https://gutenberg.org/cache/epub/{0}/pg{0}.txt".format(str_i)
    flag, content = not_404(url)
    if flag:
        with open("./guten_data/content/pg"+str_i+".txt", "w", encoding='utf-8') as writer:
            writer.write(content)
        print("pg" + str_i + ".txt finished: /xx/pgxx.txt")
        continue
    url = f"https://gutenberg.org/files/{str_i}/{str_i}-0.txt"
    flag, content = not_404(url)
    if flag:
        with open("./guten_data/content/pg"+str_i+".txt", "w", encoding='utf-8') as writer:
            writer.write(content)
        print("pg" + str_i + ".txt finished: /xx/xx-0.txt")
        continue
    url = f"https://gutenberg.org/files/{str_i}/{str_i}.txt"
    flag, content = not_404(url)
    if flag:
        with open("./guten_data/content/pg" + str_i + ".txt", "w", encoding='utf-8') as writer:
            writer.write(content)
        print("pg" + str_i + ".txt finished: /xx/xx.txt")
        continue
    with open("./guten_data/content/error.txt", 'a' ,encoding='utf-8') as f:
        f.write(str_i+"\n")
    print("pg" + str_i + ".txt failed")

    time.sleep(0.3)


# current_path = os.getcwd()  #获取当前路径
# print(current_path)
# for i in range(#1, 387):
#     path = current_path+'\\guten_data\\content\\pg{0}.txt'.format(str(i)) #在当前路径创建名为test的文本文件
#     if os.path.exists(path):
#         pass
#         # print(str(i)+' exist')
#     else:
#         with open("./guten_data/content/error.txt", 'a', encoding='utf-8') as f:
#             f.write(str(i)+"\n")
#         print(str(i))
