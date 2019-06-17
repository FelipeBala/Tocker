#!/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Bala
"""

import subprocess 
import os 

from SyntaxProcess import readSyntax, createHostConnList
from DockerInterface import *  
from RuleWriter import writeFilterRules

def createNetwork(networkName):
     network = createDockerNetwork(networkName)
     if network == None:
         network = getDockerNetwork(networkName)
     print("Subnet created: " + str(getDockerNetworkSubnet(network)))
     return network

def createHosts(hostList):
    for host in hostList:
        if host.hostType == "internet":
            #TODO: preencher depois
            continue
        
        name = host.hostName
        imag = host.hostImage
        if imag == None:
            print("No image defined - Skipping container: "+ name)
            continue
        keep = host.keep            
        try:
            host.containerID = createDockerContainer(name=name, image=imag, keep=keep)    
        except:
            pass


def attachToNetwork(hostList, network):
    for host in hostList:
        if host.IP is not None and host.containerID is not None:
            attachDockerNetworkToContainer(host.containerID, network=network, ip=host.IP)
            host.IP = getDockerContainerIP(host.containerID)[0]
            print("Attaching {} to {}".format(host.hostName, host.IP))            
    for host in hostList:
        if host.IP is None and host.containerID is not None:
            attachDockerNetworkToContainer(container=host.containerID, network=network)
            host.IP = getDockerContainerIP(host.containerID)[0]
            print("Attaching {} to {}".format(host.hostName, host.IP))

def createHostReverseDictionary(hostList):
    reverseDictionary = {}
    for host in hostList:
        reverseDictionary[host.hostName] = host    
    return reverseDictionary

def createRuleInput(hostList, hostConnList, network, outputFile="IPconnections.txt"):
    hostDict = createHostReverseDictionary(hostList)
    with open(outputFile, "w") as file:
        file.write("Subnet:{}\n".format(getDockerNetworkSubnet(network)[0]) )        
        for host in hostList:
            for conn in hostConnList[host.hostName]:
                firstHost     = hostDict[conn['firstHost']].IP
                secondtHost   = hostDict[conn['secondtHost']].IP
                firstHost     = ("*", firstHost)[firstHost is not None]
                secondtHost   = ("*", secondtHost)[secondtHost is not None]
                ports = conn['ports']
                if ports == "#":
                    if (hostDict[conn['secondtHost']] is not None) and secondtHost != "*":
                        ports = ','.join(hostDict[conn['secondtHost']].ports)
                        if not ports:
                            print("Invalid use of # operator - Host {} does not have any port defined".format(conn['secondtHost']))
                            print("The Connection was ignored")
                            continue
                    else:
                        port = "*"
                file.write("{}:{}:{}\n".format(firstHost, ports, secondtHost ))
            
    
def runBashFile(filePath):
    subprocess.call(os.getcwd()+"/"+filePath, shell=True)









if __name__ == "__main__":
    hostList, connectionList = readSyntax("SyntaxExample3.txt")
    hostConnList = createHostConnList(hostList, connectionList)
    network = createNetwork("TCCnet")
    createHosts(hostList)
    attachToNetwork(hostList, network)
    printDockerContainerIpList()
    createRuleInput(hostList, hostConnList, network, outputFile="ipConnections.toker")
    writeFilterRules("ipConnections.toker")
    runBashFile("createRulesInIptables.sh")
    
    
    
    
    
    #print(minSubNetClassMaskIPv4(["192.168.1.1","192.169.0.2","192.168.0.3","192.168.0.4","192.168.0.5"]))


