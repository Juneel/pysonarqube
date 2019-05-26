#!/usr/bin/env python
# coding=utf-8
# author=juneel
import requests
import logging
import time
logging.basicConfig(filename='sonarqube.trace', level=logging.INFO)


class Sonarqube:
    def __init__(self, sonarqube_server_ip, sonarqube_server_port):
        """
        :param sonarqube_server_ip: 搭建的sonarqube的服务器IP地址  默认127.0.0.1
        :param sonarqube_server_port: 搭建的sonarqube的服务器WEB登录端口好 默认9000
        """
        self.sonarqube_server_ip = sonarqube_server_ip if sonarqube_server_ip else "127.0.0.1"
        self.sonarqube_server_port = sonarqube_server_port if sonarqube_server_port else 9000
        self.xsrf_token = None
        self.jwt_session = None

    def login(self, username, password):
        """
        根据username, password执行登陆操作，获取xsrf_token,jwt_session
        如果登录成功xsrf_token,jwt_session不为None
        Sonarqube 6.0版本开始支持
        :param username: 登录sonarqube服务器的用户名
        :param password: 登录sonarqube服务器的密码
        :return: True表示登录成功， False表示登录失败
        """
        path = "/api/authentication/login"
        try:
            url = "http://{0}:{1}{2}?login={3}&password={4}".format(self.sonarqube_server_ip,
                                                                    str(self.sonarqube_server_port),
                                                                    path,
                                                                    username,
                                                                    password)
            logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Enter Sonarqube.login:")
            rsp = requests.post(url=url)
            if rsp.status_code == 200:
                self.xsrf_token = rsp.cookies.get("XSRF-TOKEN")
                self.jwt_session = rsp.cookies.get("JWT-SESSION")
                logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                return True
            else:
                return False
        except BaseException as be:
            print(be.message)
        return False

    def logout(self):
        """
        登出操作，让TOKEN失效
        Sonarqube 6.3版本开始支持
        :return: True表示登出成功  False表示登出失败
        """
        path = "/api/authentication/logout"
        try:
            rsp = requests.post(url="http://{0}:{1}{2}".format(self.sonarqube_server_ip,
                                                               self.sonarqube_server_port,
                                                               path),
                                headers={"Cookie": "XSRF-TOKEN={0};JWT-SESSION={1}".format(self.xsrf_token,
                                                                                           self.jwt_session),
                                         "X-XSRF-TOKEN": self.xsrf_token})
            if rsp.status_code == 200:
                logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                return True
            else:
                return False
        except BaseException as be:
            print(be.message)
        return False

    class Users:
        def __init__(self, ip, port, login, password):
            self.sonar = Sonarqube(sonarqube_server_ip=ip, sonarqube_server_port=port)
            self.sonar.login(username=login, password=password)

        def change_password(self, login, old_password, new_password):
            """
            修改user用户的密码，必须是本人修改自己的密码或者admin修改其他人的密码
            Sonarqube 5.2版本开始支持
            :param login: 被修改用户的username
            :param old_password: 老密码
            :param new_password: 新密码
            :return:
            """
            path = "/api/users/change_password"
            if login is not None:
                path = path + "?login=" + str(login)
                if old_password is not None:
                    path = path + "&previousPassword=" + str(old_password)
                if new_password is not None:
                    path = path + "&password=" + str(new_password)
            try:
                rsp = requests.post(url="http://{0}:{1}{2}".format(self.sonar.sonarqube_server_ip,
                                                                   self.sonar.sonarqube_server_port,
                                                                   path))
                if rsp.status_code == 200:
                    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                    return rsp.text
                else:
                    return None
            except BaseException as be:
                print(be.message)
            return None

        def create(self, email, login, name, password, scm_account=None, local="true"):
            """
            创建用户，创建用户的执行者必须有administrator的权限
            :param email:用户的email
            :param login: 用户登录名称
            :param name: 用户别名
            :param password: 用户名称
            :param scm_account:
            :param local:
            :return:
            """
            path = "/api/users/create"
            if login:
                path = path + "?login=" + login
                if password:
                    path = path + "&password=" + password
                if email:
                    path = path + "&email=" + email
                if name:
                    path = path + "&name=" + name
                if scm_account:
                    path = path + "&scmAccount=" + scm_account
                path = path + "&local=" + local
            try:
                rsp = requests.post(url="http://{0}:{1}{2}".format(self.sonar.sonarqube_server_ip,
                                                                   self.sonar.sonarqube_server_port,
                                                                   path))
                if rsp.status_code == 200:
                    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                    return rsp.text
                else:
                    return None
            except BaseException as be:
                print(be.message)
            return None

    class Components:
        def __init__(self, ip, port, login, password):
            self.sonar = Sonarqube(sonarqube_server_ip=ip, sonarqube_server_port=port)
            self.sonar.login(username=login, password=password)

        def search(self, language, p, ps, q, qualifiers):
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
            try:
                rsp = requests.get(url="http://{0}:{1}{2}".format(self.sonar.sonarqube_server_ip,
                                                                  self.sonar.sonarqube_server_port,
                                                                  path))
                if rsp.status_code == 200:
                    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                    return rsp.text
                else:
                    return None
            except BaseException as be:
                print(be.message)
            return None

        def show(self, component, component_id):
            """
            根据项目名称或者项目ID获取项目的详细信息
            :param component: 项目名称  str
            :param component_id: 项目ID  str
            :return: Http请求状态码为200，返回项目详细信息，否则返回None
            """
            path = "/api/components/show"
            path = path + "?"
            if component is not None:
                path = path + "component=" + component
            if component_id is not None:
                if component is not None:
                    path = path + "&componentId=" + component_id
                else:
                    path = path + "componentId=" + component_id
            try:
                rsp = requests.get(url="http://{0}:{1}{2}".format(self.sonar.sonarqube_server_ip,
                                                                  self.sonar.sonarqube_server_port,
                                                                  path))
                if rsp.status_code == 200:
                    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                    return rsp.text
                else:
                    return None
            except BaseException as be:
                print(be.message)
            return None

        def tree(self, asc, component, component_id, page_num, page_size, query, qualifiers, sort, strategy):
            """
            :param asc: true表示升序，false表示降序  str
            :param component: 项目名称  str
            :param component_id: 项目ID  str
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
            if component is not None:
                path = path + "component=" + component
            if component_id is not None:
                if component is not None:
                    path = path + "&componentId=" + component_id
                else:
                    path = path + "componentId=" + component_id
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
            try:
                rsp = requests.get(url="http://{0}:{1}{2}".format(self.sonar.sonarqube_server_ip,
                                                                  self.sonar.sonarqube_server_port,
                                                                  path))
                if rsp.status_code == 200:
                    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                    return rsp.text
                else:
                    return None
            except BaseException as be:
                print(be.message)
            return None

    class Measures:
        def __init__(self, ip, port, login, password):
            self.sonar = Sonarqube(sonarqube_server_ip=ip, sonarqube_server_port=port)
            self.sonar.login(username=login, password=password)

        def component(self, metrics, component_id):
            """
            获取工程相对应metrics的检查结果
            :param metrics: bugs, code_smells, coverage, duplicated_lines, vulnerabilities等等
            :param component_id: 工程ID
            :return: http状态码为200返回测量结果，否则返回None
            """
            path = "/api/measures/component"
            path = path + "?"
            if component_id is not None:
                path = path + "componentId=" + component_id
            if metrics is not None:
                path = path + "&metricKeys=" + metrics
            try:
                rsp = requests.get(url="http://{0}:{1}{2}".format(self.sonar.sonarqube_server_ip,
                                                                  self.sonar.sonarqube_server_port,
                                                                  path))
                if rsp.status_code == 200:
                    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                    return rsp.text
                else:
                    return None
            except BaseException as be:
                print(be.message)
            return None

        def search_history(self, component, metrics, start_time, end_time, page_num, page_size):
            """
            查看对应工程的扫描metrics的历史记录
            :param component: 工程名称
            :param metrics: bugs, code_smells, coverage, duplicated_lines, vulnerabilities等等
            :param start_time: 开始时间 2017-10-19 or 2017-10-19T13:00:00+0200
            :param end_time: 结束时间 2017-10-19 or 2017-10-19T13:00:00+0200
            :param page_num: 页码
            :param page_size: 单页大小
            :return: http状态码为200，返回历史记录，否则返回None
            """
            logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Enter search_history.")
            path = "/api/measures/search_history"
            if component is not None:
                path = path + "?component=" + component
            if metrics is not None:
                path = path + "&metrics= " + metrics
                if start_time and end_time:
                    path = path + "&from=" + str(start_time) + "&to=" + end_time
                if page_num and page_size:
                    path = path + "&p=" + str(page_num) + "&ps=" + str(page_size)
            try:
                rsp = requests.get(url="http://{0}:{1}{2}".format(self.sonar.sonarqube_server_ip,
                                                                  self.sonar.sonarqube_server_port,
                                                                  path))
                if rsp.status_code == 200:
                    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " " + str(rsp.content))
                    return rsp.text
                else:
                    return None
            except BaseException as be:
                print(be.message)
            return None
