#!/usr/bin/python
# -*- coding: cp936 -*-
# Author: Bill JaJa
# Homepage: http://pagebrin.com

import re
import sys
import urllib

def resolve_out_filename(page_main,url_main):
  global out_filename
  out_filename = keyword_filename.search(page_main).group(1) + ".txt"
  # out_filename = "pixnetblog4.txt"
  if website_type == "pixnetblog" or website_type == "chinatimesblog":
    out_filename = out_filename.decode('utf-8').encode('gbk')
  # for debug
  # print "out_filename",out_filename

def resolve_url_sub_page_chapter(url_main):
  global url_sub
  global page_chapter_title
  #global keyword_url_base
  url_sub = []
  page_chapter_title = []
  if website_type == "qqbook" or website_type == "pixnetblog" or website_type == "chinatimesblog":
    url_base = ""
  else:
    global keyword_url_base
    url_base = keyword_url_base.search(url_main).group(1)
  list_url_title = keyword_url.findall(page_main)
  for i in range(len(list_url_title)):
    if website_type == "qqbookorigin":
      url_sub.append(url_base + list_url_title[i][1] + "/chp_info_" + list_url_title[i][2] + ".htm")
      page_chapter_title.append(list_url_title[i][0] + list_url_title[i][3])
    else:
      url_sub.append(url_base + list_url_title[i][0])
      page_chapter_title.append(list_url_title[i][1])
  if website_type == "pixnetblog" or website_type == "chinatimesblog":
    url_sub.reverse()
    page_chapter_title.reverse()
  # for debug
  # print "url_sub",url_sub
  # print "page_chapter_title",page_chapter_title
  
def page_sub_to_chapter(page_sub):
  # global keyword_chapter
  global page_chapter
  page_chapter = keyword_chapter.search(page_sub).group(1)

def page_chapter_format():
  global page_chapter
  keyword_substi_1 = re.compile(r"(<br\s*\/?>)|(<\s*\/?p>)",re.IGNORECASE)
  keyword_substi_2 = re.compile(r"(&\w+;)|(<.*?>)",re.IGNORECASE)
  keyword_substi_3 = re.compile(r"(^\s+)|(\s+$)")
  #keyword_substi_4 = re.compile(r"\t")
  keyword_substi_5 = re.compile(r"(\r\s+)|(\n\s+)")
  page_chapter = keyword_substi_1.sub("\n\n",page_chapter)
  page_chapter = keyword_substi_2.sub("",page_chapter)
  page_chapter = keyword_substi_3.sub("",page_chapter)
  #page_chapter = keyword_substi_4.sub("    ",page_chapter)
  page_chapter = keyword_substi_5.sub("\n\n",page_chapter)
  page_chapter = page_chapter + "\n\n"
  # for debug
  # print page_chapter
    
def content_write200():
  global content_write
  print out_filename,
  out_file = open(out_filename,"a")
  for m in range(len(url_sub)):
    page_cache_sub = urllib.urlopen(url_sub[m])
    percent = (m + 1.0)/len(url_sub) * 100
    page_sub = page_cache_sub.read()
    if m == 0:
      pass
    else:
      print "\b\b\b\b\b\b\b\b\b\b",
    print " %5.2f" % percent,"%",
    # print "Downloading(","%3.1f" % percent,"% )... ",page_chapter_title[m]
    # for debug
    # print "Downloading(","%3.1f" % percent,"% )... ",url_sub[m],page_chapter_title[m]
    page_sub_to_chapter(page_sub)  # get the page content
    page_chapter_format() # format the text
    if m == len(url_sub) - 1:
      global page_chapter
      keyword_substi_6 = re.compile(r"\s+$")
      page_chapter = keyword_substi_6.sub("",page_chapter)
    out_file.write(page_chapter)
  out_file.close()
  print ""
  # print "Write file success."

#####################      
# main program begin.
#####################
def book(url_main):
  url_sub = []
  page_chapter_title = []
  out_filename = ""
  content_write = ""
  global keyword_filename
  global website_type
  global keyword_url
  global keyword_url_base
  global page_main
  global keyword_chapter
  # Obtaion the main page url
  #url_main = raw_input("URL: ")
  # download the main page
  try:
      global page_cache_main
      page_cache_main = urllib.urlopen(url_main)
  except:
      print "Cannot open URL"
      sys.exit()  
  page_main = page_cache_main.read()
  
  if re.search(r"http:\/\/book\.qq\.com",url_main):
    website_type = "qqbook"
    keyword_filename = re.compile(r"<h1>.*：(.*)<\/h1>")
    resolve_out_filename(page_main,url_main)
    # no keyword_url_base
    keyword_url = re.compile(r"javascript:opennew\(\'(http\S*shtml).*>(.*)<\/a>")
    resolve_url_sub_page_chapter(url_main)
    keyword_chapter = re.compile(r"<div\sid=\"content\".*>([\s\S]*?)<\/div>")
  elif re.search(r"http:\/\/bookapp\.book\.qq\.com",url_main):
    website_type = "qqbookorigin"
    keyword_filename = re.compile(r"<title>(.*)_.*<\/title>")
    resolve_out_filename(page_main,url_main)
    keyword_url_base = re.compile(r"(http:\/\/[\.\w]+\/origin\/workintro\/\d+\/)\S+\.shtml")
    keyword_url = re.compile(r"<span\sid=\"cpc_\d+\"><\/span>(.*)<a\shref=\S+workid=(\d+)&chapterid=(\d+).*>(.*)<\/a>")
    resolve_url_sub_page_chapter(url_main)
    keyword_chapter = re.compile(r"<div\sid=\"content\".*>([\s\S]*?)<\/div>")
  elif re.search(r"sina\.com\.cn",url_main):
    website_type = "sinabook"
    keyword_filename = re.compile(r"<h1>(.*)<\/h1>")
    resolve_out_filename(page_main,url_main)
    keyword_url_base = re.compile(r"([\S]+\.sina\.com\.cn\/book\/)")
    keyword_url = re.compile(r"<li><a\shref=\"(chapter_\d+_\d+\.html)\"\starget=\"_blank\">([\s\S]*?)<\/a><\/li>")
    resolve_url_sub_page_chapter(url_main)
    keyword_chapter = re.compile(r"<div\sid=\"contTxt\"\sclass=\"contTxt1\">(.*)<\/div>")
  elif re.search(r"book\.163\.com",url_main):
    website_type = "neteastbook"
    keyword_filename = re.compile(r"\"&shortname=(\S*)\"")
    resolve_out_filename(page_main,url_main)
    keyword_url_base = re.compile(r"([\S]+\.book\.163\.com)")
    keyword_url = re.compile(r"<li>\s*<a\s*href=\"(\/book/section\/\w+\/\w+\.html)\">(.*)<\/a>\s*<\/li>")
    resolve_url_sub_page_chapter(url_main)
    keyword_chapter = re.compile(r"<div\sclass=\"bk-article-body\"\sid=\"bk-article-body\">([\s\S]*?)<\/div>")
  elif re.search(r"lz\.book\.sohu\.com",url_main):
    website_type = "sohubook"
    keyword_filename = re.compile(r"var\s*bookname=\"(\S*)\"")
    resolve_out_filename(page_main,url_main)
    keyword_url_base = re.compile(r"([\S]+lz\.book\.sohu\.com\/)")
    keyword_url = re.compile(r"<li>\s*<a\starget=\"_blank\"\shref=\"(chapter-\d+-\d+.html)\">(.*)<\/a>\s*<\/li>")
    resolve_url_sub_page_chapter(url_main)
    keyword_chapter = re.compile(r"<div\sclass=\"txtC\"\sid=\"txtBg\">[\s\S]*?<p>([\s\S]*?)<\/div>")
  elif re.search(r"vip\.book\.sohu\.com",url_main):
    website_type = "sohubookvip"
    keyword_filename = re.compile(r"<div\sclass=\"booklist_tit\">(\S*)<\/div>")
    resolve_out_filename(page_main,url_main)
    keyword_url_base = re.compile(r"([\S]+vip\.book\.sohu\.com\/)")
    keyword_url = re.compile(r"<li\s*><span\sclass=\"brown\"><\/span><a\shref=\"(\/content/\d+/\d+\/)\"[\s\S]*?>([\s\S]*?)<\/a>\s*<\/li>")
    resolve_url_sub_page_chapter(url_main)
    keyword_chapter = re.compile(r"<div\sclass=\"artical_tit\">[\s\S]*?<\/table>\s*<p>([\s\S]*?)<\s*\/div>")
  elif re.search(r"\S+\.pixnet\.net\/blog",url_main):
    website_type = "pixnetblog"
    keyword_filename = re.compile(r"<meta\sname=\"description\"\scontent=\"([\s\S]*?)\">")
    resolve_out_filename(page_main,url_main)
    # no keyword_url_base
    keyword_url = re.compile(r"<li\sclass=\"title\"\sid=\"article[\d-]+\"><h2><a\shref=\"(\S+\.pixnet.net\/blog\/post\/\d+)\">(.*?)<\/a><\/h2><\/li>")
    resolve_url_sub_page_chapter(url_main)
    keyword_chapter = re.compile(r"<div\sclass=\"article-content\">([\s\S]*?)<\s*\/div>")
  elif re.search(r"\S+blog\.chinatimes\.com",url_main):
    website_type = "chinatimesblog"
    keyword_filename = re.compile(r"<SPAN\sclass=\"highlight\">\s*(\S+)<\/SPAN>")
    resolve_out_filename(page_main,url_main)
    # no keyword_url_base
    keyword_url = re.compile(r"<a\sid=\"CategoryEntryList1_EntryStoryList_Results__ctl\d+_Hyperlink3\"\shref=\"(http:\/\/blog\.chinatimes\.com\/[\w\/_-]+\.html)\".*?>(.*?)<\/a>")
    resolve_url_sub_page_chapter(url_main)
    keyword_chapter = re.compile(r"<div\sid=\"article_content\">([\s\S]*?)<\/div>\s+<\/div>")
    
  content_write200()

if __name__ == "__main__":
  url_main = raw_input("URL: ")
  book(url_main=url_main)
