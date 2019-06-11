#!/bin/python3 
# -*- coding: utf-8 -*-
"""
@author: Felipe Balabanian
"""

import re
import subprocess
import os.path

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
    return out.decode('utf-8')

def snykResultCache(imageName):
    with open("./SnykResults/"+imageName, "r") as file:
        result = file.read()
    return result
    

def runSnykOnImage(imageName):
    if os.path.exists("./SnykResults/"+imageName):
        result = snykResultCache(imageName)
    else:
        command = "snyk test --docker {}".format(imageName)
        result = runBashCommand(command)
        with open("./SnykResults/"+imageName, "w") as file:
            file.write(result)

    shortResult = re.findall("Docker image:.*?vulnerabilities\.", result, re.DOTALL)
    if not shortResult:
        shortResult = "{} - Short result not found on image scan. " \
                      "Please, see full report inside folder SnykResults.".format(imageName)
    else:
        shortResult = shortResult[0].replace("\n\n","\n")
    print(shortResult)
    

def runSnykOnImagesList(imagesList):
    for image in imagesList:
          print("")
          runSnykOnImage(image) 
    print("")

        
if __name__ == "__main__":
    from SyntaxProcess import readSyntax, createHostConnList
    hostList, connectionList = readSyntax("SyntaxExample3.txt")
    imageList = getAllUsedDockerImages(hostList)
    runSnykOnImagesList(imageList)







