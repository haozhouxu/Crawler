# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
from datetime import date

# 当没有添加http://的时候，会报错，python - ValueError: unknown url type
OrignalUrl = "http://www.pnjyj.gov.cn/"
url = "http://www.pnjyj.gov.cn/wap.php?action=list&id=23&totalresult=47&pageno="
NoticeUrl = "http://www.pnjyj.gov.cn/plus/list.php?tid=23"
page = 1
today = "("+date.today().isoformat()[-5:]+")"

def mapping(url,page):
	UrlString = url + str(page)
	html = urllib2.urlopen(UrlString)
	if 200 == html.getcode():
		soup = BeautifulSoup(html)
		content = soup.find_all("li")
		if [] != content:
			for x in content:
				if x.span.contents[0] == today:
					print BeautifulSoup(urllib2.urlopen(OrignalUrl+x.a.get("href"))).find("h1").contents[0]
					print today
					print OrignalUrl+x.a.get("href")
		else:
			print u"找不到你要的东西"

def Notice(url):
	html = urllib2.urlopen(url)
	# with open("PuNingEdu.txt",'a') as f:
	# 	f.write(html.read())
	if 200 == html.getcode():
		soup = BeautifulSoup(html,"html.parser")		
		content = soup.find_all("div",class_="articleContBox")
		string = content[0].ul.li.span.font.get_text()
		string1 = string.encode("gbk","ignore")
		print string1
		if [] != content:
			for x in content:
				SubContent = x.ul.find_all("li")
				if [] != SubContent:
					print SubContent[0]
					for SubContent2 in SubContent:
						SubDate = SubContent2.span.get_text().replace(" ", "")
						print SubDate
						if today == SubDate:
							print "yes"
				else:
					print u"找不到你要的东西2"
		else:
			print u"找不到你要的东西1"

def main():
	mapping(url,page)

if __name__ == '__main__':
	main()