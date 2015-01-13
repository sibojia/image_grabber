#!/usr/bin/env python2
# -*- coding:utf-8 -*-
# from Baidu import getImageUrlList, search, nextPage, searchResult
import Baidu, BingCN
from Downloader import downloadFromQueue
from FileHelper import getFilenameFromURL, addExtension, makedir
from Queue import Queue
from thread import start_new_thread
from Config import Config
from NetworkPrepare import prepare
import os, sys
import traceback

def site_config():
  if Config.site == 'baidu':
    return Baidu
  if Config.site == 'bing_cn':
    return BingCN
  else:
    print 'Unsupported site. Exiting.'
    sys.exit(-1)

def main():
  try:
    # 开始准备
    prepare()
    SiteTool = site_config()
    while_n = 0 # 循环计数器
    imglist = []
    makedir(Config.directory)
    print 'Generate search url',
    URL = SiteTool.search(Config.keyword, Config.addtional)
    print URL
    # 下载 #############
    # 获取搜索结果数量并与_count比较取其较小值
    count = min(SiteTool.searchResult(URL), Config.count)
    # 没有搜索结果时退出
    if not count:
      print "No search result at current condition."
      return -1
    # 获得指定数量的url, 存放于list  
    print 'Fetching page',
    while len(imglist) < count:
      print while_n,
      while_n += 1
      tmplist = SiteTool.getImageUrlList(URL)
      if len(tmplist) == 0:
      	print "getImageUrlList error."
      	return -1
      if(len(tmplist)+len(imglist) > count):
        imglist = imglist + tmplist[:count-len(imglist)]
      else:
      	imglist = imglist + tmplist
      	URL = SiteTool.nextPage(URL, len(tmplist))
    print '' # 换行
    count = len(imglist)
    print "There're %d files to download" % count
    # 将已有文件从imglist中去除
    imglist = [url for url in imglist
	      if not getFilenameFromURL(url) in os.listdir(Config.directory)]
    print "There's %d files already downloaded." % (count - len(imglist))
    # 下载该list 
    print 'Fetching list of %d files' % len(imglist)
    queue = Queue()
    for url in imglist:
      queue.put(url)
    failure = []
    for i in range(Config.thread_count):
      start_new_thread(downloadFromQueue, (
					  queue, failure, Config.directory, Config.timeout))
    queue.join()
    print "%d failed to fetch." % len(failure)
    return 0
  except Exception, e:
    print e
    print traceback.format_exc()
    return -1

def clean():
  # 清理
  # 1.添加后缀
  print 'Adding extension ...'
  for fname in os.listdir(Config.directory):
    addExtension(Config.directory + os.sep + fname, '.jpg')
  print 'done.'
  # 2.保存cookie
  Config.cj.save()

if __name__ == "__main__":
  main()
  clean()
