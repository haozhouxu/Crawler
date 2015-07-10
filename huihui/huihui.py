# -*- coding: utf-8 -*-
import urllib2

from bs4 import BeautifulSoup


OriginalUrl = "http://www.huihui.cn";
SearchUrl = "http://www.huihui.cn/all?page="
Keyword = "Casio"
Page = [1,2,3,4,5,6,7,8,9,10]


def PageHtml(url, keyword, page):
	html = urllib2.urlopen(url + str(page))
	soup = BeautifulSoup(html)
	for content in soup.find_all("div", class_="hlist-list-text"):
		string = content.h3.a.get_text().replace("\n", " ")  # 去除回车
		string = string.strip()  # 去除前后空格
		gbkstring = string.encode("gbk","ignore")  #输出的时候出现GBK问题，cmd输出的时候需要把unicode转换为GBK，导致出错
		if Keyword in string:
			print gbkstring


def main():
	print "\nBegin\n"
	for i in Page:
		PageHtml(SearchUrl, Keyword, i)
	print "\nEnd\n"


if __name__ == '__main__':
	main()