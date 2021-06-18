import requests, time
from database_class import *
from parsel import Selector
import re
import copy

def download_from_bid():
    with open(f"./smash_data/content/not_crawled.txt", "r", encoding="utf-8") as f1:
        not_crawled_ = f1.read().split('\t')[:-1]
    not_crawled = [int(i) for i in not_crawled_]
    crawled = []
    updated_not_crawled = copy.deepcopy(not_crawled)
    # print(not_crawled)
    for i in not_crawled:
        url = "https://www.smashwords.com/books/view/{bid}"
        res = requests.get(url.format(bid=i))
        selector = Selector(res.text)
        download_txt_links = [link for link in selector.css("#samples a").xpath("@href").getall()
                              if link.endswith(".txt")] + \
                             [link for link in selector.css("#download a").xpath("@href").getall()
                              if link.endswith(".txt")]
        content = requests.get("https://www.smashwords.com" + download_txt_links[-1]).text
        if content[0:9] == "<!DOCTYPE":
            print(f"{i} is failed")
            break
        else:
            with open(f"./smash_data/content/pa{i + 70000}.txt", "w", encoding="utf-8") as f1:
                f1.write(content)
            print(f"{i} is success")
            crawled.append(i)
            updated_not_crawled.remove(i)

    print(f"All crawled is :{crawled}")
    with open(f"./smash_data/content/not_crawled.txt", "w", encoding="utf-8") as f1:
        f1.write("")
    for j in updated_not_crawled:
        with open(f"./smash_data/content/not_crawled.txt", "a", encoding="utf-8") as f1:
            f1.write(f"{j}\t")

def download_from_url():
    with open(f"./smash_data/content/not_crawled_url.txt", "r", encoding="utf-8") as f1:
        not_crawled_ = f1.read().split('\n')[:-1]
    not_crawled_bid = [int(i.split('\t')[0]) for i in not_crawled_]
    not_crawled_url = [i.split('\t')[1] for i in not_crawled_]
    crawled_index = []
    for i in range(len(not_crawled_bid)):
        bid = not_crawled_url[i]
        content = requests.get(bid).text
        if content[0:9] == "<!DOCTYPE":
            print(f"index {i} bid {bid} is failed")
            break
        else:
            with open(f"./smash_data/content/pa{bid + 70000}.txt", "w", encoding="utf-8") as f1:
                f1.write(content)
            print(f"index {i} bid {bid} is success")
            crawled_index.append(i)
    crawled_bid = [not_crawled_bid[i] for i in crawled_index]
    print(f"All crawled bid is :{crawled_bid}, total number is {len(crawled_bid)}")
    if not crawled_bid:
        return
    with open(f"./smash_data/content/not_crawled_url_1.txt", "w", encoding="utf-8") as f1:
        f1.write("")
    for j in range(len(not_crawled_bid)):
        if j not in crawled_index:
            with open(f"./smash_data/content/not_crawled_url_1.txt", "a", encoding="utf-8") as f1:
                f1.write(f"{not_crawled_bid[j]}\t{not_crawled_url[j]}\n")


download_from_url()
# download_from_bid()
