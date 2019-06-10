#!/bin/python3 
# -*- coding: utf-8 -*-
"""
@author: Felipe Balabanian
"""


def getAllUsedDockerImages(hostList):
    imageList = set()
    for host in hostList:
        if host.hostImage is not None:
            imageList.add(host.hostImage)
    return imageList
        

def         
        
if __name__ == "__main__":
    from SyntaxProcess import readSyntax, createHostConnList
    hostList, connectionList = readSyntax("SyntaxExample3.txt")
    imageList = getAllUsedDockerImages(hostList)
    print(imageList)