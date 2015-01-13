#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import App,os,time

App.Config.site = 'bing_cn'

f=open('list.txt').readlines()
i=0
for l in f:
	i+=1
	# if i<2564: continue 
	name=l.split(' ')[0]
	chname=(l.strip().split(' ')[1]).decode('utf8')
	print i,chname+u' 眼镜'
	if not os.path.exists(name+'/') or len(os.listdir(name+'/')) == 0:
		App.Config.keyword=(chname+u' 眼镜')
		App.Config.directory = name
		App.Config.count = 10
		if App.main() == 0:
			App.clean()
		time.sleep(3)
	else:
		print 'Skipping...'
