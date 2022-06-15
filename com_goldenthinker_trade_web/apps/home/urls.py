# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('processes_list',views.processes_list),
    path('stop_process',views.stop_processes),
    path('get_available_nodes',views.get_available_nodes),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
