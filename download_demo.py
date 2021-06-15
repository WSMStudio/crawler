import requests
import os

for i in range(388,66000):
    str_i = str(i)
    url = "https://gutenberg.org/cache/epub/{0}/pg{0}.txt".format(str_i)
    response = requests.get(url)
    if response.status_code != 404: #int
        with open("./guten_data/content/pg"+str_i+".txt", "w", encoding='utf-8') as writer:
            writer.write(response.text)
        print("pg" + str_i + ".txt finished")
    else:
        with open("./guten_data/content/error.txt",'a',encoding='utf-8') as f:
            f.write(str_i+"\n")


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
