# -*- coding=utf-8 -*-

from base.logger import *
from login.Authentication import CheckUserToken
import json
import os
import sys

SERVER_ERROR_CODE_NO_USERNAME			=	"{\"error\" : \"no username\"}"
SERVER_ERROR_CODE_NO_PASSWORD			=	"{\"error\" : \"no password\"}"
SERVER_ERROR_CODE_NO_LOCATION			=	"{\"error\" : \"no location\"}"
SERVER_ERROR_CODE_NO_USERNAME_2			=	"{\"error\" : \"no username_2\"}"
SERVER_ERROR_CODE_NO_WECHATTYPE			=	"{\"error\" : \"no wechatType\"}"
SERVER_ERROR_CODE_NO_WECHATNUMBER		=	"{\"error\" : \"no wechatNumber\"}"
SERVER_ERROR_CODE_NO_MANAGER			=	"{\"error\" : \"no manager\"}"



