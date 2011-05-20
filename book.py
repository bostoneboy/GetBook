#!/usr/bin/python
# -*- coding: cp936 -*-
# python 2.x
# Author: Bill JaJa
# Project Home: http://github.com/bostoneboy/GetBook

import re
import os
import sys
import random
import urllib
import platform
 
def conv_to_utf8(content):
  # dest_charset = "utf-8"
  if source_charset not in ("utf-8","UTF-8"):
    return (content).decode(source_charset,"ignore").encode("utf-8")
  else:
    return content

def random_char(number_of_chars):
  basestring = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  return "".join(random.sample(basestring,number_of_chars))

def conv_filename(filename):
  # filename use unicode if host is windows.
  # filename use utf-8 if host is linux or mac osx.
  if source_charset in ("gb2312","GB2312"):
    source_charset2 = "gbk"
  else:
    source_charset2 = source_charset
  os_type = platform.system() 
  if os_type == "Windows":
    filename = (filename).decode(source_charset2,"ignore") + ".txt"
  elif os_type in ("Linux","Darwin"):
    filename = conv_to_utf8(filename) + ".txt"
  else:
    filename = "ErrorOsType-" + random_char(5) + ".txt"
  return filename

def resolve_out_filename(page_main,keyword):
  global source_charset
  keyword_charset = re.compile(r"charset=([\w-]+)",re.IGNORECASE)
  source_charset = keyword_charset.search(page_main).group(1)
  filename = keyword.search(page_main)
  if filename:
    filename = filename.group(1)
  else:
    filename = "sample-" + random_char(5)
  filename = conv_filename(filename)
  # for debug
  # print out_filename,source_charset
  return filename

def resolve_url_sub_page_chapter(url_main,page_main,website_type,keyword_url,keyword_url_base):
  url_sub = []
  global page_chapter_title
  page_chapter_title = []
  if website_type in ("qqbook","pixnetblog","chinatimesblog"):
    url_base = ""
  else:
    url_base = keyword_url_base.search(url_main).group(1)
  list_url_title = keyword_url.findall(page_main)
  for i in range(len(list_url_title)):
    if website_type == "qqbookorigin":
      url_sub.append(url_base + list_url_title[i][1] + "/chp_info_" + list_url_title[i][2] + ".htm")
      page_chapter_title.append(list_url_title[i][0] + list_url_title[i][3])
    else:
      url_sub.append(url_base + list_url_title[i][0])
      page_chapter_title.append(list_url_title[i][1])
  if website_type in ("pixnetblog","chinatimesblog"):
    url_sub.reverse()
    page_chapter_title.reverse()
  # for debug
  # print "url_sub",url_sub
  # print "page_chapter_title",page_chapter_title
  return url_sub
  
def page_sub_to_chapter(page_sub,keyword_chapter):
  # page_chapter = keyword_chapter.search(page_sub).group(1)
  result = keyword_chapter.search(page_sub)
  if result:
    page_chapter = result.group(1)
  else:
    page_chapter = keyword_chapter2.search(page_sub).group(1)
  # for debug
  # print page_chapter
  return page_chapter

def page_chapter_format(page_chapter):
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
  return page_chapter


######################   
# main program begin.#
######################
def book(url_main):
  if re.search(r"http:\/\/book\.qq\.com",url_main):
    website_type = "qqbook"
    # keyword_filename = re.compile(r"<h1>.*：(.*)<\/h1>")
    keyword_filename = re.compile(r"<title>(.*?)_.*<\/title>")
    # no keyword_url_base
    keyword_url_base = ""
    keyword_url = re.compile(r"javascript:opennew\(\'(http\S*shtml).*?>([\s\S]*?)<\/a>")
    keyword_chapter = re.compile(r"<div\sid=\"content\".*>([\s\S]*?)<\/div>")
  elif re.search(r"http:\/\/bookapp\.book\.qq\.com",url_main):
    website_type = "qqbookorigin"
    keyword_filename = re.compile(r"<title>(.*?)_.*<\/title>")
    keyword_url_base = re.compile(r"(http:\/\/[\.\w]+\/origin\/workintro\/\d+\/)\S+\.shtml")
    keyword_url = re.compile(r"<span\sid=\"cpc_\d+\"><\/span>(.*)<a\shref=\S+workid=(\d+)&chapterid=(\d+).*>(.*)<\/a>")
    keyword_chapter = re.compile(r"<div\sid=\"content\".*>([\s\S]*?)<\/div>")
  elif re.search(r"sina\.com\.cn",url_main):
    website_type = "sinabook"
    keyword_filename = re.compile(r"<h1>(.*)<\/h1>")
    keyword_url_base = re.compile(r"([\S]+\.sina\.com\.cn\/book\/)")
    keyword_url = re.compile(r"<li><a\shref=\"(chapter_\d+_\d+\.html)\"\starget=\"_blank\">([\s\S]*?)<\/a><\/li>")
    keyword_chapter = re.compile(r"<div\sid=\"contTxt\"\sclass=\"contTxt1\">(.*)<\/div>")
  elif re.search(r"book\.163\.com",url_main):
    website_type = "neteastbook"
    keyword_filename = re.compile(r"\"&shortname=(.*?)\"")
    keyword_url_base = re.compile(r"([\S]+\.book\.163\.com)")
    keyword_url = re.compile(r"<li>\s*<a\s*href=\"(\/book/section\/\w+\/\w+\.html)\">(.*)<\/a>\s*<\/li>")
    keyword_chapter = re.compile(r"<div\sclass=\"bk-article-body\"\sid=\"bk-article-body\">([\s\S]*?)<\/div>")
    #keyword_chapter2 = re.compile(r"class=\"aContent\">([\s\S]*?)<p\sclass=\"aPages\">")
  elif re.search(r"lz\.book\.\.m",url_main):
    website_type = "sohubook"
    keyword_filename = re.compile(r"var\s*bookname=\"(.*?)\"")
    keyword_url_base = re.compile(r"([\S]+lz\.book\.sohu\.com\/)")
    keyword_url = re.compile(r"<li>\s*<a\starget=\"_blank\"\shref=\"(chapter-\d+-\d+.html)\">(.*)<\/a>\s*<\/li>")
    keyword_chapter = re.compile(r"<div\sclass=\"txtC\"\sid=\"txtBg\">[\s\S]*?<p>([\s\S]*?)<\/div>")
  elif re.search(r"vip\.book\.sohu\.com",url_main):
    website_type = "sohubookvip"
    keyword_filename = re.compile(r"<div\sclass=\"booklist_tit\">(.*?)<\/div>")
    keyword_url_base = re.compile(r"([\S]+vip\.book\.sohu\.com\/)")
    keyword_url = re.compile(r"<li\s*><span\sclass=\"brown\"><\/span><a\shref=\"(\/content/\d+/\d+\/)\"[\s\S]*?>([\s\S]*?)<\/a>\s*<\/li>")
    keyword_chapter = re.compile(r"<div\sclass=\"artical_tit\">[\s\S]*?<\/table>\s*<p>([\s\S]*?)<\s*\/div>")
  elif re.search(r"\S+\.pixnet\.net\/blog",url_main):
    website_type = "pixnetblog"
    keyword_filename = re.compile(r"<meta\sname=\"description\"\scontent=\"([\s\S]*?)\">")
    # no keyword_url_base
    keyword_url_base = ""
    keyword_url = re.compile(r"<li\sclass=\"title\"\sid=\"article[\d-]+\"><h2><a\shref=\"(\S+\.pixnet.net\/blog\/post\/\d+)\">(.*?)<\/a><\/h2><\/li>")
    keyword_chapter = re.compile(r"<div\sclass=\"article-content\">([\s\S]*?)<\s*\/div>")
  elif re.search(r"\S+blog\.chinatimes\.com",url_main):
    website_type = "chinatimesblog"
    keyword_filename = re.compile(r"<SPAN\sclass=\"highlight\">\s*(.*?)<\/SPAN>")
    # no keyword_url_base
    keyword_url_base = ""
    keyword_url = re.compile(r"<a\sid=\"CategoryEntryList1_EntryStoryList_Results__ctl\d+_Hyperlink3\"\shref=\"(http:\/\/blog\.chinatimes\.com\/[\w\/_-]+\.html)\".*?>(.*?)<\/a>")
    keyword_chapter = re.compile(r"<div\sid=\"article_content\">([\s\S]*?)<\/div>\s+<\/div>")

  try:
      global page_cache_main
      page_cache_main = urllib.urlopen(url_main)
  except:
      print "Cannot open URL"
      sys.exit()

  page_main = page_cache_main.read()
  out_filename = resolve_out_filename(page_main,keyword_filename)
  print out_filename,
  out_file = open(out_filename,"a")
  url_sub = resolve_url_sub_page_chapter(url_main,page_main,website_type,keyword_url,keyword_url_base)
  
  for m in range(len(url_sub)):
    page_cache_sub = urllib.urlopen(url_sub[m])
    percent = (m + 1.0)/len(url_sub) * 100
    page_sub = page_cache_sub.read()
    if m == 0:
      pass
    else:
      print "\b\b\b\b\b\b\b\b\b\b",
    print " %5.2f" % percent,"%",
    # for debug
    # print "Downloading(","%3.1f" % percent,"% )... ",url_sub[m],page_chapter_title[m]
    # get chapter content from sub page
    page_chapter = page_sub_to_chapter(page_sub,keyword_chapter)
    # format the text
    page_chapter = page_chapter_format(page_chapter)
    if m == len(url_sub) - 1:
      keyword_substi_6 = re.compile(r"\s+$")
      page_chapter = keyword_substi_6.sub("",page_chapter)
    # convert the content from $source_charset to utf-8
    page_chapter = conv_to_utf8(page_chapter)
    out_file.write(page_chapter)
  whole_file = open(out_filename,"r").read()
  out_file.close()
  if re.search(r"^\s*$",whole_file):
    print "\b\b\b\b\b\b\b\b\b\bThere is no content to match, REJECT!"
    os.remove(out_filename)
  else:
    print ""

if __name__ == "__main__":
  url_main = raw_input("URL: ")
  url_suffix = re.search(r"(http:.*\.s?html)\?\w+",url_main)
  if url_suffix:
    url_main = url_suffix.group(1)
  book(url_main)
