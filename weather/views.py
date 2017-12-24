# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import loader,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import csrf_token
from django.db import IntegrityError
from django.core import serializers
from django.shortcuts import render
from weather.models import Weather,Country
import re
import StringIO
import unicodedata
import requests
import json
import time

# --- Initial Config ----
# Set Maximum Retry For URL Requests
r_session = requests.Session()
url_max_retry = 6
http = requests.adapters.HTTPAdapter(max_retries=url_max_retry)
https = requests.adapters.HTTPAdapter(max_retries=url_max_retry)
r_session.mount('http://', http)
r_session.mount('https://', https)



# Index Page View
@csrf_exempt
def index(request):
	if request.GET.get('view','')=='graph':
		template = loader.get_template('index.html')
		return HttpResponse(template.render({'graph':True}))
	else:
		template = loader.get_template('index.html')
		return HttpResponse(template.render({'index':True}))


# Graph Page View
@csrf_exempt
def graph(request):
	template = loader.get_template('graph.html')
	country = request.GET.get('country','')
	scale_x = 'Years'
	scale_y = ' '
	if request.GET.get('country','')=="UK":
		if request.GET.get('tag_code','')=="UK_TMAX":
			data = graph_data("UK","UK_TMAX")
			scale_y = 'UK Temp Max (Degrees C)'
		elif request.GET.get('tag_code','')=="UK_TMIN":
			data = graph_data("UK","UK_TMIN")
			scale_y = 'UK Temp Min (Degrees C)'
		elif request.GET.get('tag_code','')=="UK_TMEAN":
			data = graph_data("UK","UK_TMEAN")
			scale_y = 'UK Temp Mean (Degrees C)'
		elif request.GET.get('tag_code','')=="UK_SUNSHINE":
			data = graph_data("UK","UK_SUNSHINE")
			scale_y = 'UK Sunshine (Total Hours)'
		elif request.GET.get('tag_code','')=="UK_RAINFALL":
			data = graph_data("UK","UK_RAINFALL")
			scale_y = 'UK Rainfall (mm)'

	elif request.GET.get('country','')=="England":
		if request.GET.get('tag_code','')=="England_TMAX":
			data = graph_data("England","England_TMAX")
			scale_y = 'England Temp Max (Degrees C)'
		elif request.GET.get('tag_code','')=="England_TMIN":
			data = graph_data("England","England_TMIN")
			scale_y = 'England Temp Min (Degrees C)'
		elif request.GET.get('tag_code','')=="England_TMEAN":
			data = graph_data("England","England_TMEAN")
			scale_y = 'England Temp Mean (Degrees C)'
		elif request.GET.get('tag_code','')=="England_SUNSHINE":
			data = graph_data("England","England_SUNSHINE")
			scale_y = 'England Sunshine (Total Hours)'
		elif request.GET.get('tag_code','')=="England_RAINFALL":
			data = graph_data("England","England_RAINFALL")
			scale_y = 'England Rainfall (mm)'

	elif request.GET.get('country','')=="Wales":
		if request.GET.get('tag_code','')=="Wales_TMAX":
			data = graph_data("Wales","Wales_TMAX")
			scale_y = 'Wales Temp Max (Degrees C)'
		elif request.GET.get('tag_code','')=="Wales_TMIN":
			data = graph_data("Wales","Wales_TMIN")
			scale_y = 'Wales Temp Min (Degrees C)'
		elif request.GET.get('tag_code','')=="Wales_TMEAN":
			data = graph_data("Wales","Wales_TMEAN")
			scale_y = 'Wales Temp Mean (Degrees C)'
		elif request.GET.get('tag_code','')=="Wales_SUNSHINE":
			data = graph_data("Wales","Wales_SUNSHINE")
			scale_y = 'Wales Sunshine (Total Hours)'
		elif request.GET.get('tag_code','')=="Wales_RAINFALL":
			data = graph_data("Wales","Wales_RAINFALL")
			scale_y = 'Wales Rainfall (mm)'

	elif request.GET.get('country','')=="Scotland":
		if request.GET.get('tag_code','')=="Scotland_TMAX":
			data = graph_data("Scotland","Scotland_TMAX")
			scale_y = 'Scotland Temp Max (Degrees C)'
		elif request.GET.get('tag_code','')=="Scotland_TMIN":
			data = graph_data("Scotland","Scotland_TMIN")
			scale_y = 'Scotland Temp Min (Degrees C)'
		elif request.GET.get('tag_code','')=="Scotland_TMEAN":
			data = graph_data("Scotland","Scotland_TMEAN")
			scale_y = 'Scotland Temp Mean (Degrees C)'
		elif request.GET.get('tag_code','')=="Scotland_SUNSHINE":
			data = graph_data("Scotland","Scotland_SUNSHINE")
			scale_y = 'Scotland Sunshine (Total Hours)'
		elif request.GET.get('tag_code','')=="Scotland_RAINFALL":
			data = graph_data("Scotland","Scotland_RAINFALL")
			scale_y = 'Scotland Rainfall (mm)'

	else:
		return HttpResponse("Error : No Valid Graph Request Found !")

	return HttpResponse(template.render({'graph_name':country, "data":data, "scale":[scale_x,scale_y]}))


# Get Data From Table For Populating Graph
def graph_data(country,tag_code):
	try:

		# | Grab Only Last 20 Records FOR BETTER VIEW And QUERY PERFORMANCE
		if country=="UK":
			if tag_code=="UK_TMAX":
				data =  Weather.objects.filter(country_code=1,tag_code="UK_TMAX").order_by('-id')[:20]
				return data
			elif tag_code=="UK_TMIN":
				data =  Weather.objects.filter(country_code=1,tag_code="UK_TMIN").order_by('-id')[:20]
				return data
			elif tag_code=="UK_TMEAN":
				data =  Weather.objects.filter(country_code=1,tag_code="UK_TMEAN").order_by('-id')[:20]
				return data
			elif tag_code=="UK_SUNSHINE":
				data =  Weather.objects.filter(country_code=1,tag_code="UK_SUNSHINE").order_by('-id')[:20]		
				return data
			elif tag_code=="UK_RAINFALL":
				data =  Weather.objects.filter(country_code=1,tag_code="UK_RAINFALL").order_by('-id')[:20]
				return data
		
		elif country=="England":
			if tag_code=="England_TMAX":
				data =  Weather.objects.filter(country_code=2,tag_code="England_TMAX").order_by('-id')[:20]
				return data
			elif tag_code=="England_TMIN":
				data =  Weather.objects.filter(country_code=2,tag_code="England_TMIN").order_by('-id')[:20]
				return data
			elif tag_code=="England_TMEAN":
				data =  Weather.objects.filter(country_code=2,tag_code="England_TMEAN").order_by('-id')[:20]				
				return data
			elif tag_code=="England_SUNSHINE":
				data =  Weather.objects.filter(country_code=2,tag_code="England_SUNSHINE").order_by('-id')[:20]		
				return data
			elif tag_code=="England_RAINFALL":
				data =  Weather.objects.filter(country_code=2,tag_code="England_RAINFALL").order_by('-id')[:20]
				return data

		elif country=="Wales":
			if tag_code=="Wales_TMAX":
				data =  Weather.objects.filter(country_code=3,tag_code="Wales_TMAX").order_by('-id')[:20]
				return data
			elif tag_code=="Wales_TMIN":
				data =  Weather.objects.filter(country_code=3,tag_code="Wales_TMIN").order_by('-id')[:20]
				return data
			elif tag_code=="Wales_TMEAN":
				data =  Weather.objects.filter(country_code=3,tag_code="Wales_TMEAN").order_by('-id')[:20]				
				return data
			elif tag_code=="Wales_SUNSHINE":
				data =  Weather.objects.filter(country_code=3,tag_code="Wales_SUNSHINE").order_by('-id')[:20]		
				return data
			elif tag_code=="Wales_RAINFALL":
				data =  Weather.objects.filter(country_code=3,tag_code="Wales_RAINFALL").order_by('-id')[:20]
				return data

		elif country=="Scotland":
			if tag_code=="Scotland_TMAX":
				data =  Weather.objects.filter(country_code=4,tag_code="Scotland_TMAX").order_by('-id')[:20]
				return data
			elif tag_code=="Scotland_TMIN":
				data =  Weather.objects.filter(country_code=4,tag_code="Scotland_TMIN").order_by('-id')[:20]
				return data
			elif tag_code=="Scotland_TMEAN":
				data =  Weather.objects.filter(country_code=4,tag_code="Scotland_TMEAN").order_by('-id')[:20]				
				return data
			elif tag_code=="Scotland_SUNSHINE":
				data =  Weather.objects.filter(country_code=4,tag_code="Scotland_SUNSHINE").order_by('-id')[:20]		
				return data
			elif tag_code=="Scotland_RAINFALL":
				data =  Weather.objects.filter(country_code=4,tag_code="Scotland_RAINFALL").order_by('-id')[:20]
				return data
		else:
			return HttpResponse("Error : No Valid Graph Request Found !")		

	except Exception,e:
		data = {'Status':'Fail','Message':str(e)}
		return HttpResponse(data)


# Run The Automated Process
@csrf_exempt
def run(request):
	if  request.method == 'POST' and request.is_ajax() and request.POST.get('submit','') == 'run':
		crawl_page()
		return HttpResponse("Message : Completed Check The DB For Data Or Explore The Graph By Clicking Below Button !")
	else:
		return HttpResponse("Error : Please Submit The Form Again !")


# Crawl Page And Download File
def crawl_page(url='https://www.metoffice.gov.uk/climate/uk/summaries/datasets',keywords=['UK','England','Wales','Scotland']):
	if type(keywords) is list:
		url_data = r_session.get(url)
		for name in keywords:
			print "Crawling Page Data For : {0}".format(name)
			link_tmax = r_session.get(re.findall('http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/{0}.txt'.format(name),url_data.content)[0])
			link_tmin = r_session.get(re.findall('http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmin/date/{0}.txt'.format(name),url_data.content)[0])
			link_tmean = r_session.get(re.findall('http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/{0}.txt'.format(name),url_data.content)[0])
			link_sunshine =  r_session.get(re.findall('http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Sunshine/date/{0}.txt'.format(name),url_data.content)[0])
			link_rainfall =  r_session.get(re.findall('http://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Rainfall/date/{0}.txt'.format(name),url_data.content)[0])
			links = [link_tmax.content,"{0}_TMAX".format(name)],[link_tmin.content,"{0}_TMIN".format(name)],[link_tmean.content,"{0}_TMEAN".format(name)],[link_sunshine.content,"{0}_SUNSHINE".format(name)],[link_rainfall.content,"{0}_RAINFALL".format(name)]
			for data in links:
				save_data(data[0],data[1],name)


# Save Data And Avoid Duplicate
def save_data(data,tag_code,country):
	tmp_f = StringIO.StringIO()
	tmp_f.write(data)
	data = tmp_f.getvalue().splitlines()
	for i,data in enumerate(data):
		if i>=8:
			refined_line_data = data.split(' ')
			refined_line_data = filter(len, refined_line_data)
			refined_line_data =  map(lambda x: unicodedata.normalize('NFKD', x).encode('ascii','ignore'), refined_line_data)
			refined_line_data =  map(lambda x: str.replace(x, "---",'0'), refined_line_data)
			if len(refined_line_data)==18:
				try:
					if country=="UK":
						country=1
					elif country=="England":
						country=2
					elif country=="Wales":
						country=3
					elif country=="Scotland":
						country=4

					obj, created = Weather.objects.get_or_create(country_code=int(country),tag_code=str(tag_code),year=int(refined_line_data[0]),january=float(refined_line_data[1])
						  ,february=float(refined_line_data[2]),march=float(refined_line_data[3]),april=float(refined_line_data[4])
						  ,may=float(refined_line_data[5]),june=float(refined_line_data[6]),july=float(refined_line_data[7])
						  ,august=float(refined_line_data[8]),september=float(refined_line_data[9]),october=float(refined_line_data[10])
						  ,november=float(refined_line_data[11]),december=float(refined_line_data[12]),winter=float(refined_line_data[13])
						  ,spring=float(refined_line_data[14]),summer=float(refined_line_data[15]),autumn=float(refined_line_data[16])
						  ,annual=float(refined_line_data[17]))

					# DEBUG CONSOLE MSG's
					print "*"*30
					print "--- DEBUG ---"
					print "ID : "+str(obj.id)
					print "Country : "+str(country)
					print "Tag Code : "+str(tag_code)
					print "DATA : "+str(refined_line_data)
					print "*"*30
					print "\n"
			
				except IntegrityError,e:
					print "Integrity Error : "+str(e.message)
					print "\n"

				except IndexError,e:
					print "Index Error Occured : Skipping..."
					print "\n"
					pass

			else:
				print "Message : Skipping Record, Malformed Data Format Found In File !"
				print "\n"

	tmp_f.close()
