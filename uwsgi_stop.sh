#########################################################################
# File Name: uwsgi_start.sh
# Author: guqi
# mail: guqi_282@126.com
# Created Time: Mon 29 Jan 2018 05:31:27 PM CST
#########################################################################
#!/bin/sh  
NAME="uwsgi"  
if [ ! -n "$NAME" ];then  
	echo "no arguments"  
	exit;  
fi  

echo $NAME  
ID=`ps -ef | grep "$NAME" | grep -v "$0" | grep -v "grep" | awk '{print $2}'`  
echo $ID  
echo "################################################"  
for id in $ID  
do  
	kill -9 $id  
	echo "kill $id"  
done  
echo  "################################################"  
