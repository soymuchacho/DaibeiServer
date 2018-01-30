#########################################################################
# File Name: nginx_start.sh
# Author: guqi
# mail: guqi_282@126.com
# Created Time: Mon 29 Jan 2018 05:40:21 PM CST
#########################################################################
#!/bin/bash
echo '/usr/sbin/nginx -s stop'
/usr/sbin/nginx -s stop
echo '/usr/sbin/nginx -c /root/DaiBeiServer/nginx.conf '
/usr/sbin/nginx -c /root/DaiBeiServer/nginx.conf 
