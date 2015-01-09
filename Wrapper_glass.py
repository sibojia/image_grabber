#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import App

f=open('list.txt').readlines()
i=0
for l in f:
	i+=1
	if i<45: continue 
	name=l.split(' ')[0]
	chname=l.strip().split(' ')[1]
	print i,chname+' 眼镜'
	App.Config.keyword=chname+' 眼镜'
	App.Config.directory = name
	App.Config.count = 10
	if App.main() == 0:
		App.clean()
