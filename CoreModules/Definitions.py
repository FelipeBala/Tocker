# -*- coding: utf-8 -*-
"""

@author: Bala
"""

class Host:
  def __init__(self, hostId):
    self.id = hostId
    self.hostName = None
    self.hostImage = None        #Docker Image Name    
    self.hostType = None
    self.hostVendor = None
    self.keep = True
    self.ports = []
    self.IP = None
    self.subnet = None
    self.containerID = None

def limit(value,minV,maxV):
    return max(  min(value,minV),  maxV)