# pysonarqube

component: sonar下面扫描的工程对象的类，封装了工程的属性和方法

user: 用户的类,封装了用户的属性和方法

measure: 工程的扫描结果的类，封装了获取结果的方法

log：打印日志的装饰器

MRO：Measure继承Component，Component继承User，User继承Sonarqube, Sonarqube继承object
