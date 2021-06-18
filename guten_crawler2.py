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
        print("\033[33;1m", e, url, "\033[0m")
        return False, url
    if response.status_code != 404:
        return True, response.text
    else:
        return False, ""

def supplemental_crawler(str_i):
    # url1 = "https://gutenberg.org/cache/epub/{0}/pg{0}.txt".format(str_i)
    # flag1, content1 = not_404(url1)
    # if flag1:
    #     with open("./guten_data/content/pg"+str_i+".txt", "w", encoding='utf-8') as writer:
    #         writer.write(content1)
    #     print("pg" + str_i + ".txt finished: /xx/pgxx.txt")
    #     return
    url2 = f"https://gutenberg.org/files/{str_i}/{str_i}-0.txt"
    flag2, content2 = not_404(url2)
    if flag2:
        with open("./guten_data/content/pg"+str_i+".txt", "w", encoding='utf-8') as writer:
            writer.write(content2)
        print("pg" + str_i + ".txt finished: /xx/xx-0.txt")
        return
    url3 = f"https://gutenberg.org/files/{str_i}/{str_i}.txt"
    flag3, content3 = not_404(url3)
    if flag3:
        with open("./guten_data/content/pg" + str_i + ".txt", "w", encoding='utf-8') as writer:
            writer.write(content3)
        print("pg" + str_i + ".txt finished: /xx/xx.txt")
        return
    with open("./guten_data/content/failed.txt", 'a' ,encoding='utf-8') as f:
        f.write(str_i+"\n")
    print("pg" + str_i + ".txt failed")


if __name__ == '__main__':
    with open("./guten_data/content/error.txt", 'r', encoding="utf-8") as f:
        bids = f.read().split('\n')[:-1]
    for bid in bids:
        supplemental_crawler(bid)
        # time.sleep(0.3)
