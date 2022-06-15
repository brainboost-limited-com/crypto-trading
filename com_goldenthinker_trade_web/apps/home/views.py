# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


import subprocess

def execute(command):
    #try:
    batcmd=command
    return str(subprocess.check_output(batcmd, shell=True,text=True))
    #except:
    #    Logger.log("Error executing commmand :" + str(command),telegram=True)





@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def processes_list(request):
    
    processes_table_html =   '''
            <tr class="unread">
                <td><img class="rounded-circle" style="width:40px;" src="/static/assets/images/process.png" alt="activity-user"></td>
                <td>
                    <h6''' + ''' class="mb-1">Process Name</h6>
                </td>
                <td>
                    Node
                </td>
                <td>
                    <h6>PID</h6>''' + '''
                </td>
                <td>
                    <h6>Status</h6>''' + '''
                </td>
            </tr>
        '''
    services = Utils.execute('ls com_goldenthinker_trade_install/ec2/etc/systemd/system/goldenthinker_services/*.service').split('\n')
    
    
    def process_status(name):
        if len(name)>0:
            pline_info = Utils.execute('ps aux|grep ' + name)
            if len(pline_info) > 0:
                parts = pline_info.split(' ')
                return str(parts[4])
            else:
                return "Off"
        else:
            return "Cannot find process " + name
    
    
    for s in services:
        
        process_name = s.split('/')[-1]
        if len(process_name)>0:
            pstatus = process_status(process_name) 
            if len(pstatus)>0:
                process_control_buttons = '''<td><a href="/process_stop/''' +  pstatus + '''" class="label theme-bg2 text-white f-12">Stop</a>'''+'''<a href="/view_log_tail/''' + pstatus + '''" class="label theme-bg text-white f-12">Log</a>'''
            else:
                process_control_buttons = '''<a href="/process_start/''' + pstatus + '''" class="label theme-bg text-white f-12">Start</a>'''
            single_row = ''' 
                <tr class="unread">
                    <td><img class="rounded-circle" style="width:40px;" src="/static/assets/images/process.png" alt="activity-user"></td>
                    <td>
                        <h6''' + ''' class="mb-1">''' + process_name + '''</h6>
                    </td>
                    <td>
                        <h6''' + ''' class="mb-1">''' + "Node" + '''</h6>
                    </td>                    
                    <td>
                        <h6>''' + pstatus + '''</h6>''' + '''
                    </td>''' + process_control_buttons + '''</td>
                
                </tr>
                '''
            processes_table_html = processes_table_html + single_row
    return HttpResponse(processes_table_html)
    
    
    
@login_required(login_url="/login/")
def stop_processes(request,pid):
    execute('kill -9 ' + pid)
    return None

def server_space(request):
    space = Utils.execute('df')
    table = []
    for each_line in space:
        line_parts = each_line.split(' ')
        table.append(line_parts)
        free_space = free_space + int(line_parts[3])/1024/1024
        used_space = used_space + int(line_parts[2])/1024/1024
    space_calculation = []
    return table
     

def get_available_nodes(request):
    config_file = open(r"/Users/goldenthinker/Desktop/OneDrive/Projects/crypto_trading/global.config", "r")
    config_file_lines = config_file.readlines()
    table = []
    for each_line in config_file_lines:
        line_parts = each_line.split(' ')
        table.append(line_parts)
    return table
        