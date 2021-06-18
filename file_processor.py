import copy
import requests
from parsel import Selector

def not_crawled2not_crawled_url():
    with open(f"./smash_data/content/not_crawled.txt", "r", encoding="utf-8") as f1:
        not_crawled_ = f1.read().split('\t')[:-1]
    not_crawled = [int(i) for i in not_crawled_]
    countdown = len(not_crawled)
    not_crawled_url = []
    # print(not_crawled)
    for i in not_crawled:
        if i >= 1904:
            print(i)
            break
        url = "https://www.smashwords.com/books/view/{bid}"
        res = requests.get(url.format(bid=i))
        selector = Selector(res.text)
        download_txt_links = [link for link in selector.css("#samples a").xpath("@href").getall()
                              if link.endswith(".txt")] + \
                             [link for link in selector.css("#download a").xpath("@href").getall()
                              if link.endswith(".txt")]
        not_crawled_url.append("https://www.smashwords.com" + download_txt_links[-1])
        countdown -= 1
        print(f"{i} is finished. still has {countdown}")

    # print(not_crawled_url)
    with open(f"./smash_data/content/not_crawled_url.txt", "w", encoding="utf-8") as f1:
        for i, url in enumerate(not_crawled_url):
            f1.write(f"{not_crawled[i]}\t{url}\n")

def complete_epub_links():
    with open("./smash_data/smash_epub.txt", "r", encoding="utf-8") as f:
        all = f.read().split('\n')[:-1]
    updated_all = []
    countdown = len(all)
    for i, line in enumerate(all):
        updated_all.append(line.split('\t')[0]+"\thttps://www.smashwords.com"+line.split('\t')[1]+"\n")
        countdown -= 1
        print(f"{i} finished, still {countdown}")
    with open("./smash_data/smash_epub_1.txt", "w", encoding="utf-8") as f:
        f.write("".join(updated_all))

def get_wrong_epub_bid():
    with open("./smash_data/content/not_crawled_url.txt", "r", encoding="utf-8") as f:
        lines = f.read().split('\n')[:-1]
    start_index = 0
    for index, line in enumerate(lines):
        if line.startswith("10281"):
            print(index, line)
            start_index = index
            break
    if start_index == 0:
        print(f"start index is {start_index}, wrong")
        return
    result = []
    for i in range(start_index, len(lines)):
        result.append(int(lines[i].split('\t')[0]))
    if not result:
        print("emtpy")
        return
    else:
        for i in result:
            url = "https://www.smashwords.com/books/view/{bid}"
            res = requests.get(url.format(bid=i))
            if res.status_code == 404:
                print(i, "No Book")
                continue
            selector = Selector(res.text)
            download_txt_links = [link for link in selector.css("#samples a").xpath("@href").getall()
                                  if link.endswith(".txt")] + \
                                 [link for link in selector.css("#download a").xpath("@href").getall()
                                  if link.endswith(".txt")]
            if download_txt_links:
                # print(download_txt_links)
                print(str(i) + "\033[32;1mhas txt\033[0m")
                text = str(i) + "\thttps://www.smashwords.com" + download_txt_links[-1] + "\n"
                with open("./smash_data/content/not_crawled_url_1.txt", "a", encoding="utf-8") as f:
                    f.write(text)
            else:
                print(str(i), "wrong here")

def crawl_smash_overwrite():
    url = "https://www.smashwords.com/books/view/{bid}"
    for bid in range(0, 50):
        res = requests.get(url.format(bid=bid))
        if res.status_code == 404:
            print(bid, "No Book")
            continue
        selector = Selector(res.text)
        download_txt_links = [link for link in selector.css("#samples a").xpath("@href").getall()
                              if link.endswith(".txt")] + \
                             [link for link in selector.css("#download a").xpath("@href").getall()
                              if link.endswith(".txt")]

        if not download_txt_links:
            print(f"{bid} don't have txt, next bid")
            continue
        else:
            # print(download_txt_links)
            print(str(bid) + "\033[32;1mhas txt\033[0m")
            text = str(bid) + "\thttps://www.smashwords.com" + download_txt_links[-1] + "\n"
            with open("./smash_data/content/not_crawled_url.txt", "a", encoding="utf-8") as f:
                f.write(text)  # 如果只有epub没有TXT,记录到./smash_data/smash_epub_1.txt

def count_data_number():
    with open("./smash_data/smash_basic_info.txt", "r", encoding="utf-8") as f:
        print(len(f.read().split("\n")[:-1]))

# not_crawled2not_crawled_url()
# complete_epub_links()
# get_wrong_epub_bid()
# crawl_smash_overwrite()
# count_data_number()
