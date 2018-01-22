#!/usr/bin/env python

import json
import requests
import sys
import warnings

warnings.filterwarnings("ignore")

def gettoken(ip,port,username,password):
    
    requests.packages.urllib3.disable_warnings()

    headers={ 'Content-Type':'application/json' }
   
    payload = { 'username' : username, "password" : password}
    response = requests.post("https://%s:%s/vsm/authenticate" % (ip, port),
                             data=json.dumps(payload),
                             headers=headers,
                             verify=False,                      # disable SSH certificate verification
                             timeout=30)
    
    if response.status_code == 200:
        return response.json()['token']
    
    else:
        print "Could not get token for authentication, error code %s" % (response.status_code)
        sys.exit(9)
    
   
def getdata(ip,port,token,url):
    token = token.strip()
    requests.packages.urllib3.disable_warnings()
    headers={ 'Content-Type':'application/json', 'CustomToken' : token }
    #print "https://%s:%s%s" % (ip, port,url)

    response = requests.get("https://%s:%s%s" % (ip, port,url),
                             headers=headers,
                             verify=False,                      # disable SSH certificate verification
                             timeout=30)
    
    if response.status_code == 200:
        return response.json()
    
    else:
        print "Could not get %s, error code %s" % (url,response.status_code)
        sys.exit(9)

def main(argv):
    
    protocol = 'https'
    port     = 8443
    ip       = '10.90.56.84'
    username = 'administrator'
    password = 'CopAdmin1'
    methods  = ('resources','users')
    final    = []
    
    token = gettoken(ip,port,username,password)

    for m in methods:
        data = getdata(ip,port,token,"/vsm/%s" % m)
        for d in data:
            d['apicall'] = m
            
        final.extend(data)
    
    for key in final:
        for value in key:
            print value + "," + str(key[value])

if __name__ == '__main__':
    main(sys.argv[1:])
