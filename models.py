from exts import db
from datetime import datetime

class EmployeeModel(db.Model):
    __tablename__ = "employee_data"
    #id、姓名、性别、学历、员工星级、部门、状态、入职时间 15个字段
    id = db.Column(db.Integer, db.ForeignKey('user_data.id'),primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(100),nullable=True)
    education = db.Column(db.String(100),nullable=True)
    mail = db.Column(db.String(100),nullable=False)
    imp = db.Column(db.Integer,nullable=True)
    department = db.Column(db.String(100),nullable=False)
    state = db.Column(db.String(100),nullable=True)
    entrytime = db.Column(db.String(100),nullable=True)
    #详细信息（出生日期、毕业学校、生源地址、婚姻状态、备注、创建信息时间）    
    birthday = db.Column(db.String(100),nullable=True)
    school = db.Column(db.String(100),nullable=True)
    home = db.Column(db.String(100),nullable=True)
    marriage = db.Column(db.String(100),nullable=True)
    remark = db.Column(db.Text,nullable=True)
    creatime = db.Column(db.DateTime,default=datetime.now)
    imageName = db.Column(db.LargeBinary(length=65536))
    
#打卡表
class PunchModel(db.Model):
    __tablename__ = "punch_data"
    punch_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    id = db.Column(db.Integer,nullable=False)
    name = db.Column(db.String(100),nullable=False)
    department = db.Column(db.String(100),nullable=False)
    identity = db.Column(db.String(100),nullable=False)
    day = db.Column(db.String(100),nullable=False)
    go_time = db.Column(db.String(100),default=None)
    leave_time = db.Column(db.String(100),default=None)
    intervals = db.Column(db.String(100),default=None)
    grp_agree = db.Column(db.String(100),default='agency')
    htp_agree = db.Column(db.String(100),default='agency')
    is_go_punch = db.Column(db.String(100),default='false')
    is_leave_punch = db.Column(db.String(100),default='false')

class UserModel(db.Model):
    __tablename__ = "user_data"
    #id、用户名、密码、邮箱、头像、部门、身份、创建时间
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    mail = db.Column(db.String(100),nullable=False)
    imageName = db.Column(db.LargeBinary(length=65536))
    department = db.Column(db.String(100),nullable=False)
    identity = db.Column(db.String(100),nullable=False)
    creatime = db.Column(db.DateTime,default=datetime.now)
    employee = db.relationship('EmployeeModel', backref='user')
    # 设置relationship，第一个参数为指向的ORM模型，backref参数可以指定反向访问的属性名称