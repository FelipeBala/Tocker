#!/bin/python3 
# -*- coding: utf-8 -*-
"""

@author: Felipe Balabanian
"""

from Definitions import Host, limit


def readSyntax(filePath):
    with open(filePath, "r") as file: 
        lines = file.readlines() 
        hostId = 0
        connId = 0
        hostList = []
        connectionList = []
        flagConnections = False
        for line in lines:
            sline = line.strip().split(":")
            #print(sline)
            if not flagConnections:
                
                if sline[0].casefold() == "hostname":
                    try:
                        if sline[1] == '':
                            raise Exception('HostName without name')
                    except :
                            raise Exception('HostName without name')                
                    hostId = hostId+1
                    host = Host(hostId)
                    host.hostName = sline[1].strip()
                    hostList.append(host)
                
                if len(hostList) <= 0:
                    raise Exception('HostName not definied') 

                if sline[0].casefold() == "hostimage":
                    hostList[-1].hostImage = sline[1].strip().casefold()
                       
                if sline[0].casefold() == "hosttype":
                    hostList[-1].hostType = sline[1].strip().casefold()
                    
                if sline[0].casefold() == "hostvendor":
                    hostList[-1].hostVendor = sline[1].strip().casefold()

                if sline[0].casefold() == "hostip":
                    hostList[-1].IP = sline[1].strip().casefold()

                if sline[0].casefold() == "keep":
                    hostList[-1].keep = True #TODO criar um analisador estático para diferenciar o True e False                  
                    
                if sline[0].casefold() == "ports":
                    ports = sline[1].split(',')
                    for port in ports:
                        hostList[-1].ports.append(port.strip())
            
                if sline[0].casefold() == "connections":
                    flagConnections = True
                    
            else:
                if len(sline) == 3 and sline[0] != '' and sline[0][0] != '-':
                    connId = connId+1
                    connectionList.append({"id":connId, "firstHost":sline[0].strip(), "ports":sline[1].strip(), "secondtHost":sline[2].strip() })
        
        #print([i["secondtHost"] for i in connectionList])
        return hostList, connectionList



def internetHostNameList(hostList):
    return [ a.hostname for a in hostList if a.hostType == "internet" ]

def getHostNameList(hostList):
    return [ a.hostname for a in hostList ]

def createHostConnList(hostList, connectionList):    
    host = {}
    for hostl in hostList:
        #print(hostl.hostname)
        host[hostl.hostName] = [ a for a in connectionList if (a['firstHost'] == hostl.hostName) ]
    #print([host[h.hostname]["conn"] for h in hostList])
    return host     
    

def minSubNetClassMaskIPv4(ipList):
    IPfield = []
    for ip in ipList:
        field = ip.strip().split(".")
        if len(field)!= 4:
            raise Exception('IPv4 must have 4 fields')
        IPfield.append(field)
        
    print(IPfield)
    mask = [True,True,True,True]
    for i in range(0,4):
        mask[i] = len(set([a[i] for a in IPfield]))==1
        if not mask[i]:
            t = i*8
            return t
        

        

    
if __name__ == "__main__":
    hostList, connectionList = readSyntax("SyntaxExample3.txt")
    hostConnList = createHostConnList(hostList, connectionList)
    print(hostConnList['W1'])

















    
    