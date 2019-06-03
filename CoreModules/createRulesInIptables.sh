#!/bin/bash 
iptables --policy FORWARD DROP 
iptables -t filter -N RULES 
iptables -t filter -N SUBNETS 
iptables -t filter -F RULES 
iptables -t filter -F SUBNETS 
iptables -t filter -I FORWARD 1 -j SUBNETS 
iptables -t filter -A SUBNETS -s 172.17.0.0/24 -d 172.17.0.0/24 -j RULES 
iptables -t filter -A RULES -p tcp --dport 80 -d 172.17.0.2 -j ACCEPT  
iptables -t filter -A RULES -p udp --dport 80 -d 172.17.0.2 -j ACCEPT  
iptables -t filter -A RULES -s 172.17.0.2 -m state --state ESTABLISHED,RELATED -j ACCEPT  
iptables -t filter -A RULES -s 172.17.0.6 -p tcp --dport 9999 -j ACCEPT  
iptables -t filter -A RULES -s 172.17.0.6 -p udp --dport 9999 -j ACCEPT  
iptables -t filter -A RULES -d 172.17.0.6 -m state --state ESTABLISHED,RELATED -j ACCEPT  
iptables -t filter -A RULES -s 172.17.0.3 -p tcp --dport 80 -d 172.17.0.2 -j ACCEPT  
iptables -t filter -A RULES -s 172.17.0.3 -p udp --dport 80 -d 172.17.0.2 -j ACCEPT  
iptables -t filter -A RULES -d 172.17.0.3 -s 172.17.0.2 -m state --state ESTABLISHED,RELATED -j ACCEPT  
iptables -t filter -A RULES -s 172.17.0.4 -d 172.17.0.2 -j ACCEPT  
iptables -t filter -A RULES -d 172.17.0.4 -s 172.17.0.2 -m state --state ESTABLISHED,RELATED -j ACCEPT  
iptables -A RULES -j DROP 
iptables -t filter -A SUBNETS -j RETURN 
