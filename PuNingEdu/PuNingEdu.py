# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import base64

# 当没有添加http://的时候，会报错，python - ValueError: unknown url type
OrignalUrl = "http://www.pnjyj.gov.cn/"
url = "http://www.pnjyj.gov.cn/wap.php?action=list&id=23&totalresult=47&pageno="
NoticeUrl = "http://www.pnjyj.gov.cn/plus/list.php?tid=23"
page = 1
today = "("+date.today().isoformat()[-5:]+")"
month = today[1:3]
MailContent = ""

def mapping(url,page):
	global MailContent
	UrlString = url + str(page)
	html = urllib2.urlopen(UrlString)
	if 200 == html.getcode():
		soup = BeautifulSoup(html)
		content = soup.find_all("li")
		if [] != content:
			for x in content:
				if x.span.contents[0][1:3] == month :
					intime = x.span.contents[0]
					incontent = BeautifulSoup(urllib2.urlopen(OrignalUrl+x.a.get("href"))).find("h1").contents[0]
					print intime + incontent
					print "\n"
					MailContent += intime
					MailContent += incontent
					MailContent += "\n"
		else:
			print month + u"月没有公告" + "\n"
	print "end\n"

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

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def SendMail():
	global MailContent
	from_addr = 'xhz_public1@163.com'
	password = 'xhz123456'
	to_addr = '470001421@qq.com'
	smtp_server = 'smtp.163.com'

	msg = MIMEText(MailContent, 'plain', 'utf-8')
	msg['From'] = _format_addr('xhz_public <%s>' % from_addr)
	msg['To'] = _format_addr('xhz <%s>' % to_addr)
	msg['Subject'] = Header('普宁教育局-公告内容', 'utf-8').encode()

	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(base64.encodestring(from_addr), base64.encodestring(password))
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()

def main():
	# 如果时间等于中午12点的时候，就爬一次
	Time = datetime.now()
	# if (23 == Time.hour) and (14 == Time.minute) :
	# 	mapping(url,page)
	# 	SendMail()
	# 	raw_input()
	# else:
	# 	print u"时间还没到12点00分"

	if True :
		mapping(url,page)
		raw_input()

if __name__ == '__main__':
	main()