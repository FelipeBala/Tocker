#!/bin/python3 
# -*- coding: utf-8 -*-
"""
@author: Felipe Balabanian
"""

import re
import subprocess

def getAllUsedDockerImages(hostList):
    imageList = set()
    for host in hostList:
        if host.hostImage is not None:
            imageList.add(host.hostImage)
    return imageList


def runBashCommand(command):
    commandWithArgs = [i for i in command.split(" ") if i != '']
    process = subprocess.Popen(commandWithArgs, stdout=subprocess.PIPE)
    out, err = process.communicate() 
    return out.decode('ascii')

def runSnykOnImage(imageName):
    command = "snyk test --docker {}".format(imageName)
    result = runBashCommand(command)
    re.search(r"Organisation:*.vulnerabilities.", str)
    
    
    with open("/SnikResult/"+imageName, "w") as file:
        file.write(result)
        
if __name__ == "__main__":
    from SyntaxProcess import readSyntax, createHostConnList
    hostList, connectionList = readSyntax("SyntaxExample3.txt")
    imageList = getAllUsedDockerImages(hostList)
    print(imageList)
    print(runBashCommand("ls -a; ls -a"))