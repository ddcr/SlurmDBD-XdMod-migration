# -*- coding: utf-8 -*-
# @Author: ddcr
# @Date:   2016-08-30 21:37:39
# @Last Modified by:   ddcr
# @Last Modified time: 2016-09-04 00:27:16
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

SLURMDBD = {
    'drivername': 'mysql',
    'username': os.environ.get("USER_SLURM_BD"),
    'password': os.environ.get("PASS_SLURM_BD"),
    'host': os.environ.get("HOST"),
    'port': os.environ.get("PORT"),
    'database': os.environ.get("SLURM_DB"),
    'query': {'unix_socket': os.environ.get("UNIX_SOCKET")}
}
