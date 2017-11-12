#coding:utf-8
import sys
import time
from flask import Flask, render_template,request
from flask.ext.moment import Moment

from . import main
import urllib
import urllib2
import  json
import re
import requests
import md5

#API地址
gateway = 'http://api.hz66.com/'
#公钥
auth_key = 'ad99a64c86ecd7cd47fd3b344a2513dd'
#私钥
auth_secret = 'ecefd649b9958a0aeed84c8487788f42'

#读cmstop的json数据的函数
def read_cmstop_json(url):
	data = None
    
	list_stream = urllib2.urlopen(url)
	
	content = list_stream.read()
	python_to_json = json.loads(content)

	data = python_to_json['data']

	return data

#得到菜单的json数据
def get_menu_json(id):
  	#显示菜单
	api_url = '?app=system&controller=category&action=ls'
	
	flag = 'catid=' + str(id)
	
	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag
	tags = read_cmstop_json(request_url)

	return tags

#得到栏目页的json数据
def get_list_json(id):
	api_url = '?app=system&controller=content&action=ls'

	flag = 'catid=' + urllib.quote(id)

	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag

	column = read_cmstop_json(request_url)

	return column

#显示区块内容
def get_section(sectionid):
	api_url = '?app=page&controller=section&action=get'
	
	flag = 'sectionid=' + str(sectionid)
	
	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag

	list_stream = urllib2.urlopen(request_url)

	list_stream = list_stream.read()

	python_to_json = json.loads(list_stream)
	
	return python_to_json

#显示图片幻灯内容
def get_img_json(id):
	api_url = '?app=system&controller=content&action=ls'
	
	flag = 'catid=' + urllib.quote(id)+ '&size=6' +'&weight=' + '100'
	
	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag

	list_stream = urllib2.urlopen(request_url)

	section = list_stream.read()

	python_to_json = json.loads(section)

	return python_to_json['data']


#全局首页
@main.route('/', methods=['GET', 'POST'])
def index():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	#显示菜单
	menuid = request.args.get('catid', '?catid=27,28,29,30,31，97')
	type = request.args.get('type', '0')
	tags = get_menu_json('100')

	#显示幻灯图
	imgid = menuid
	imgs = get_img_json(imgid)
	#显示列表
	catid = request.args.get('catid','27,28,29,30,31')
	column = get_list_json(catid)

	return render_template('main/index.html', main_title=u'湖州在线手机版', tags = tags, \
		column = column, catid = catid, imgs = imgs, type = type)

#报纸
@main.route('/paper/', methods=['GET', 'POST'])
def paper():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	return render_template('main/paper.html', main_title=u'湖州在线手机版')

#列出手机版栏目
@main.route('/list/' , methods=['GET', 'POST'])
def list():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	api_url = '?app=system&controller=category&action=ls'
	catid = request.args.get('catid', '1')

	#flag = 'published=' + '2017-10-17' +'&size=' + str(1000)
	flag = 'catid=' + str(catid)

	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag


	list_stream = urllib2.urlopen(request_url)

	content = list_stream.read()

	python_to_json = json.loads(content)

	for pjson in python_to_json['data']:
		print pjson

	return content.decode('unicode_escape')

#列出指定栏目中的内容
@main.route('/column/' , methods=['GET', 'POST'])
def column():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	api_url = '?app=system&controller=content&action=ls'

	catid = request.args.get('catid', '1')
	size = request.args.get('size', '10')
	offset = request.args.get('offset','0')
	page = request.args.get('page','1')

	size = 15

	flag = 'catid=' + urllib.quote(catid) + '&page=' + str(page) + '&size=' + str(size)

	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag

	list_stream = urllib2.urlopen(request_url)

	content = list_stream.read()

	data = json.loads(content)

	return 'cmstop_callback('+json.dumps(data['data'])+')'
	#return 'cmstop_callback('+content.decode('unicode_escape')+');'

#显示内容页
@main.route('/content/' , methods=['GET', 'POST'])
def content():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	#显示菜单
	api_url = '?app=system&controller=category&action=ls'
	catid = request.args.get('catid', '100')
	
	flag = 'catid=' + str(100)
	
	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag
	tags = read_cmstop_json(request_url)

	#内容
	api_url = '?app=article&controller=article&action=get'
	contentid = request.args.get('contentid', '1')

	#flag = 'published=' + '2017-10-17' +'&size=' + str(1000)
	flag = 'contentid=' + urllib.quote(contentid)

	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag

	content_stream = urllib2.urlopen(request_url)

	content = content_stream.read()
	content_data = json.loads(content)

	data = content_data['data']
		
	if data != False:
		#转换成localtime
		curr_time = None
		curr_time = int(data['published'])
	
		time_local = time.localtime(curr_time)
		#转换成新的时间格式(2016-05-05 20:28:54)
		dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

		data['published'] = dt
		#return content.decode('unicode_escape')
	
	return render_template('main/content.html', main_title=u'湖州在线手机版', tags = tags, content = data)


#显示内容页
@main.route('/content2/' , methods=['GET', 'POST'])
def content2():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	#显示菜单
	api_url = '?app=system&controller=category&action=ls'
	catid = request.args.get('catid', '96')
	
	flag = 'catid=' + str(96)
	
	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag
	tags = read_cmstop_json(request_url)

	#内容
	api_url = '?app=article&controller=article&action=get'
	contentid = request.args.get('contentid', '1')

	#flag = 'published=' + '2017-10-17' +'&size=' + str(1000)
	flag = 'contentid=' + str(contentid)

	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag

	content_stream = urllib2.urlopen(request_url)

	content = content_stream.read()
	content_data = json.loads(content)
	data = content_data['data']

	return content.decode('unicode_escape')


#显示内容页
@main.route('/video/' , methods=['GET', 'POST'])
def getvideo():
	reload(sys)
	sys.setdefaultencoding('utf-8')

	#显示菜单
	api_url = '?app=system&controller=category&action=ls'
	catid = request.args.get('catid', '96')
	
	flag = 'catid=' + str(96)
	
	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag
	tags = read_cmstop_json(request_url)

	#内容
	api_url = '?app=video&controller=video&action=get'
	contentid = request.args.get('contentid', '1')

	#flag = 'published=' + '2017-10-17' +'&size=' + str(1000)
	flag = 'contentid=' + urllib.quote(contentid)

	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag

	content_stream = urllib2.urlopen(request_url)

	content = content_stream.read()
	content_data = json.loads(content)

	return content.decode('unicode_escape')

#显示内容页
@main.route('/test/' , methods=['GET', 'POST'])
def test():
	'''
	vaule = {}

	api_url='?app=system&controller=content&action=ls'
	
	reload(sys)  
	sys.setdefaultencoding('utf-8')

	catid = request.args.get('catid', '27')
	size = request.args.get('size', '15')

	flag = 'catid=' + urllib.quote(catid) + '&size=' + urllib.quote(size)
	print flag

	sign = md5.new()
	sign.update(flag + auth_secret)

	request_url = gateway + api_url + '&key=' +auth_key + '&sign=' + sign.hexdigest() + '&' + flag 
	print request_url
	
	data = None
	list_stream = urllib2.urlopen(request_url)
	content = list_stream.read()
	python_to_json = json.loads(content)

	return content.decode('unicode_escape')
	'''
	data = get_section(279)
	return data
