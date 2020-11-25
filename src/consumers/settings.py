# -*- coding: utf-8 -*-
# @Author: ddcr
# @Date:   2016-09-05 19:36:59
# @Last Modified by:   ddcr
# @Last Modified time: 2016-09-05 19:38:06
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

XDMODBD = {
    'drivername': 'mysql',
    'username': os.environ.get("USER_XDMOD_BD"),
    'password': os.environ.get("PASS_XDMOD_BD"),
    'host': os.environ.get("HOST"),
    'port': os.environ.get("PORT"),
    'database': os.environ.get("XDMOD_DB"),
    'query': {'unix_socket': os.environ.get("UNIX_SOCKET")}
}
