iptables -t filter -F RULES 
iptables -t filter -F SUBNETS
iptables -t filter -D FORWARD -j SUBNETS
iptables -t filter -X RULES 
iptables -t filter -X SUBNETS
