#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from Downloader import getStream
from MyParser import MyParser
from String import longestString, cutTo, cutBegin, getCodingContent
from urllib import urlencode
import json
import re

def getImageUrlFromScript(script):
  pattern = re.compile(r'(?<="objURL":").*?(?=")')
  groups = pattern.findall(script)
  new_group = [amatch.strip() for amatch in groups] # 更Pythonic的方式
  return new_group

def getImageUrlList(url):
  imglist = []
  jsonlist = _getJsonList(url)
  if jsonlist == None:
    return []
  for i in jsonlist:
    imglist.append(i['objURL'].strip())
  return imglist
# def bruteGetList(url):
#   stream = getStream(url)
#   data = getCodingContent(stream)
#   pattern = re.compile(r'(?<=objURL=).*?(?=&)')
#   return pattern.findall(data)[0]

def _getJsonList(url):
  stream = getStream(url)
  if stream == None:
    return None
  data = getCodingContent(stream)
  # start=data.index('var imgTempData')
  # end=data[start:].index(';')
  # block=data[start+18:start+end]
  pattern = re.compile(r'(?<=var imgdata =).*?}(?=;var)')
  block = pattern.findall(data)[0]
  try:
	  jsonlist = json.loads(block)
	  return jsonlist['data'][:-1]
  except:
	  print 'json load error. write to debug.txt'
	  f=open('debug.txt','w')
	  f.write(data.encode('utf8'))
	  f.close()
	  return None


def nextPage(url, pn):
  url_pn = cutBegin(url, '&pn=')
  if not url_pn:
    url_pn = 0
  url_pn = int(url_pn) + pn
  return cutTo(url, '&pn') + '&pn=' + str(url_pn)

def search(keyword, addtionParams={}):
  """Generate a search url by the given keyword.
  params keyword: utf8 string"""
  url = 'http://image.baidu.com/i?'
  parser = MyParser()
  params = _getParams('http://image.baidu.com', parser)
  params.update(addtionParams)
  params.update({'word':keyword.encode('utf8'),'tn': 'result_pageturn'})
  return url + urlencode(params)

def searchResult(url):
  parser = MyParser()
  parser.feed(getCodingContent(getStream(url)))
  block = longestString(parser.scriptList)
  parser.close()
  pattern = re.compile('(?<="listNum":)\d*(?=,)')
  count = pattern.findall(block)
  if count:
    count = int(count[0])
    return count
  return 0

def _getParams(url, parser):
  """Get a dict contained the url params"""
  stream = getStream(url)
  data = getCodingContent(stream)
  parser.feed(data)
  return parser.formParams

def _appendParams(adict):
  """Generate a url with params in adict."""
  p = [key + '=' + adict[key] for key in adict]
  return '&'.join(p)
