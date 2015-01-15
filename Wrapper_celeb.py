#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import App,os,time,sys

App.Config.site = 'baidu'
App.Config.addtional = {'z':'3'}
# App.Config.addtional = {'qft':'+filterui:imagesize-large'}
App.Config.proxy = 'localhost:1080'
App.Config.use_proxy = False

f=open(sys.argv[1]).readlines()
i=0
for l in f:
	i+=1
	# if i<2564: continue 
	name=l.strip()
	print i,name
	if not os.path.exists(name+'/') or len(os.listdir(name+'/')) < 15:
		App.Config.keyword=name
		App.Config.directory=name
		App.Config.count =20
		if App.main() == 0:
			App.clean()
		time.sleep(1)
	else:
		print 'Skipping...'
