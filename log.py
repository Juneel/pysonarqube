#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/9/30 11:53 
# @Author : Juneel
# @File : log.py
import logging

logger = logging.getLogger(name="sonar")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler_info = logging.FileHandler("pysonarqube.info", mode='a')
file_handler_info.setLevel(logging.INFO)
file_handler_info.setFormatter(formatter)
logger.addHandler(file_handler_info)
file_handler_error = logging.FileHandler("pysonarqube.error", mode='a')
file_handler_error.setLevel(logging.ERROR)
file_handler_error.setFormatter(formatter)


def cls_log_handler(cls):
    if not hasattr(cls, 'logger'):
        setattr(cls, 'logger', logger)
    return cls
