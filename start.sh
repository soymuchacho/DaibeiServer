#########################################################################
# File Name: start.sh
# Author: guqi
# mail: guqi_282@126.com
# Created Time: Tue 08 Aug 2017 11:49:53 AM CST
#########################################################################
#!/bin/bash

ulimit -c unlimited

python manage.py runserver 0.0.0.0:80 > /dev/null 2>&1 &

