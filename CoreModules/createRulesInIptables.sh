#!/bin/bash 
iptables --policy FORWARD DROP 
iptables -t filter -N RULES 
iptables -t filter -N INTERNETRULES 
iptables -t filter -N SUBNETS 
iptables -t filter -F RULES 
iptables -t filter -F INTERNETRULES 
iptables -t filter -F SUBNETS 
iptables -t filter -D FORWARD -j SUBNETS 
iptables -t filter -I FORWARD 1 -j SUBNETS 
iptables -t filter -A SUBNETS -s 172.18.0.0/16 -d 172.18.0.0/16 -j RULES 
iptables -t filter -A SUBNETS -s 172.18.0.0/16 -j INTERNETRULES 
iptables -t filter -A SUBNETS -d 172.18.0.0/16 -j INTERNETRULES 
iptables -t filter -A INTERNETRULES -p tcp --dport 80 -d 172.18.0.2 -j ACCEPT  
iptables -t filter -A INTERNETRULES -p udp --dport 80 -d 172.18.0.2 -j ACCEPT  
iptables -t filter -A INTERNETRULES -s 172.18.0.2 -m state --state ESTABLISHED,RELATED -j ACCEPT  
iptables -t filter -A INTERNETRULES -p tcp --dport 80 -d 172.18.0.3 -j ACCEPT  
iptables -t filter -A INTERNETRULES -p udp --dport 80 -d 172.18.0.3 -j ACCEPT  
iptables -t filter -A INTERNETRULES -s 172.18.0.3 -m state --state ESTABLISHED,RELATED -j ACCEPT  
iptables -t filter -A RULES -s 172.18.0.3 -p tcp -m multiport --dports 80,8080 -d 172.18.0.2 -j ACCEPT  
iptables -t filter -A RULES -s 172.18.0.3 -p udp -m multiport --dports 80,8080 -d 172.18.0.2 -j ACCEPT  
iptables -t filter -A RULES -d 172.18.0.3 -s 172.18.0.2 -m state --state ESTABLISHED,RELATED -j ACCEPT  
iptables -t filter -A RULES -s 172.18.0.3 -d 172.18.0.4 -j ACCEPT  
iptables -t filter -A RULES -d 172.18.0.3 -s 172.18.0.4 -m state --state ESTABLISHED,RELATED -j ACCEPT  
iptables -A RULES -j DROP 
iptables -t filter -A INTERNETRULES -j DROP 
iptables -t filter -A SUBNETS -j RETURN 
