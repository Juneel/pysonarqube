#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/9/29 16:45 
# @Author : Juneel
# @File : user.py
import requests
from __init__ import Sonarqube


class User(Sonarqube):
    def __init__(self, ip, port, username, password):
        super().__init__(ip=ip, port=port)
        self.username = username
        self.password = password
        self.xsrf_token = None
        self.jwt_session = None

    def login(self):
        """
        根据username, password执行登陆操作，获取xsrf_token,jwt_session
        如果登录成功xsrf_token,jwt_session不为None
        Sonarqube 6.0版本开始支持
        :return: "success"表示登录成功， "fail"表示登录失败
        """
        path = "/api/authentication/login"
        try:
            url = "http://{0}:{1}{2}?login={3}&password={4}".format(self.ip,
                                                                    str(self.port),
                                                                    path,
                                                                    self.username,
                                                                    self.password)
            rsp = requests.post(url=url)
            if rsp.status_code == 200:
                self.xsrf_token = rsp.cookies.get("XSRF-TOKEN")
                self.jwt_session = rsp.cookies.get("JWT-SESSION")
                return "success"
            else:
                return "fail"
        except ConnectionError:
            return "fail"

    def logout(self):
        """
        登出操作，让TOKEN失效
        Sonarqube 6.3版本开始支持
        :return: "success"表示登出成功， "fail"表示登出失败  str
        """
        path = "/api/authentication/logout"
        try:
            rsp = requests.post(url="http://{0}:{1}{2}".format(self.ip,
                                                               self.port,
                                                               path),
                                headers={"Cookie": "XSRF-TOKEN={0};JWT-SESSION={1}".format(self.xsrf_token,
                                                                                           self.jwt_session),
                                         "X-XSRF-TOKEN": self.xsrf_token})
            if rsp.status_code == 200:
                return "success"
            else:
                return "fail"
        except ConnectionError:
            return "fail"

    def change_password(self, old_password, new_password):
        """
        修改user用户的密码，必须是本人修改自己的密码或者admin修改其他人的密码
        Sonarqube 5.2版本开始支持
        :param old_password: 老密码
        :param new_password: 新密码
        :return: "success"表示修改密码成功， "fail"表示修改密码失败 str
        """
        if self.xsrf_token is None:
            return "fail"
        path = "/api/users/change_password"
        if self.username is not None:
            path = path + "?login=" + str(self.username)
            if old_password is not None:
                path = path + "&previousPassword=" + str(old_password)
            if new_password is not None:
                path = path + "&password=" + str(new_password)
        try:
            rsp = requests.post(url="http://{0}:{1}{2}".format(self.ip,
                                                               self.port,
                                                               path))
            if rsp.status_code == 200:
                return "success"
            else:
                return "fail"
        except ConnectionError:
            return "fail"

    def create(self, email, username, nickname, password, scm_account=None, local="true"):
        """
        创建用户，创建用户的执行者必须有administrator的权限
        :param email:用户的email
        :param username: 用户登录名称
        :param nickname: 用户别名
        :param password: 用户名称
        :param scm_account:
        :param local:
        :return: "success"表示创建用户成功， "fail"表示创建用户失败 str
        """
        path = "/api/users/create"
        if username:
            path = path + "?login=" + username
            if password:
                path = path + "&password=" + password
            if email:
                path = path + "&email=" + email
            if nickname:
                path = path + "&name=" + nickname
            if scm_account:
                path = path + "&scmAccount=" + scm_account
            path = path + "&local=" + local
        try:
            rsp = requests.post(url="http://{0}:{1}{2}".format(self.ip,
                                                               self.port,
                                                               path))
            if rsp.status_code == 200:
                return "success"
            else:
                return "fail"
        except ConnectionError:
            return "fail"

# todo 继续增加其他的用户操作接口
