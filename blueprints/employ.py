from flask import Blueprint,request
import json
import pymysql
from models import EmployeeModel
from exts import db
import datetime
import re

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

pymysql.install_as_MySQLdb()
conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    db='employ_manage',
    charset='utf8',
    autocommit=True
)
cursor = conn.cursor()
bp = Blueprint('employ', __name__, url_prefix='/Employ')

#个人用户修改信息
@bp.route('/FormSubmit',methods=["POST"])
def FormSubmit():
    ruleForm = request.json.get('ruleForm')
    request_token = request.json.get('token')
    id = int(request_token.split('_')[0])
    updata_employee = EmployeeModel.query.filter_by(id=id).first()
    updata_employee.name=ruleForm['name']
    updata_employee.sex = ruleForm['sex']
    updata_employee.marriage = ruleForm['marriage']
    updata_employee.education = ruleForm['education']
    updata_employee.imp = ruleForm['imp']
    updata_employee.department = ruleForm['department']
    updata_employee.state = ruleForm['state']
    updata_employee.entrytime = ruleForm['entrytime']
    updata_employee.birthday = ruleForm['birthday']
    updata_employee.school = ruleForm['school']
    updata_employee.home = ruleForm['home']
    updata_employee.remark = ruleForm['remark']
    updata_employee.mail = ruleForm['mail']
    #同步另一张表
    updata_employee.user.department = ruleForm['department']
    updata_employee.user.mail = ruleForm['mail']
    db.session.commit()
    return json.dumps({"code":200,"msg":'员工信息创建成功'}, ensure_ascii=False)


# 超级管理员提交表单
@bp.route('/AdminFormSubmit',methods=["POST"])
def AdminFormSubmit():
    ruleForm = request.json.get('ruleForm')
    new_Form = EmployeeModel(name = ruleForm['name'],
                              sex = ruleForm['sex'],
                              marriage = ruleForm['marriage'],
                              education = ruleForm['education'],
                              imp = ruleForm['imp'],
                              department = ruleForm['department'],
                              state = ruleForm['state'],
                              entrytime = ruleForm['entrytime'],
                              birthday = ruleForm['birthday'],
                              school = ruleForm['school'],
                              home = ruleForm['home'],
                              remark = ruleForm['remark'])
    db.session.add(new_Form)
    db.session.commit()
    return json.dumps({"code":20000,"msg":'员工信息创建成功'}, ensure_ascii=False)


# order by id desc;  
# limit 1,5 从索引为1的地方包括1向下取5条数据;
# listQuery={
# 'page': 1, 
# 'limit': 20, 
# 'sort': '+id'
# 'name': '张三', 
# 'imp': 3, 
# 'department': '后勤部',
# 'education': '专科',
# 'state': '休假',
# }
# select * from employee_data where imp='1' and name='李四' and department='技术部' and education='专科' 
# and state='休假' order by id desc limit 0,5;
# 查找加载到页面的信息
@bp.route('/SelectEmployee',methods=["POST"])
def SelectEmployee():
    listQuery = request.json.get('listQuery')
    sql_list = ['select id,name,sex,education,imp,department,state,entrytime,birthday,school,home,marriage,remark,creatime from employee_data']
    # 对值为''的键值对过滤
    for key in list(listQuery.keys()):
        if not listQuery.get(key):
            del listQuery[key]
    print('过滤后的listQuery：',listQuery)
    if len(listQuery) == 2:
        sql = ''.join(sql_list)
        cursor.execute(sql)
        employees = cursor.fetchall()
        employees_data = [{'id':employee[0],
                  'name': employee[1],
                  'sex': employee[2],
                  'education': employee[3],
                  'imp':employee[4],
                  'department': employee[5],
                  'state':employee[6],
                  'entrytime': employee[7],
                  'birthday': employee[8],
                  'school': employee[9],
                  'home':employee[10],
                  'marriage':employee[11],
                  'remark':employee[12],
                  'creatime':employee[13],             
              } for employee in employees]
        print('返回给前端的数据长度（导出excel，完整数据无分页）：',len(employees_data))
        return json.dumps({'items':employees_data,'code':20000,'total':len(EmployeeModel.query.all())}, 
                          ensure_ascii=False,
                          cls=ComplexEncoder)
    elif len(listQuery) == 3 :
        if listQuery['sort'] == '+id':
            pass
        else:
            sql_list.append(' order by id desc')
        search_page_limit = ' limit {},{}'.format(str((listQuery['page']-1)*listQuery['limit']),
                                              str(listQuery['limit']))
        sql_list.append(search_page_limit)
        sql = ''.join(sql_list)
        cursor.execute(sql)
        employees = cursor.fetchall()
        employees_data = [{'id':employee[0],
                  'name': employee[1],
                  'sex': employee[2],
                  'education': employee[3],
                  'imp':employee[4],
                  'department': employee[5],
                  'state':employee[6],
                  'entrytime': employee[7],
                  'birthday': employee[8],                  
                  'school': employee[9],
                  'home':employee[10],
                  'marriage':employee[11],
                  'remark':employee[12],
                  'creatime':employee[13],             
              } for employee in employees]
        print('返回给前端的数据长度(表格分页无搜索)：',len(employees_data))
        return json.dumps({'items':employees_data,'code':20000,'total':len(EmployeeModel.query.all())}, 
                          ensure_ascii=False,
                          cls=ComplexEncoder)
    elif len(listQuery) == 4:
        sql_list.append(' where {}="{}"'.format(str(list(listQuery.keys())[-1]),
                                              str(listQuery[list(listQuery.keys())[-1]])))
        if listQuery['sort'] == '+id':
            pass
        else:
            sql_list.append(' order by id desc')
        sql = ''.join(sql_list)
        cursor.execute(sql)
        total = len(cursor.fetchall())
        search_page_limit = ' limit {},{}'.format(str((listQuery['page']-1)*listQuery['limit']),
                                              str(listQuery['limit']))
        sql_list.append(search_page_limit)
        sql = ''.join(sql_list)
        cursor.execute(sql)
        employees = cursor.fetchall()
        employees_data = [{'id':employee[0],
                  'name': employee[1],
                  'sex': employee[2],
                  'education': employee[3],
                  'imp':employee[4],
                  'department': employee[5],
                  'state':employee[6],
                  'entrytime': employee[7],
                  'birthday': employee[8],                  
                  'school': employee[9],
                  'home':employee[10],
                  'marriage':employee[11],
                  'remark':employee[12],
                  'creatime':employee[13],             
              } for employee in employees]
        print('返回给前端的数据长度（表格分页加搜索）：',len(employees_data))
        return json.dumps({'items':employees_data,'code':20000,'total':total}, 
                          ensure_ascii=False,
                          cls=ComplexEncoder)
    else:
        last_item_key = list(listQuery.keys())[len(list(listQuery.keys()))-1]
        other_items_keys = list(listQuery.keys())[3:len(list(listQuery.keys()))-1]
        sql_list.append(' where {}="{}"'.format(str(last_item_key),
                                              str(listQuery[last_item_key])))   
        for other_item in other_items_keys:
            sql_list.append(' and {}="{}"'.format(str(other_item),
                                                str(listQuery[other_item])))
        if listQuery['sort'] == '+id':
            pass
        else:
            sql_list.append(' order by id desc')
        sql = ''.join(sql_list)
        cursor.execute(sql)
        total = len(cursor.fetchall())
        search_page_limit = ' limit {},{}'.format(str((listQuery['page']-1)*listQuery['limit']),
                                              str(listQuery['limit']))
        sql_list.append(search_page_limit)
        sql = ''.join(sql_list)
        cursor.execute(sql)
        employees = cursor.fetchall()
        employees_data = [{'id':employee[0],
                  'name': employee[1],
                  'sex': employee[2],
                  'education': employee[3],
                  'imp':employee[4],
                  'department': employee[5],
                  'state':employee[6],
                  'entrytime': employee[7],
                  'birthday': employee[8],
                  'school': employee[9],
                  'home':employee[10],
                  'marriage':employee[11],
                  'remark':employee[12],
                  'creatime':employee[13],             
              } for employee in employees]
        print('返回给前端的数据长度（表格分页加搜索）：',len(employees_data))
        return json.dumps({'items':employees_data,'code':20000,'total':total}, 
                          ensure_ascii=False,
                          cls=ComplexEncoder)

# 查找详细信息
@bp.route('/SeleteEmployeeMore',methods=["POST"])
def SeleteEmployeeMore():
    more_id = request.json.get('more_id')
    items = EmployeeModel.query.filter_by(id=more_id).all()
    more_employee = [{'id':item.id,
                  'name': item.name,
                  'sex': item.sex,
                  'education': item.education,
                  'imp':item.imp ,
                  'department': item.department,
                  'state': item.state,
                  'entrytime': item.entrytime,
                  'birthday':item.birthday,
                  'school':item.school,
                  'home':item.home,
                  'marriage':item.marriage,
                  'remark':item.remark,
                  'creatime':item.creatime,
                  } for item in items]
    return json.dumps({"code":20000,"more_employee":more_employee}, ensure_ascii=False,
                      cls=ComplexEncoder)

# 删除员工信息
@bp.route('/DeleteEmployee',methods=["POST"])
def DeleteEmployee():
    delete_id = request.json.get('delete_id')
    delete_employee = EmployeeModel.query.filter_by(id=delete_id).first()
    db.session.delete(delete_employee)
    db.session.commit()
    return json.dumps({"code":20000}, ensure_ascii=False)

# 修改员工信息
@bp.route('/UpdateEmployee',methods=["POST"])
def UpdateEmployee():
    tempData = request.json.get('tempData')
    update_employee = EmployeeModel.query.filter_by(id=tempData['id']).first()
    update_employee.education = tempData['education']
    update_employee.imp = tempData['imp']
    update_employee.department = tempData['department']
    entrytime = str(tempData['entrytime'])
    year = re.findall(r'(.*)-(.*)-(.*)',entrytime)[0][0]
    month = re.findall(r'(.*)-(.*)-(.*)',entrytime)[0][1]
    day = re.findall(r'(.*)-(.*)-(.*)',entrytime)[0][2][:2]
    update_employee.entrytime = '-'.join([year,month,day])
    update_employee.marriage = tempData['marriage']
    update_employee.remark = tempData['remark']
    db.session.commit()
    return json.dumps({"code":20000}, ensure_ascii=False)

# 修改员工状态
@bp.route('/UpdateEmployeeState',methods=["POST"])
def UpdateEmployeeState():
    change_state_id = request.json.get('change_state_id')
    change_state = request.json.get('change_state')
    update_employee = EmployeeModel.query.filter_by(id=change_state_id).first()
    update_employee.state = change_state
    db.session.commit()
    return json.dumps({"code":20000}, ensure_ascii=False)

# 个人中心需要的数据(不用token里的vuex的数据原因在于修改完表单后会返回2022-05-11T00:00:00.000Z，
# 包含时间的字段，组件默认返回形式)
@bp.route('/GetTwoTime',methods=["POST"])
def GetTwoTime():
    request_token = request.json['token']
    token_id = request_token.split('_')[0]
    employee = EmployeeModel.query.filter_by(id=token_id).first()
    if employee.education is None:
        return json.dumps({"code":20000}, ensure_ascii=False)
    else:    
        data = [{'entrytime':employee.entrytime,
                'birthday':employee.birthday}]
        return json.dumps({"code":20000,"items":data}, ensure_ascii=False)
