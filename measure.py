#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/9/29 16:45 
# @Author : Juneel
# @File : measure.py
import requests
from component import Component
from log import cls_log_handler


@cls_log_handler
class Measure(Component):
    def __init__(self, ip, port, username, password):
        super().__init__(ip=ip, port=port, username=username, password=password)
        self.component_name = None
        self.component_id = None
        # metrics指扫描类型: bugs, code_smells, coverage, duplicated_lines, vulnerabilities等等
        self.metrics = None

    def result(self):
        """
        获取工程相对应metrics的检查结果
        :return: http状态码为200返回测量结果，否则返回None
        """
        path = "/api/measures/component"
        path = path + "?"
        if self.component_id is not None:
            path = path + "componentId=" + self.component_id
        if self.metrics is not None:
            path = path + "&metricKeys=" + self.metrics
        self.logger.info("Request url is " + path)
        try:
            rsp = requests.get(url="http://{0}:{1}{2}".format(self.ip, self.port, path))
            self.logger.info("Response content is " + str(rsp.text))
            if rsp.status_code == 200:
                return rsp.text
            else:
                return None
        except ConnectionError:
            return None

    def history_result(self, start_time, end_time, page_num, page_size):
        """
        查看对应工程的扫描metrics的历史记录
        :param start_time: 开始时间 2017-10-19 or 2017-10-19T13:00:00+0200
        :param end_time: 结束时间 2017-10-19 or 2017-10-19T13:00:00+0200
        :param page_num: 页码
        :param page_size: 单页大小
        :return: http状态码为200，返回历史记录，否则返回None
        """
        path = "/api/measures/search_history"
        if self.component_name is not None:
            path = path + "?component=" + self.component_name
        if self.metrics is not None:
            path = path + "&metrics= " + self.metrics
            if start_time and end_time:
                path = path + "&from=" + str(start_time) + "&to=" + end_time
            if page_num and page_size:
                path = path + "&p=" + str(page_num) + "&ps=" + str(page_size)
        self.logger.info("Request url is " + path)
        try:
            rsp = requests.get(url="http://{0}:{1}{2}".format(self.ip, self.port, path))
            self.logger.info("Response content is " + str(rsp.text))
            if rsp.status_code == 200:
                return rsp.text
            else:
                return None
        except ConnectionError:
            return None
