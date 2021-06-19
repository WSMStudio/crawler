import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def get_init(base_url, current_page=""):
    # ua = UserAgent()
    # headers = {"User - Agent": ua.ff} 会报错，就不用了
    # 下面这个header是自己的浏览器header，可以从http://httpbin.org/headers看得到
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(base_url, headers = header) # headers=headers
    # print(response)
    page_tag = "pagination"
    tbody_tag = "tbody"
    result = BeautifulSoup(response.text, "lxml")
    tables = result.findAll("table")
    tab = tables[0]
    for tr in tab.tbody.findAll("tr"):
        for index, td in enumerate(tr.findAll("td")):
            if index == 0:
                ip = td.find("a").text
                continue
            if index == 1:
                port = td.getText()
                continue
            if index == 4:
                support_https = td.getText()
                continue
            if index == 5:
                support_post = td.getText()
                continue
            if index == 7:
                speed = td.getText().replace("秒", "")
                continue
        init_data.append([ip, port, support_https, support_post, speed])
    pages = result.find_all("ul", class_=page_tag)
    for index, i in enumerate(pages[0].find_all("li")):
        if index == 0:
            continue
        page_url_postfix = i.find("a")["href"]
        if current_page != page_url_postfix and page_url_postfix not in page_data:
            page_data.append(page_url_postfix)
            print(f"new added page_url_postfix is {page_url_postfix}")
    # print(f"page_data is {page_data}")

def get_current_ip(proxies={}):
    check_url = "http://www.ip111.cn/"
    if proxies:
        requests.get(check_url, timeout=5, proxies=proxies)
    else:
        requests.get(check_url, timeout=5)


def check_content_and_ip(init_data):
    for i in init_data:
        if i[3] == "支持":
            print(i[0], i[1])
            if i[2] == "支持": # 优先看该代理是否支持https
                w = "https://{0}:{1}".format(i[0], i[1])
                proxies = {"https": w}
            else:
                w = "http://{0}:{1}".format(i[0], i[1])
                proxies = {"http": w}

            OrigionalIP = get_current_ip()
            print("\033[31;1mOrigionalIP\033;0m", OrigionalIP)
            try:
                MaskedIP = get_current_ip(proxies)# 是这么用代理的！
                print("\033[31;1mMaskedIP\033;0m", MaskedIP)
                if OrigionalIP != MaskedIP:
                    ip_pool.writelines(w + "\n")
                    ip_pool.flush()
            except:
                continue

if __name__ == "__main__":
    # 获取全国的url 地址
    init_url = "https://ip.ihuan.me/address/5Lit5Zu9.html"
    init_data = []
    page_data = []
    get_init(init_url)

    num = 5   # 循环获取 5 次,数字可修改
    for _k in range(1, num):
        print("searching page ",_k, page_data[_k], "for IP and port")
        url = init_url + page_data[_k]
        try:
            get_init(url, current_page=page_data[_k])
        except Exception as e:
            print(str(e))

        # page_data = list(set(page_data))
        if _k > num:
            break
        time.sleep(1)
    # 至此为止得到许多IP 及 port， 都记录在了init_data中. 里面每一个元素都是[ip, port, support_https, support_post, speed]格式
    # 接下来目的是根据小幻代理网站上的自述，设置proxy
    ip_pool = open("ip_pool.txt", "w")
    check_content_and_ip(init_data)
    ip_pool.close()