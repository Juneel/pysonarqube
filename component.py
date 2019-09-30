#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/9/29 16:45 
# @Author : Juneel
# @File : component.py
from user import User
import requests
from log import cls_log_handler


@cls_log_handler
class Component(User):
    def __init__(self, ip, port, username, password, component_name=None, component_id=None):
        super().__init__(ip=ip, port=port, username=username, password=password)
        self.component_name = component_name
        self.component_id = component_id

    def list(self, language=None, p=None, ps=None, q=None, qualifiers=None):
        """
        按照类型搜索项目
        :param language: 非必传参数，语言 str
        :param p: 非必传参数，页码  int
        :param ps: 非必传参数，一页的数量 int
        :param q: 非必传参数，搜索关键字 str
        :param qualifiers: 必传参数，=TRK返回所有项目，=DIR返回所有路径，=FIL返回所有文件  str
        :return: Http请求状态码200返回搜索结果，否则返回None
        """
        path = "/api/components/search"
        path = path + "?qualifiers=" + str(qualifiers)
        if language is not None:
            path = path + "&language=" + str(language)
        if p is not None:
            path = path + "&p=" + str(p)
        if ps is not None:
            path = path + "&ps=" + str(ps)
        if q is not None:
            path = path + "&q=" + str(q)
        self.logger.info("Request path is " + path)
        try:
            rsp = requests.get(url="http://{0}:{1}{2}".format(self.ip,
                                                              self.port,
                                                              path))
            self.logger.info("Response content is " + str(rsp.text))
            if rsp.status_code == 200:
                return rsp.text
            else:
                return None
        except ConnectionError as ce:
            self.logger.error("Http request catch some error: " + str(ce))
            return None

    def detail(self):
        """
        根据项目名称或者项目ID获取项目的详细信息
        :return: Http请求状态码为200，返回项目详细信息，否则返回None
        """
        path = "/api/components/show"
        path = path + "?"
        if self.component_name is not None:
            path = path + "component=" + self.component_name
        if self.component_id is not None:
            if self.component_name is not None:
                path = path + "&componentId=" + self.component_id
            else:
                path = path + "componentId=" + self.component_id
        self.logger.info("Request path is " + path)
        try:
            rsp = requests.get(url="http://{0}:{1}{2}".format(self.ip, self.port, path))
            self.logger.info("Response content is " + str(rsp.text))
            if rsp.status_code == 200:
                return rsp.text
            else:
                return None
        except ConnectionError:
            return None

    def tree(self, asc, page_num, page_size, query, qualifiers, sort, strategy):
        """
        :param asc: true表示升序，false表示降序  str
        :param page_num: 页码  int
        :param page_size: 页大小 int
        :param query: 查询关键字 str
        :param qualifiers:  =TRK返回所有项目，=DIR返回所有路径，=FIL返回所有文件  str
        :param sort: 排序对象，按照s进行排序  str
        :param strategy: =all表示所有项目， =children表示子项目，=leaves表示所有叶子项目  str
        :return: Http状态码为200，返回项目列表，否则返回None
        """
        path = "/api/components/tree"
        path = path + "?"
        if self.component_name is not None:
            path = path + "component=" + self.component_name
        if self.component_id is not None:
            if self.component_name is not None:
                path = path + "&componentId=" + self.component_id
            else:
                path = path + "componentId=" + self.component_id
        if asc is not None:
            path = path + "&asc=" + asc
        if page_num is not None:
            path = path + "&p=" + str(page_num)
        if page_size is not None:
            path = path + "&ps=" + str(page_size)
        if query is not None:
            path = path + "&q=" + query
        if qualifiers is not None:
            path = path + "&qualifiers=" + qualifiers
        if sort is not None:
            path = path + "&s=" + sort
        if strategy is not None:
            path = path + "&strategy=" + strategy
        self.logger.info("Request path is " + path)
        try:
            rsp = requests.get(url="http://{0}:{1}{2}".format(self.ip, self.port, path))
            self.logger.info("Response content is " + str(rsp.text))
            if rsp.status_code == 200:
                return rsp.text
            else:
                return None
        except ConnectionError:
            return None
