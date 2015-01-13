#!/usr/bin/env python2
# -*- coding:utf-8 -*-
from Downloader import getStream
from MyParser import MyParser
from String import longestString, cutTo, cutBegin, getCodingContent
from urllib import urlencode
import json
import re

def getImageUrlFromScript(script):
  pattern = re.compile(r'(?<=imgurl:&quot;).*?(?=&quot;)')
  groups = pattern.findall(script)
  if len(groups[0]) == 0:
    return []
  new_group = [amatch.strip() for amatch in groups] # 更Pythonic的方式
  return new_group

def getImageUrlList(url):
  imglist = []
  stream = getStream(url)
  if stream == None:
    return []
  data = getCodingContent(stream)
  imglist = getImageUrlFromScript(data)
  return imglist
# def bruteGetList(url):
#   stream = getStream(url)
#   data = getCodingContent(stream)
#   pattern = re.compile(r'(?<=objURL=).*?(?=&)')
#   return pattern.findall(data)[0]


def nextPage(url, pn):
  print 'Next page unsupported.'
  return ''

def search(keyword, addtionParams={}):
  """Generate a search url by the given keyword.
  params keyword: utf8 string"""
  url = 'http://cn.bing.com/images/search?'
  parser = MyParser()
  params = _getParams('http://cn.bing.com/images/', parser)
  params.update(addtionParams)
  params.update({'q':keyword.encode('utf8')})
  return url + urlencode(params)

def searchResult(url):
  data = getCodingContent(getStream(url))
  pattern = re.compile('(?<=end=")\d*(?=")')
  count = pattern.findall(data)
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
