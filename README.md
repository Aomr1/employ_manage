# 基于Vue2.0、Vue-Element-Admin、Flask、MySQL、SQLAlchemy实现的员工管理系统

**实现前后端分离，前端使用Vue2.0、Vue-Element-Admin，后端使用Flask，数据库选用MySQL、SQLAlchemy**

**主要实现由后端控制不同用户角色的路由分配模块、用户注册登录修改密码模块、对员工信息，用户信息的增删改查超级表模块、员工打卡模块、不同身份打卡审核模块、信息导出模块、分页搜索获取数据模块等等。实现4种不同身份，5种部门的员工管理系统，实现修改头像，邮箱验证码发送注册等小模块**

本项目主要基于Vue-Element-Admin，详见：https://github.com/PanJiaChen/vue-element-admin/blob/master/README.zh-CN.md

![image-20220601182954456](D:\University\项目\员工管理系统\pic\1.png)

![image-20220601183020149](D:\University\项目\员工管理系统\pic\2.png)

![image-20220601183107571](D:\University\项目\员工管理系统\pic\3.png)

![image-20220601183145369](D:\University\项目\员工管理系统\pic\4.png)

![image-20220601190503481](D:\University\项目\员工管理系统\pic\5.png)

### 如何启动项目

需要配置好对应的Flask环境，以及了解Vue-Element-Admin，详见

https://github.com/PanJiaChen/vue-element-admin/blob/master/README.zh-CN.md

这里不再过多赘述。

#### 1.使用flask-migrate构建数据库

1.首先需要构建数据库名称，项目中使用的是employ_manage，在config.py中需要配置你的mysql信息以及邮箱信息

![image-20220601184130090](D:\University\项目\员工管理系统\pic\6.png)

2.在蓝图中的employ.py、punch.py中配置你的mysql信息

![image-20220601185129653](D:\University\项目\员工管理系统\pic\7.png)

![image-20220601185049932](D:\University\项目\员工管理系统\pic\8.png)

3.在蓝图中的user.py中配置你的邮箱信息

![image-20220601185300880](D:\University\项目\员工管理系统\pic\9.png)

然后在python环境中输入：

需要初始化一个迁移文件夹：

```
flask db init
```

然后再把当前的模型添加到迁移文件中：

```
flask db migrate
```

最后再把迁移文件中对应的数据库操作，真正的映射到数据库中：

```
flask db upgrade
```

#### 2.启动项目

在Python环境中启动app.py开启后台，项目已经打包放置dist文件，在浏览器输入http://127.0.0.1:5000/即可查看

开发环境下可在在vscode等前端开发工具中npm run dev启动后台

#### 3.注册用户

可以在数据库中添加或者在注册页面中自行进行注册

### **参考来源**

https://panjiachen.github.io/vue-element-admin/#/login?redirect=%2Fdashboard

https://panjiachen.github.io/vue-admin-template/#/login?redirect=%2Fdashboard

http://vue-admin.findfuture.cn/#/login?redirect=%2Fdashboard
