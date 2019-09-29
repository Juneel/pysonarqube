#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/9/29 17:32 
# @Author : Juneel
# @File : test.py

from measure import Measure
from component import Component

c = Component(ip="10.127.26.86", port=9000, username="sonar", password="sonar")
m = Measure(ip="10.127.26.86", port=9000, username="sonar", password="sonar")


if __name__ == "__main__":
    print(c.list(qualifiers="TRK"))
    print("\n")
    m.metrics = "bugs,code_smells,coverage,vulnerabilities"
    m.component_id = "AWf4E4NybATKeFuH9MGX"
    print(m.result())
