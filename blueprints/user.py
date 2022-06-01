from flask import Blueprint,request
from flask_mail import Message
from models import UserModel,EmployeeModel
import json
from exts import db,mail
import random
from router import employee_data,groupleader_data,highleader_data,boss_data
import datetime

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)
        
bp = Blueprint('user', __name__, url_prefix='/User')

#登录
@bp.route('/Login',methods=['POST'])
def Login():
    username = request.json['username']
    password = request.json['password']
    user = UserModel.query.filter_by(username=username,password=password).all()
    if len(user) == 0:
        print("账号密码错误")
        return json.dumps({'code': 50016, 'message':'账号或密码错误'}, ensure_ascii=False)
    else:
        id = str(user[0].id)
        token = user[0].identity
        #加密
        ord_token_list = [id]
        for i in token:
            ord_token_list.append(str(ord(i)))
        token = '_'.join(ord_token_list)
        return json.dumps({'code': 20000,'data': {'token': token}}, ensure_ascii=False,)

# 获取个人信息
@bp.route('/GetInfo',methods=['GET'])
def GetInfo():
    #获取token并且解密
    request_token = request.args['token']
    token_list = request_token.split('_')
    token = ''
    for i in token_list[1:]:
        token += chr(int(i))
    print('GetInfo获取信息成功')
    id = int(token_list[0])
    employee = EmployeeModel.query.filter_by(id=id).first()

    return json.dumps({
    "code": 20000,
    "data": {
        "roles": [
            token
        ],
        #"avatar":employee.imageName,
        "id": employee.id,
        "avatar": 'http://127.0.0.1:5000/user/ChangeImg',
        "name": employee.name,
        "sex": employee.sex,
        "education": employee.education,
        'mail': employee.mail,
        "imp": employee.imp,
        'department': employee.department,
        "state": employee.state,
        "entrytime": employee.entrytime,
        "birthday": employee.birthday,
        "school": employee.school,
        "home": employee.home,
        "marriage": employee.marriage,
        "remark": employee.remark,
        "creatime": employee.creatime,
        }
    }, ensure_ascii=False,cls=ComplexEncoder)


# 注册
@bp.route('/Register',methods=['POST'])
def Register():
    ruleForm = request.json
    if int(ruleForm['code']) != VerificationCode:
        return 'codeError'

    #获取默认头像的二进制流
    with open('default.gif','rb') as f:
        a = f.read()
    #print(a)

    new_Form = UserModel(username = ruleForm['username'],
                     password = ruleForm['pass'],
                     mail = ruleForm['email'],
                     department = ruleForm['department'],
                     identity = ruleForm['identity'],
                     imageName = a)

    new_Form.employee=[EmployeeModel(name = ruleForm['username'],
                                     department = ruleForm['department'],
                                     mail = ruleForm['email'],
                                     imageName = a)]
    db.session.add(new_Form)
    db.session.commit()

    return json.dumps({"code":200,"msg":'注册成功'}, ensure_ascii=False)

#修改密码
@bp.route('/ChangePwd',methods=["POST"])
def ChangePwd():
    ruleForm = request.json
    user = UserModel.query.filter_by(username=ruleForm['username'],mail=ruleForm['email']).first()
    user.password = ruleForm['pass']
    db.session.commit()
    print("密码修改成功")
    return json.dumps({"code": 20000, "msg":"修改密码成功"}, ensure_ascii=False)

#邮箱验证
@bp.route('/SendMail',methods=['POST'])
def SendMail():
    recipient_mail = request.json.get("mail")
    with open("邮箱验证界面.txt", 'r', encoding='utf-8') as f:
        html = f.read()

    global VerificationCode
    VerificationCode = random.randint(100000, 1000000)

    msg = Message(subject="注册账号通知",
                  sender="", #在此处配置你的邮箱
                  html=html.format("注册账号",VerificationCode),
                  recipients=[recipient_mail])
    mail.send(msg)
    return json.dumps({'VerificationCode':VerificationCode}, ensure_ascii=False)

# 返回身份对应的路由
@bp.route('/GetRouter',methods=["POST"])
def GetRouter():
    #获取token,识别身份,返回身份对应的路由
    request_token = request.json['token']
    token_list = request_token.split('_')
    role = ''
    for i in token_list[1:]:
        role += chr(int(i))
    print(role)
    if role == '老板':
        data = boss_data
    elif role == '小组长':
        data = groupleader_data
    elif role == '主管':
        data = highleader_data
    else:
        data = employee_data
    print("GetRouter获取路由成功")
    return json.dumps({"code":20000,"data":data}, ensure_ascii=False)


#获取头像,在getinfo内
@bp.route('/GetAvatar',methods=['GET', 'POST'])
def GetAvatar():
    id = request.args.get('id')
    employee = EmployeeModel.query.filter_by(id=id).first()
    a = employee.imageName
    return a

#修改头像
@bp.route('/ChangeAvatar',methods=['GET', 'POST'])
def ChangeAvatar():
    file = request.files.get('file')
    token_request = request.form.get('token')
    id = int(token_request.split('_')[0])
    a = file.read()
    employee = EmployeeModel.query.filter_by(id=id).first()
    user = UserModel.query.filter_by(id=id).first()
    user.imageName = a
    employee.imageName = a
    db.session.commit()
    print('头像修改成功')

    return a