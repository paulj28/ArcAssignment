import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import pandas as pd
import json
import ast
import time


al=time.time()
if len(sys.argv)==1:
    print('Enter valid arg!')
    exit(0)

baseReq='http://localhost:8000/'
services = ['RouteService', 'AuthService', 'MonitorService', 'FinService', 'TimeService',
    'GeoService', 'TicketService', 'FlightService', 'IdService', 'UserService', 'GroupService']

def updateDF(url, ip):
    a=requests.get(url, verify=False)
    ipdata=json.loads(a.text)
    #print(type(ipdata))
    data={'ip': ip, 'cpu': int(ipdata['cpu'].replace('%', '')), 'memory': int(ipdata['memory'].replace('%', '')), 'service': ipdata['service']}
    if data['cpu']>80 or data['memory']>80:
        data['status']='Unhealthy'
    else:
        data['status']='Healthy'
    return data

def runner(iplist):
    service_info={'RouteService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]}, 'AuthService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]},
                  'MonitorService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]}, 'FinService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]},
                  'TimeService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]}, 'GeoService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]},
                  'TicketService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]}, 'FlightService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]},
                  'IdService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]}, 'UserService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]},
                  'GroupService': {'count':0, 'cpusum':0, 'memsum':0, 'healthy':0, 'unhealthy':0, 'files':[]}}
    threads=[]
    with ThreadPoolExecutor(max_workers=8) as executor:
        for ip in iplist:
            url=baseReq+ip
            threads.append(executor.submit(updateDF, url, ip))

        for task in as_completed(threads):
            k=task.result()
            service_info[k['service']]['count']+=1
            service_info[k['service']]['cpusum']+=k['cpu']
            service_info[k['service']]['memsum']+=k['memory']
            service_info[k['service']]['files'].append({'ip': ip, 'memory': k['memory'], 'cpu': k['cpu'], 'status':k['status']})

    with open('serverInfo.json', 'w') as f:
        json.dump(service_info, f)

    return service_info

if sys.argv[1]=='--update':
    a=requests.get(baseReq+'servers')
    ip_list=ast.literal_eval(a.text)
    runner(ip_list)
    exit(0)

res={}
with open('serverInfo.json', 'r') as f:
    res=json.load(f)

if sys.argv[1]=='--print':
    for k,v in res.items():
        for v1 in v['files']:
            print(v1['ip'], v1['cpu'], v1['memory'], k, v1['status'])
elif sys.argv[1]=='--avg':
    for k,v in res.items():
        print(k,' CPU   : ', v['cpusum']/v['count'])
        print(k,' Memory: ', v['memsum']/v['count'])
elif sys.argv[1]=='--study':
    if(sys.argv[2] in services):
        while(True):
            init_sec=time.time()
            a=requests.get(baseReq+'servers')
            ip_list=ast.literal_eval(a.text)
            res=runner(ip_list)
            fls=res[sys.argv[2]]['files']
            print(sys.argv[2], ' File Info :')
            for f in fls:
                print(f['ip'], ' -  CPU : ', f['cpu'], '    Memory : ', f['memory'], '    Status : ', f['status'])
            print('\n ----------------------------------------------------------------- \n')
            fin_sec=time.time()
            print('Time taken :', fin_sec-init_sec)
            time.sleep(10)

for k,v in res.items():
    if v['healthy']<2:
        print('ALERT! - ', k, ' has less than 2 healthy systems!!!!')
