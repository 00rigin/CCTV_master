import http.server
import json
import socket
import sys
import requests
from urllib.parse import urlparse, parse_qs
from collections import OrderedDict
from description import jsonDescription
import numpy as np

sharedContext = []
global result
global es_res, de_res

result = '1'

# 2-year decision making algorithm
def collaboration_decision():

    list_edge = [x['Edgeserver']['netAddress'] for x in sharedContext] # edge ip list
    list_edge_cpu = [x['Edgeserver']['CPU']['cpuUsage'] for x in sharedContext]
    list_device = [] # Device ip list
    ai_context = sharedContext[0]['AI'] # ai context
    # cpu_avg = sum(list_edge_cpu,0.0)/len(list_edge_cpu)
    list_cpu_pred = [] # predicted cpu usage of edge server
    d_min = float('inf')
    c_min = float('inf')
    list_target = [] # Target name list

    for dat in sharedContext:
        for ip_ in dat['Device']['cameraIp']:
            list_device.append(ip_)
        for target_ in dat['Device']['Target']:
            list_target.append(target_)
    
    # calculate required resource of anal target
    # Find the predicted usage of cpu by target
    # for _tar_ in list_target:
        
    # list_cpu_pred.append()
    
    
    


# 1-year decision making algorithm
def decision():

    list_cpu = [float(sharedContext[0]['Edgeserver']['CPU']['cpuOccupancy']), float(sharedContext[1]['Edgeserver']['CPU']['cpuOccupancy'])]
    list_service = [5, 10, 15, 20]
    list_cameraip = sharedContext[0]['Device']['cameraIp']
    list_var = []
    list_servicevar = []
    list_servervar = []
    
    global result
    ternetAddress = None
    netaddress = None
    cameraIp = None
    
    for i in range(len(list_cpu)):
        
        if list_cpu[i]>70:
            print('70')
            for j in range(len(list_service)):
                list_cpu[i] = list_cpu[i] - list_service[j]
                for x in range(len(list_cpu)):
                    list_cpu[x] = list_cpu[x] + list_service[j]
                    cpu_variation = np.var(list_cpu)
                    list_var.insert(x, cpu_variation)
                    list_cpu[x] = list_cpu[x] - list_service[j]
                    list_servervar.insert(x, min(list_var))

                  
                list_servicevar.insert(j, min(list_var))
                selectService = list_service.index(min(list_service))
                selectServer = list_servervar.index(min(list_servervar))
                netaddress = sharedContext[selectServer]['Edgeserver']['netAddress']
                ternetAddress = sharedContext[i]['Edgeserver']['netAddress']
                cameraIp = sharedContext[i]['Device']['cameraIp'][selectService]

                    
                
            
    control = {
     "terresult" : ternetAddress,
     "result" : netaddress,
     "camera" : cameraIp
    }
    print(control)
    if ternetAddress == None or ternetAddress == result:
        return
    
    '''
    print(f'camera control result : {result} terent : {ternetAddress} compare: {ternetAddress == result}')
    '''
    result = ternetAddress

    resultShare(control)

def resultShare(data):
    params = data
    #requests.post('http://localhost:4000/api/post/collabo', json=params)
    requests.get('http://192.168.0.3:8000', params=params)
    requests.get('http://192.168.0.2:8000', params=params)


        

	
class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

   

    def close():
        http.server.shutdown(socket.SHUT_RDWR)
        http.server.close()
        
    def do_GET(self):
        self.response(200, 'hell')

    
        
    def response(self, status_code, body):
        self.send_response(status_code)

        parsed_path = urlparse(self.path)
        data = parse_qs(parsed_path.query)


        print(data)
        # edgeID = data['name'][0]
        # print(edgeID)
        # json.loads(parsed_path[4])

        self.send_header('Content-type', 'text/plain; charset-utf-8')
        self.end_headers()

        # self.wfile.write(body.encode('utf-8'))
        # for num in list:
    
        # return
        j = jsonDescription()
        
        j.description(sharedContext, data)


        ################ HJ DEV for test ##########################
        # Test env : 1 worker ES
        # DEV purpose : Deving collaboration decision algorithm
        if j.device_num_change_detector(data) is True:
            collaboration_decision()
        ###########################################################


        ## Monitoring page ##
        #requests.post('http://localhost:4000/api/post/context', json=sharedContext)
        
       
        
       
        ######### 1-year decision ###############
        # if len(sharedContext)>=2:
        #     print('sharedContext')
        #     print(sharedContext)
        #     decision()

host = socket.gethostname()
ADDRESS = '192.168.0.5', 8000


listener = http.server.HTTPServer(ADDRESS, HTTPRequestHandler)

listener.serve_forever()
