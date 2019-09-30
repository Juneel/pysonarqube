#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/9/29 16:33
# @Author : Juneel
# @File : __init__.py
import requests

__all__ = ['component', 'measure', 'user']


class Sonarqube(object):
    def __init__(self, ip="127.0.0.1", port=9000):
        """
        :param ip: 搭建的sonarqube的服务器IP地址  默认127.0.0.1
        :param port: 搭建的sonarqube的服务器WEB登录端口好 默认9000
        """
        self.ip = ip
        self.port = port

    def version(self):
        """
        获取sonarqube的版本号
        :return: 版本号 str
        """
        path = "/api/server/version"
        return requests.get(url="http://{0}:{1}{2}".format(self.ip, self.port, path)).text
