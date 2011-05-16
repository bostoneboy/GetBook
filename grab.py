#!/usr/bin/python
# Homepage: http://pagebrin.com

import re
import urllib
from book import book

url_grub = "http://book.qq.com/rankcount/lz_ph_top100_click_month_13.htm"
file_grub = urllib.urlopen(url_grub)
file_content = file_grub.read()
keyword_grub = re.compile(r"<a\shref=\"(http:\/\/book\.qq\.com\/s\/book\/[\d\/]+\/index\.shtml)\"\starget=\"_blank\">")
url_list_origin = keyword_grub.findall(file_content)
url_list_origin.reverse()
url_list = []
url_list.append(url_list_origin[0])
for i in range(1,len(url_list_origin)):
  if url_list_origin[i] != url_list_origin[i-1]:
    url_list.append(url_list_origin[i])
for i in url_list:
  book(i)
