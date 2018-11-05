# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    return render(request, 'page/index.html', {})

def traceroute(request):
    if request.is_ajax():
        input_traceroute = request.POST.get('input_traceroute')
        quantidade_saltos_trace = request.POST.get('quantidade_saltos_trace')
        print(input_traceroute)
        print(quantidade_saltos_trace)

        context = {
 	    	'input_traceroute': input_traceroute,
 	    	'quantidade_saltos_trace': quantidade_saltos_trace,
 	    }

        return render(request, "page/resultado_trace.html", context)
    #return render(request,"page/resultado.html")

def ping(request):
    if request.is_ajax():
        input_ping = request.POST.get('input_ping')
        quantidade_saltos_ping = request.POST.get('quantidade_saltos_ping')
        print(input_ping)
        print(quantidade_saltos_ping)

        context = {
 	    	'input_ping': input_ping,
 	    	'quantidade_saltos_ping': quantidade_saltos_ping,
 	    }
 
        return render(request, "page/resultado_ping.html", context)
    #return render(request,"page/resultado.html")