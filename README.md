# crawler

## 数据格式

详见./data/gutenberg0-4999.txt. 

格式为（相邻之间只有\t， 一本书一行）

书本详情页的url	\t author(s)（可能带生辰，是否要去除）\t	title  \t	publish_year	\t description（第二个网址无description，我默认'No description'）\t	content_url(书本内容下载链接，格式不定，优先级如下text, pdf, epub no pic, epub with pic, kindle no pic, kindle with pic, txt ASCII, HTML, RDF，剩余的稀有格式如只有音频下载链接已在./data/gutenberg_attention.txt中声明， 不同格式下载方式不同)

