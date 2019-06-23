iptables -t filter -I RULES 1 -s 172.18.0.1 -d 172.18.0.2 -j ACCEPT 
iptables -t filter -I RULES 1 -s 172.18.0.2 -d 172.18.0.1 -j ACCEPT 
docker exec --privileged ping1 sh -c "route add 172.18.0.1 gw 172.18.0.1"
docker exec --privileged ping1 sh -c "route add 172.18.0.2 gw 172.18.0.2"
docker exec --privileged W1 sh -c "route del default"
docker exec --privileged W1 sh -c "route add default gw 172.18.0.5"
docker exec --privileged W1 sh -c "route add 172.18.0.1 gw 172.18.0.5"
iptables -t filter -I RULES 1 -s 172.18.0.1 -d 172.18.0.3 -j ACCEPT 
iptables -t filter -I RULES 1 -s 172.18.0.3 -d 172.18.0.1 -j ACCEPT 
docker exec --privileged ping1 sh -c "route add 172.18.0.1 gw 172.18.0.1"
docker exec --privileged ping1 sh -c "route add 172.18.0.3 gw 172.18.0.3"
docker exec --privileged H1 sh -c "route del default"
docker exec --privileged H1 sh -c "route add default gw 172.18.0.5"
docker exec --privileged H1 sh -c "route add 172.18.0.1 gw 172.18.0.5"
