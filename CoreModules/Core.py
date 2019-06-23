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
from SyntaxInsertSecurity import readTransformationsFromFileAndExecute
from StaticAnalysis import runBashCommand, getAllUsedDockerImages, runSnykOnImagesList 

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


def defineHostIP(host):
    if host == "*":
        #TODO adicionar "*", "N" como hosts genericos
        hostIP = "*"
        return hostIP

    if host.IP is None:
        if host.hostType == "internet":
            hostIP = "internet"
            return hostIP
        else:
            raise Exception('host without IP must be a internet access point')
    else:
        hostIP   = host.IP
        return hostIP   



def createRuleInput(hostList, hostConnList, network, outputFile="IPconnections.txt"):
    hostDict = createHostReverseDictionary(hostList)
    with open(outputFile, "w") as file:
        file.write("Subnet:{}\n".format(getDockerNetworkSubnet(network)[0]) )    
        #print(hostConnList)    
        for host in hostList:
            for conn in hostConnList[host.hostName]:
                firstHost     = hostDict[conn['firstHost']]
                secondHost    = hostDict[conn['secondHost']]
                try:
                    firstHostIP   = defineHostIP(firstHost)
                    secondHostIP  = defineHostIP(secondHost)
                except:
                    print("The Connection was ignored")
                    continue
                

                ports = conn['ports']
                if ports == "#":
                    if (secondHostIP != "*") and (secondHostIP != "internet"):
                        ports = ','.join(secondHost.ports)
                        if not ports:
                            print("Invalid use of # operator - Host {} does not have any port defined".format(secondHost))
                            print("The Connection was ignored")
                            continue
                    else:
                        ports = "*"
                file.write("{}:{}:{}\n".format(firstHostIP, ports, secondHostIP ))






def createSecuritySolutionsRouteRules(hostList, hostConnList, network, inputFile="ConfigRoute.toker", outputFile="createRoute.toker"):
    hostDict = createHostReverseDictionary(hostList)
    with open(inputFile, "r") as Inputfile: 
        with open(outputFile, "w") as Outputfile:  
            lines = Inputfile.readlines() 
            for line in lines:
                sline          = line.strip().split(":")
                sline          = [s.strip() for s in sline]
                firstHostName  = sline[0]
                secondHostName = sline[1]
                firstHost      = hostDict[firstHostName]
                secondHost     = hostDict[secondHostName]
                try:
                    firstHostIP   = defineHostIP(firstHost)
                    secondHostIP  = defineHostIP(secondHost)
                except:
                    print("The Connection was ignored")
                    continue
                if firstHostIP=="internet" or secondHostIP=="internet":
                    continue
                if firstHostIP=="*" or secondHostIP=="*":
                    continue                

                Outputfile.write('iptables -t filter -A INTERNETRULES -d {} -j ACCEPT'.format(firstHostIP))
                Outputfile.write('route add {} gw {} \n'.format(secondHostIP, firstHostIP))
                Outputfile.write('docker exec --privileged {} sh -c "route del default"\n'.format(secondHostName))    
                Outputfile.write('docker exec --privileged {} sh -c "route add default gw {}"\n'.format(secondHostName, firstHostIP))           





    
def runBashFile(filePath):
    subprocess.call(os.getcwd()+"/"+filePath, shell=True)









if __name__ == "__main__":
    hostList, connectionList = readSyntax("SyntaxExample3.txt")
    hostConnList = createHostConnList(hostList, connectionList)
    hostList, connectionList = readTransformationsFromFileAndExecute("TransformationsExample.txt",  "secureTopologic.toker", hostList, connectionList)
    hostList, connectionList = readSyntax("secureTopologic.toker")

    imageList = getAllUsedDockerImages(hostList)
    runSnykOnImagesList(imageList)
    
    network = createNetwork("TCCnet")
    createHosts(hostList)
    attachToNetwork(hostList, network)
    printDockerContainerIpList2()

    hostConnList = createHostConnList(hostList, connectionList)
    createRuleInput(hostList, hostConnList, network, outputFile="ipConnections.toker")
    createSecuritySolutionsRouteRules(hostList, hostConnList, network, inputFile="ConfigRoute.toker", outputFile="createRoute.sh")
 
    writeFilterRules("ipConnections.toker")
    runBashCommand("chmod 777 createRulesInIptables.sh")
    runBashFile("createRulesInIptables.sh")    

    runBashCommand("chmod 777 createRoute.sh")
    runBashFile("createRoute.sh")
    
    
    
    
    #print(minSubNetClassMaskIPv4(["192.168.1.1","192.169.0.2","192.168.0.3","192.168.0.4","192.168.0.5"]))


