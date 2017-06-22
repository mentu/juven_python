#!C:\Python27\python.exe
# coding: utf-8

__author__ = 'yueyt'
from config_tt import base_config
from config_tt import base_config_debug
import socket
hostip = socket.gethostbyname(socket.gethostname())
if hostip.startswith('182.251'):
    base_config=base_config
elif hostip.startswith('182.119'):
    base_config=base_config_debug

