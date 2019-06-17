#!/bin/python3 
# -*- coding: utf-8 -*-
"""

@author: Felipe Balabanian
"""

from SyntaxProcess import readSyntax, createHostConnList, internetHostNameList, getMaxHostId, getMaxConnId, listConn, dictConn
from Definitions import Host


def SnortInsert(hostList, connectionList):
    
    
    internetList = internetHostNameList(hostList)
    hostId = getMaxHostId(hostList)
    pairSnortInternet = dict()
    num = 0
    for internetHost in internetList:
        num = num+1
        name = "Snort"+str(num)
        pairSnortInternet[internetHost] = name
        hostId = hostId+1
        host = Host(hostId)
        host.hostName = name
        host.hostImage = "Snort"
        host.hostType = "Monitor"
        host.hostVendor = "Snort"
        host.ports = "*"
        hostList.append(host)
    
    connId = getMaxConnId(connectionList)  
    connDict = dictConn(hostList, connectionList)


    for internet in internetList:
        for conn in connectionList:
            if conn["firstHost"] == internet:
                t = conn["secondtHost"]
                conn["secondtHost"] = pairSnortInternet[internet]
                connId = connId+1
                connectionList.append({"id":connId, "firstHost":pairSnortInternet[internet], "ports":conn["ports"], "secondtHost":t })
            if conn["secondtHost"] == internet:
                t = conn["firstHost"]
                conn["firstHost"] = pairSnortInternet[internet]
                connId = connId+1
                connectionList.append({"id":connId, "firstHost":t, "ports":conn["ports"], "secondtHost":pairSnortInternet[internet] })
        
        #print(connList)
    
    
        
    return hostList, connectionList
        








def dataToText(filePath, hostList, connectionList, msg=None):
    if msg is not None:
        string = "---- "+msg+"\n"
    else:
        string = "\n"
    
    for host in hostList:
        string = string + "\n"
        string = string + "HostName:{}\n".format(host.hostName)
        if host.hostType is not None:
            string = string + "HostType:{}\n".format(host.hostType)
        if host.hostImage is not None:
            string = string + "HostImage:{}\n".format(host.hostImage)
        if host.hostVendor is not None:
            string = string + "HostVendor:{}\n".format(host.hostVendor)
        if host.ports:
            string = string + "Ports:{}\n".format(','.join(host.ports))            
        if host.IP is not None:
            string = string + "IP:{}\n".format(host.IP)             
            
    string = string + "\nConnections:\n" 
    
    for conn in connectionList:   
        string = string + "{}:{}:{}\n".format(conn["firstHost"],conn["ports"],conn["secondtHost"])
           
    with open(filePath, "w") as file: 
            file.write(string)      






        
if __name__ == "__main__":
    hostList, connectionList = readSyntax("SyntaxExample3.txt")
    hostList, connectionList = SnortInsert(hostList, connectionList)
    dataToText("secureTopologic.toker", hostList, connectionList, "Auto Generated")
        