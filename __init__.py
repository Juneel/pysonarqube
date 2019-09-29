#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/29 16:33
# @Author : Juneel
# @File : __init__.py
__all__ = ['component', 'measure', 'user']


class Sonarqube(object):
    def __init__(self, sonarqube_server_ip="127.0.0.1", sonarqube_server_port=9000):
        """
        :param sonarqube_server_ip: 搭建的sonarqube的服务器IP地址  默认127.0.0.1
        :param sonarqube_server_port: 搭建的sonarqube的服务器WEB登录端口好 默认9000
        """
        self.sonarqube_server_ip = sonarqube_server_ip
        self.sonarqube_server_port = sonarqube_server_port
