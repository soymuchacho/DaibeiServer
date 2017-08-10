#########################################################################
# File Name: sql.sh
# Author: guqi
# mail: guqi_282@126.com
# Created Time: Wed 09 Aug 2017 04:53:16 PM CST
#########################################################################
#!/bin/bash

python manage.py makemigrations
python manage.py migrate
