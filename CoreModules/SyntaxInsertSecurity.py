#!/bin/python3 
# -*- coding: utf-8 -*-
"""

@author: Felipe Balabanian
"""

from SyntaxProcess import readSyntax, createHostConnList, typeHostNameList, getMaxHostId, getMaxConnId, listConn, dictConn
from Definitions import Host


def insertAfter(type, image, hostList, connectionList):
    
    hostsThatHasThisTypeList = typeHostNameList(type, hostList)
    hostId = getMaxHostId(hostList)
    pairSnortInternet = dict()
    num = 0
    for hostT in hostsThatHasThisTypeList:
        num = num+1
        name = image+str(num)
        pairSnortInternet[hostT] = name
        hostId = hostId+1
        host = Host(hostId)
        host.hostName = name
        host.hostImage = image
        host.hostType = "SecuritySolution"
        host.hostVendor = image
        host.ports = "*"
        hostList.append(host)
    
    connId = getMaxConnId(connectionList)  
    connDict = dictConn(hostList, connectionList)

    with open("SecuritySolutionsConfigRoute.toker", "a") as file:
        for hostT in hostsThatHasThisTypeList:
            for conn in connectionList:
                if conn["firstHost"] == hostT:
                    t = conn["secondHost"]
                    #conn["secondHost"] = pairSnortInternet[hostT]
                    file.write(conn["firstHost"]+":"+pairSnortInternet[hostT]+"\n")
                    connId = connId+1
                    #connectionList.append({"id":connId, "firstHost":pairSnortInternet[hostT], "ports":conn["ports"], "secondHost":t })
                    file.write(pairSnortInternet[hostT]+":"+t+"\n")
                if conn["secondHost"] == hostT:
                    t = conn["firstHost"]
                    #conn["firstHost"] = pairSnortInternet[hostT]
                    file.write(conn["secondHost"]+":"+pairSnortInternet[hostT]+"\n")
                    connId = connId+1
                    #connectionList.append({"id":connId, "firstHost":t, "ports":conn["ports"], "secondHost":pairSnortInternet[hostT] })
                    file.write(t+":"+pairSnortInternet[hostT]+"\n")
            #print(connList)
    
    
        
    return hostList, connectionList
        


def insertBefore(type, image, hostList, connectionList):
    #TODO
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
        string = string + "{}:{}:{}\n".format(conn["firstHost"],conn["ports"],conn["secondHost"])
           
    with open(filePath, "w") as file: 
            file.write(string)      



def readTransformationsFromFileAndExecute(inputFilePath, outputFilePath, hostList, connectionList):
    f = open("ConfigRoute.toker", "w")
    #f.write("Connections:\n")
    f.close()
    with open(inputFilePath, "r") as file:
        lines = file.readlines() 
        for line in lines:
            sline = line.strip().split(":")
            #sline = [s.strip().casefold() for s in sline]
            #print(sline)
            command = sline[0].casefold()
            if not command:
                continue
            if command[0] == '-':
                continue
            if command == "insertafter":
                hostList, connectionList = insertAfter(sline[1], sline[2], hostList, connectionList)
            if command == "insertbefore":
                hostList, connectionList = insertBefore(sline[1], sline[2], hostList, connectionList)

    dataToText(outputFilePath, hostList, connectionList, "Auto Generated")
    return hostList, connectionList

        
if __name__ == "__main__":
    hostList, connectionList = readSyntax("SyntaxExample3.txt")
    readTransformationsFromFileAndExecute("TransformationsExample.txt", hostList, connectionList)
    #dataToText("secureTopologic.toker", hostList, connectionList, "Auto Generated")
        
