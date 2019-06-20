#!/bin/python3 
# -*- coding: utf-8 -*-
"""

@author: Felipe Balabalabanian
"""

import docker


from Definitions import Host 


def createDockerNetwork(networkName, ipam_pool=None):
    client = docker.from_env()
    networkList = client.networks.list() 
    existnetworkName = any([True for i in networkList if i.name == networkName ]) 
    if existnetworkName:
        print("Network already exist")
        return None
    if ipam_pool is not None:
        ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
        network = client.networks.create(networkName, driver="bridge", ipam=ipam_config) 
    else:
        network = client.networks.create(networkName, driver="bridge")
    return network

def getDockerNetwork(networkName):
    client = docker.from_env()
    network = client.networks.list(names=[networkName]) 
    if 0<len(network):
        return network[0]
    

def getDockerNetworkIPAM(network):
    network.reload()
    return network.attrs['IPAM']['Config']

def getDockerNetworkSubnet(network):
    subnets = getDockerNetworkIPAM(network)
    return [i['Subnet'] for i in subnets]

def attachDockerNetworkToContainer(container, network, ip=None):
    try:
        if 'bridge' in getDockerContainerNetworks(container):
            client = docker.from_env()
            client.networks.get("bridge").disconnect(container)
        network.connect(container, ipv4_address=ip)
    except:
        pass
    return getDockerContainerIP(container)





def createDockerContainer(name, image, network='bridge', keep=False, autoremove=True):
    client = docker.from_env()
    try:
        container = client.containers.get(name)        
        print("Found a continer with the same name: "+ name)
        
    except docker.errors.NotFound:
        container = client.containers.run(name=name, 
                                          image=image , 
                                          network=network, 
                                          stdin_open=keep,
                                          labels=["TCC"], 
                                          detach=True, 
                                          remove=autoremove, 
                                          auto_remove=autoremove)
            
    return container
    
def getDockerContainer(name):
    client = docker.from_env()
    return client.containers.get(name)

def getDockerContainerIP(container):
    return [ip for _,ip in getDockerContainerNetworkAndIP(container)]

def getDockerContainerNetworkAndIP(container):
    container.reload()
    networks = container.attrs['NetworkSettings']['Networks']
    return [ (net,value['IPAddress']) for net,value in networks.items()]

def printDockerContainerIpList():
    containerList = getDockerContainerList()
    print("-----------------------------------------------")
    print("Listing container`s (network, IP)")
    print("-----------------------------------------------")
    for container in containerList:
        print("Container: "+getDockerContainerName(container))
        [ print(i) for i in getDockerContainerNetworkAndIP(container) ]
        print("-----------------------------------------------")

def printDockerContainerIpList2():
    containerList = getDockerContainerList()
    print("-----------------------------------------------")
    print("Listing container`s (network, IP)")
    print("-----------------------------------------------")
    for container in containerList:
        s = ",".join([str(i) for i in getDockerContainerNetworkAndIP(container)])
        print(getDockerContainerName(container) + " " + str(s))


def getDockerContainerNetworks(container):
    container.reload()
    return [key for key in container.attrs['NetworkSettings']['Networks'] ]
    
def getDockerContainerList(label=None):
    client = docker.from_env()
    if label is not None:
        containerList = client.containers.list(filter={'label':label})
    else:
        containerList = client.containers.list()
    return containerList

def getDockerContainersIDList(label=None): 
    containerList = getDockerContainerList(label)
    containerIdList = [ i.id for i in containerList]
    return containerIdList
 
def getDockerContainerName(container):
    container.reload()
    name = container.attrs['Name']
    return name.replace("/","")





if __name__ == "__main__":
     containerList = getDockerContainerList()
     print([a.name for a in containerList])
     network = createDockerNetwork("testeNet")
     if network == None:
         network = getDockerNetwork("testeNet")
     print(getDockerNetworkSubnet(network))
     container = createDockerContainer(name="teste", image="ping", keep=True)
     container = getDockerContainer("teste")
     print(attachDockerNetworkToContainer(container,network))
     
     
     
     
     
     # from DockerInterface import *
     # a = getDockerContainer("teste")
