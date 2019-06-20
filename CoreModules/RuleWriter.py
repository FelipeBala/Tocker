# -*- coding: utf-8 -*-
"""
Created on Mon May 27 20:01:06 2019

@author: Bala
"""
#!/bin/python3 


def writeFilterRules(filePath):
    with open(filePath, "r") as file:
        lines = file.readlines()
        with open("createRulesInIptables.sh", "w") as outfile:
            outfile.write("#!/bin/bash \n")
            outfile.write("iptables --policy FORWARD DROP \n")    
            outfile.write("iptables -t filter -N RULES \n")
            outfile.write("iptables -t filter -N SUBNETS \n")
            outfile.write("iptables -t filter -F RULES \n")
            outfile.write("iptables -t filter -F SUBNETS \n")
            outfile.write("iptables -t filter -D FORWARD -j SUBNETS \n")
            outfile.write("iptables -t filter -I FORWARD 1 -j SUBNETS \n")
            
            for line in lines:
                temp = line.strip().split(':')
                if temp[0].strip() == "Subnet":
                    subnet = temp[1]
                    outfile.write("iptables -t filter -A SUBNETS -s {} -d {} -j RULES \n".format(subnet,subnet))
                    continue
                else:                 
                    source  = temp[0].strip()
                    ports   = temp[1].strip()
                    destine = temp[2].strip()
                
                rule = "iptables -t filter -A RULES "
                ruleBack = rule
                                
                if source != "*":
                    rule     = rule + "-s {} ".format(source)                 
                    ruleBack = ruleBack + "-d {} ".format(source)
                if ports != "*":
                    if len(ports.split(",")) > 1:
                        #TODO:restringir a 15 portas no máximo.
                        rule = rule + "-p tcp -m multiport --dports {} ".format(ports)
                    else:
                        rule = rule + "-p tcp --dport {} ".format(ports)

                if destine != "*":
                    rule     = rule + "-d {} ".format(destine)
                    ruleBack = ruleBack + "-s {} ".format(destine)
                    
                rule     = rule + "-j ACCEPT "
                ruleBack = ruleBack + "-m state --state ESTABLISHED,RELATED -j ACCEPT "
                outfile.write(rule+" \n")
                
                if rule.find("-p tcp") > -1:
                    ruleUDP = rule.replace("-p tcp", "-p udp") 
                    outfile.write(ruleUDP+" \n")

                outfile.write(ruleBack+" \n")
                
            outfile.write("iptables -A RULES -j DROP \n")
            outfile.write("iptables -t filter -A SUBNETS -j RETURN \n")

if __name__ == "__main__":
    writeFilterRules("RuleExample.txt")
            
