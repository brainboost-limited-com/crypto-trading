from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render
import re

def home(request):
    return render(
        request,
        'com_goldenthinker_trade_web/index.html'
        )

def com_goldenthinker_trade_web(request,name):
    return render(
        request,
        'html/' + str(name)
        )