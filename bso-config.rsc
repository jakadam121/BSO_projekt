# 2026-05-05 20:34:09 by RouterOS 7.22.1
# system id = swQu2HN7cvG
#
/interface bridge
add name=docker-bridge
/interface ethernet
set [ find default-name=ether1 ] disable-running-check=no
set [ find default-name=ether2 ] disable-running-check=no
/interface veth
add address=172.17.0.2/24 container-mac-address=5A:8F:A7:1E:1C:80 dhcp=no \
    gateway=172.17.0.1 gateway6="" mac-address=5A:8F:A7:1E:1C:7F name=veth1
/container
add env="SCAN_SUBNET=192.168.40.0/24,SCAN_TYPE=quick,EMAIL_TO=jakadam121@gmail\
    .com,SMTP_USER=jakadam121@gmail.com,SMTP_PASS=eigwbklxeklkvnjz,REPORT_FORM\
    AT=html" interface=veth1 layer-dir="" logging=yes name=\
    bso-scanner-v2:latest remote-image=sadjgasjdg/bso-scanner-v2:latest \
    root-dir=/tmp/scanner workdir=/app
/container config
set registry-url=https://registry-1.docker.io tmpdir=/tmp
/container mounts
add dst=/results list=nmap-output src=/nmap-results
/interface bridge port
add bridge=docker-bridge interface=veth1
/ip address
add address=192.168.40.2/24 interface=ether1 network=192.168.40.0
add address=172.17.0.1/24 interface=docker-bridge network=172.17.0.0
/ip dhcp-client
add interface=ether1 name=client1
add interface=ether2 name=client2
/ip firewall nat
add action=masquerade chain=srcnat src-address=172.17.0.0/24
/system scheduler
add interval=1d name=bso-scan on-event=\
    "/container/start [find tag~\"bso-scanner\"]" policy=\
    ftp,reboot,read,write,policy,test,password,sniff,sensitive,romon \
    start-date=2026-05-05 start-time=20:31:20
