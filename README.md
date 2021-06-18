# crawler

## 数据格式

详见./data/gutenberg0-4999.txt. 

格式为（相邻之间只有\t， 一本书一行）

书本详情页的url	\t author(s)（可能带生辰，是否要去除）\t	title  \t	publish_year	\t description（第二个网址无description，我默认'No description'）\t	content_url(书本内容下载链接，格式不定，优先级如下text, pdf, epub no pic, epub with pic, kindle no pic, kindle with pic, txt ASCII, HTML, RDF，剩余的稀有格式如只有音频下载链接已在./data/gutenberg_attention.txt中声明， 不同格式下载方式不同)

### 注意点

1. author 如果有多个，有部分会用'# '分离，剩下的部分是网页上就放在了一起，不太好分，因此未处理。
2. author处偶尔会有生卒年份(格式：1950-1942)，或者生年至今(格式：1950-)

## 目前进展

爬了第二个网址的7000本书的基本信息，content未爬取。基本信息存储在./data/gutenberg0-4999.txt以及 同目录下gutenberg5000-9999.txt。

## 遇到困难

### content爬取有两种方式，

1. 模拟用户使用右键另存为，在弹窗中选择保存位置。需要额外插件，还未学会。
2. 已爬取content的url，如果是pdf格式或者txt格式，用浏览器打开url会在该浏览器中打开新标签页，上面的内容经过掐头去尾地剪辑可以得到完整content。

第一种方法与第二种相比，缺点是需要重新爬取网页，反爬机制就得再来一遍，第二个书本网址是每天5000个。优点是（即法二缺点是）需要内存较大，时间也比较久，还有一个大问题是大书本需要加载，目前不确定是滚轮滚到下面再重新去原网页下载加载，还是已经全部下载到本地内存中，滚轮滚到下面时浏览器进一步加载，如果是前者判断加载完成还未学会。

### 第一个网址更复杂

1. 存有cookie，比如是否包含涩情书本，比如是图片显示还是行显示。如果是访问页面.../0, ..../1, .../2，cookie会消失，
2. 点击书本会出弹窗，弹窗内有下载链接，但详情页面需要在弹窗内再点击书名才可跳转。弹窗怎么识别爬取的问题尚未解决。
3. 虽然可以用一种简单粗暴的方法用序号遍历所有书.../0, ..../1, .../2 （如果用简单粗暴的方法，不会有2中的问题）， 但根据总书本和免费书本的比例约7比1，以及每天限爬，所以最好还是在free大类内爬取。
4. 就算是free大类，里面也有不少是付费的，需要进一步筛选。
5. 可以用IP代理池，还未学会

# 学习到的点，经验

1. 把事作对很重要，更重要的是做对的事，**多做自顶向下规划**而不是埋头猛码代码。 多做代码重用，多写函数。

2. 非动态网页用基础的**requests**即可，不用**selenium**， 两者的xpath语法类似，可借鉴，requests额外还有selector.ccs()， selenium额外还有find_element或elements_by_id或link_text, xpath等等很方便。

3. 可使用数据库 sqlite3，配合sql语言。

4. * selenium 可以设置默认下载地址，对于那些弹窗类型的下载链接可以直接下载，但对于在当前页面打开的不行。 
   * selenium可以设置无头模式，不弹出浏览器，如果不设置，会有浏览器弹出，方便看到程序自动化过程中的各种操作很好用。

5. * 如果是代码改进后，想对已经有数据的文档如txt进行附加操作， 最好是另开一个新文档，完全调试测试后再到原文档。
   * 如果要更新txt，比如txt里存的是还没有爬的url，然后一轮爬完后更新剩余没爬的url，最好还是另起文档，除非能确保代码没问题。**当然还有一种办法是多用git，控制版本**!

6.  调试时，文件读写的可以用print来代替，先用print，调试完成再用文件读写。

   ```python
   text = str(bid) + "\thttps://www.smashwords.com" + download_txt_links[-1] + "\n"
   print(text)
   with open("./smash_data/content/1test_not_crawled_url.txt", "a", encoding="utf-8") as f:
       f.write(text)
   ```

7. 下载text时，有多种可能的网址格式，有/{}/pg{}.txt或/{}/{}-0.txt或/{}/{}.txt，及时发现。

8. 多线程 test_multithread_smash.py  smash_crawler3_multithread.py中都有，多线程其实对于python不麻烦，**文件读写也已测试**, with open 貌似自带文件锁，不会不同线程同时写一个txt。

9. 多IP地址，已经下载了一个repo，

