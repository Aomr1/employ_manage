# -*- coding: utf-8 -*-
from flask import Blueprint,request
from models import PunchModel
import json
from exts import db
import pymysql
import datetime

bp = Blueprint('punch', __name__, url_prefix='/Punch')

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

@bp.route('/GetPunch',methods=["POST"])
def GetPunch():
    request_token = request.json['token']
    name = request.json['name']
    gotime = request.json['go_time'] #2022-05-20 14:56:53
    leavetime = request.json['leave_time'] #2022-05-20 14:58:53
    date = request.json['date'] #2022-05-20 14:58:59
    identity = request.json['identity']
    department = request.json['department']
    token_id = request_token.split('_')[0]
    day = date.split(' ')[0]
    go_time = gotime.split(' ')[1]
    leave_time = leavetime.split(' ')[1]
    # 计算时间差
    timedelta = [int(i) for i in go_time.split(':')]
    intervals = str(datetime.datetime.strptime(leave_time, '%H:%M:%S') - 
                   datetime.timedelta(hours=timedelta[0],minutes=timedelta[1],seconds=timedelta[2])).split(' ')[1]
    # 默认主管不需要自己的批准，但可以被主管修改htp_agree
    if identity == '小组长':
        if len(PunchModel.query.filter_by(id=token_id,day=day).all()) == 0:    
            Punch = PunchModel(id = token_id,
                                    name = name,
                                    day = day,
                                    go_time = go_time,
                                    leave_time = leave_time,
                                    identity = identity,
                                    department = department,
                                    intervals = intervals,
                                    grp_agree = 'true',
                                    is_go_punch = 'true',
                                    is_leave_punch = 'true')
            db.session.add(Punch)
            db.session.commit()
            return json.dumps({"code":20000,
                               "desc_go_time":go_time,
                               "desc_leave_time":leave_time,
                               "msg":'上班打卡成功'}, ensure_ascii=False)
        else:
            if PunchModel.query.filter_by(id=token_id,day=day).first().identity != identity or PunchModel.query.filter_by(id=token_id,day=day).first().department != department:
                delete_punch = PunchModel.query.filter_by(id=token_id,day=day).first()
                db.session.delete(delete_punch)
                db.session.commit()
                Punch = PunchModel(id = token_id,
                                        name = name,
                                        day = day,
                                        go_time = go_time,
                                        leave_time = leave_time,
                                        identity = identity,
                                        department = department,
                                        intervals = intervals,
                                        grp_agree = 'true',
                                        is_go_punch = 'true',
                                        is_leave_punch = 'true')  
                db.session.add(Punch)
                db.session.commit()
                return json.dumps({"code":20000,
                                   "desc_go_time":go_time,
                                   "desc_leave_time":leave_time,
                                   "msg":'修改员工打卡成功（考虑到员工可能换部门或者职位提升'}, ensure_ascii=False)
            else:
                update_punch = PunchModel.query.filter_by(id=token_id,day=day).first()
                update_punch.go_time = go_time
                update_punch.is_go_punch = 'true'
                update_punch.leave_time = leave_time
                update_punch.is_leave_punch = 'true'
                update_punch.intervals = intervals
                update_punch.grp_agree = 'true'
                update_punch.htp_agree = 'agency'
                db.session.commit()
                return json.dumps({"code":20000,
                                    "desc_go_time":go_time,
                                    "desc_leave_time":leave_time,                               
                                    "msg":'修改上班打卡成功'}, ensure_ascii=False)
    # 默认主管不需要自己和小组长的批准，但可以被老板修改htp_agree
    if identity == '主管':
        if len(PunchModel.query.filter_by(id=token_id,day=day).all()) == 0:    
            Punch = PunchModel(id = token_id,
                                    name = name,
                                    day = day,
                                    go_time = go_time,
                                    leave_time = leave_time,
                                    identity = identity,
                                    department = department,
                                    intervals = intervals,
                                    grp_agree = 'true',
                                    htp_agree = 'true',
                                    is_go_punch = 'true',
                                    is_leave_punch = 'true')
            db.session.add(Punch)
            db.session.commit()
            return json.dumps({"code":20000,
                               "desc_go_time":go_time,
                               "desc_leave_time":leave_time,
                               "msg":'上班打卡成功'}, ensure_ascii=False)
        else:
            if PunchModel.query.filter_by(id=token_id,day=day).first().identity != identity or PunchModel.query.filter_by(id=token_id,day=day).first().department != department:
                delete_punch = PunchModel.query.filter_by(id=token_id,day=day).first()
                db.session.delete(delete_punch)
                db.session.commit()
                Punch = PunchModel(id = token_id,
                                        name = name,
                                        day = day,
                                        go_time = go_time,
                                        leave_time = leave_time,
                                        identity = identity,
                                        department = department,
                                        intervals = intervals,
                                        grp_agree = 'true',
                                        htp_agree = 'true',
                                        is_go_punch = 'true',
                                        is_leave_punch = 'true')  
                db.session.add(Punch)
                db.session.commit()
                return json.dumps({"code":20000,
                                   "desc_go_time":go_time,
                                   "desc_leave_time":leave_time,
                                   "msg":'修改员工打卡成功（考虑到员工可能换部门或者职位提升'}, ensure_ascii=False)
            else:
                update_punch = PunchModel.query.filter_by(id=token_id,day=day).first()
                update_punch.go_time = go_time
                update_punch.is_go_punch = 'true'
                update_punch.leave_time = leave_time
                update_punch.is_leave_punch = 'true'
                update_punch.intervals = intervals
                update_punch.grp_agree = 'true',
                update_punch.htp_agree = 'true',
                db.session.commit()
                return json.dumps({"code":20000,
                                    "desc_go_time":go_time,
                                    "desc_leave_time":leave_time,                               
                                    "msg":'修改上班打卡成功'}, ensure_ascii=False)
    else:
        if len(PunchModel.query.filter_by(id=token_id,day=day).all()) == 0:    
            Punch = PunchModel(id = token_id,
                                    name = name,
                                    day = day,
                                    go_time = go_time,
                                    leave_time = leave_time,
                                    identity = identity,
                                    department = department,
                                    intervals = intervals,
                                    is_go_punch = 'true',
                                    is_leave_punch = 'true')
            db.session.add(Punch)
            db.session.commit()
            return json.dumps({"code":20000,
                               "desc_go_time":go_time,
                               "desc_leave_time":leave_time,
                               "msg":'上班打卡成功'}, ensure_ascii=False)
        else:
            if PunchModel.query.filter_by(id=token_id,day=day).first().identity != identity or PunchModel.query.filter_by(id=token_id,day=day).first().department != department:
                delete_punch = PunchModel.query.filter_by(id=token_id,day=day).first()
                db.session.delete(delete_punch)
                db.session.commit()
                Punch = PunchModel(id = token_id,
                                        name = name,
                                        day = day,
                                        go_time = go_time,
                                        leave_time = leave_time,
                                        identity = identity,
                                        department = department,
                                        intervals = intervals,
                                        is_go_punch = 'true',
                                        is_leave_punch = 'true')  
                db.session.add(Punch)
                db.session.commit()
                return json.dumps({"code":20000,
                                   "desc_go_time":go_time,
                                   "desc_leave_time":leave_time,
                                   "msg":'修改员工打卡成功（考虑到员工可能换部门或者职位提升'}, ensure_ascii=False)
            else:
                update_punch = PunchModel.query.filter_by(id=token_id,day=day).first()
                update_punch.go_time = go_time
                update_punch.is_go_punch = 'true'
                update_punch.leave_time = leave_time
                update_punch.is_leave_punch = 'true'
                update_punch.intervals = intervals
                update_punch.grp_agree = 'agency'
                update_punch.htp_agree = 'agency'
                db.session.commit()
                return json.dumps({"code":20000,
                                    "desc_go_time":go_time,
                                    "desc_leave_time":leave_time,                               
                                    "msg":'修改上班打卡成功'}, ensure_ascii=False) 

@bp.route('/GetIsPunch',methods=["POST"])
def GetIsPunch():
    request_token = request.json['token']
    date = request.json['date'] #2022-05-20 14:58:53
    token_id = request_token.split('_')[0]
    day = date.split(' ')[0]
    if len(PunchModel.query.filter_by(id=token_id,day=day).all()) == 0:
        return json.dumps({"code":20000,
                           "is_go_punch":"false",
                           "is_leave_punch":"false",
                           "go_time":'1900-01-01 00:00:00',
                           "leave_time":'1900-01-01 00:00:00',
                           "desc_go_time":"null",
                           "desc_leave_time":"null"}, ensure_ascii=False)
    else:
        # "2020-06-18 22:10:13"
        go_time = PunchModel.query.filter_by(id=token_id,day=day).first().go_time
        go_time_format = date = ' '.join([str(day),str(go_time)])
        leave_time = PunchModel.query.filter_by(id=token_id,day=day).first().leave_time
        leave_time_format = date = ' '.join([str(day),str(leave_time)])
        return json.dumps({"code":20000,
                           "is_go_punch":"true",
                           "is_leave_punch":"true",
                           "go_time":go_time_format,
                           "leave_time":leave_time_format,
                            "desc_go_time":go_time,
                            "desc_leave_time":leave_time, 
                           }, ensure_ascii=False)  

# In [17]: time2 = '22:01:49'
# In [18]: datetime.datetime.strptime(time2, '%H:%M:%S') - 
# In [18]: datetime.timedelta(hours=8,minutes=9,seconds=51)
# Out[18]: datetime.datetime(1900, 1, 1, 13, 51, 58)
#select * from punch_data where department = '人力资源部' and( identity='小组长' or identity='员工');
@bp.route('/SelectPunch',methods=["POST"])
def SelectPunch():
    PunchQuery = request.json.get('PunchQuery')
    department = request.json.get('department')
    request_token = request.json.get('token')
    token_list = request_token.split('_')
    role = ''
    for i in token_list[1:]:
        role += chr(int(i))
    sql_list = ['select id,name,day,go_time,leave_time,department,identity,intervals,grp_agree,htp_agree from punch_data']
    if role != '老板':
        sql_list.append(" where department = '{}'".format(department))
        if role == '小组长':
            sql_list.append(" and identity = '员工' and grp_agree !='true' and htp_agree != 'true'")
        elif role == '主管':
            sql_list.append(" and (identity = '员工' or identity = '小组长') and grp_agree ='true' and htp_agree != 'true'")
    else:
        sql_list.append(" where (identity = '员工' or identity = '小组长' or identity = '主管') and grp_agree = 'true' and htp_agree = 'true'")
    # 对值为''的键值对过滤
    for key in list(PunchQuery.keys()):
        if not PunchQuery.get(key):
            del PunchQuery[key]
    print(PunchQuery)
    if len(PunchQuery) == 3 :
        if PunchQuery['sort'] == '+id':
            sql_list.append(' order by id')
        else:
            sql_list.append(' order by id desc')
        sql = ''.join(sql_list)
        cursor.execute(sql)
        total = len(cursor.fetchall())
        search_page_limit = ' limit {},{}'.format(str((PunchQuery['page']-1)*PunchQuery['limit']),
                                              str(PunchQuery['limit']))
        sql_list.append(search_page_limit)
        sql = ''.join(sql_list)
        cursor.execute(sql)
        punchs = cursor.fetchall()
        punchs_data = [{'id':punch[0],
                  'name': punch[1],
                  'day': punch[2],
                  'go_time': punch[3],
                  'leave_time':punch[4],  
                  'department':punch[5],
                  'identity':punch[6],
                  'intervals':punch[7],
                  'grp_agree':punch[8],
                  'htp_agree':punch[9]
              } for punch in punchs]
        return json.dumps({'items':punchs_data,'code':20000,'total':total}, 
                          ensure_ascii=False)
    else:
        # 判断查询条件是否存在state
        if 'state' in list(PunchQuery.keys()):
            if PunchQuery['state'] == '代办':
                if role == '小组长':
                    sql_list.append(' and {}="{}"'.format('grp_agree','agency'))    
                else:
                    sql_list.append(' and {}="{}"'.format('htp_agree','agency')) 
            else:
                if role == '小组长':
                    sql_list.append(' and {}="{}"'.format('grp_agree','false'))    
                else:
                    sql_list.append(' and {}="{}"'.format('htp_agree','false'))       
        other_items_keys = list(PunchQuery.keys())[3:len(list(PunchQuery.keys()))]   
        # 判断查询条件是否存在intervals
        if 'intervals' in list(PunchQuery.keys()):
            sql_list.append(" and str_to_date(intervals, '%H:%i:%s') > str_to_date('{}', '%H:%i:%s')".format(''.join([PunchQuery['intervals'],':00'])))
        for other_item in other_items_keys:
            if other_item == 'state' or other_item == 'intervals':
                pass
            else:
                if other_item == 'day':
                    sql_list.append(' and {}="{}"'.format(str('day'),
                                        str(PunchQuery['day'].split('T')[0])))
                else:     
                    sql_list.append(' and {}="{}"'.format(str(other_item),
                                                    str(PunchQuery[other_item])))
        if PunchQuery['sort'] == '+id':
            sql_list.append(' order by id')
        else:
            sql_list.append(' order by id desc')
        sql = ''.join(sql_list)
        cursor.execute(sql)
        total = len(cursor.fetchall())
        search_page_limit = ' limit {},{}'.format(str((PunchQuery['page']-1)*PunchQuery['limit']),
                                              str(PunchQuery['limit']))
        sql_list.append(search_page_limit)
        sql = ''.join(sql_list)
        cursor.execute(sql)
        punchs = cursor.fetchall()
        punchs_data = [{'id':punch[0],
                  'name': punch[1],
                  'day': punch[2],
                  'go_time': punch[3],
                  'leave_time':punch[4],  
                  'department':punch[5],
                  'identity':punch[6],
                  'intervals':punch[7],
                  'grp_agree':punch[8],
                  'htp_agree':punch[9]
              } for punch in punchs]
        return json.dumps({'items':punchs_data,'code':20000,'total':total}, 
                          ensure_ascii=False)

# 修改员工上班打卡时间
@bp.route('/UpDateGoTime',methods=["POST"])
def UpDateGoTime():
    # login_role = request.json.get('login_role')
    # identity = request.json.get('identity')
    id = request.json.get('id')
    new_go_time = request.json.get('new_go_time')
    leave_time = request.json.get('leave_time')
    day = request.json.get('day')
    # 计算时间差
    timedelta = [int(i) for i in new_go_time.split(':')]
    intervals = str(datetime.datetime.strptime(leave_time, '%H:%M:%S') - 
                   datetime.timedelta(hours=timedelta[0],minutes=timedelta[1],seconds=timedelta[2])).split(' ')[1]
    update_punch = PunchModel.query.filter_by(id=id,day=day).first()
    update_punch.intervals = intervals
    update_punch.go_time = new_go_time
    # if login_role == '小组长':
    #     update_punch.grp_agree = 'true'
    # elif login_role == '主管':
    #     if identity == '员工':
    #         update_punch.grp_agree = 'true'
    #     else:
    #         update_punch.htp_agree = 'true'
    db.session.commit()
    return json.dumps({"code":20000,"intervals":intervals}, ensure_ascii=False)

# 修改员工下班打卡时间
@bp.route('/UpDateLeaveTime',methods=["POST"])
def UpDateLeaveTime():
    # login_role = request.json.get('login_role')
    # identity = request.json.get('identity')
    id = request.json.get('id')
    new_leave_time = request.json.get('new_leave_time')
    go_time = request.json.get('go_time')
    day = request.json.get('day')
    # 计算时间差
    timedelta = [int(i) for i in go_time.split(':')]
    intervals = str(datetime.datetime.strptime(new_leave_time, '%H:%M:%S') - 
                   datetime.timedelta(hours=timedelta[0],minutes=timedelta[1],seconds=timedelta[2])).split(' ')[1]
    update_punch = PunchModel.query.filter_by(id=id,day=day).first()
    update_punch.intervals = intervals 
    update_punch.leave_time = new_leave_time
    # if login_role == '小组长':
    #     update_punch.grp_agree = 'true'
    # elif login_role == '主管':
    #     if identity == '员工':
    #         update_punch.grp_agree = 'true'
    #     else:
    #         update_punch.htp_agree = 'true'
    db.session.commit()
    return json.dumps({"code":20000,"intervals":intervals}, ensure_ascii=False)

# 删除所有打卡信息
@bp.route('/DeletePunch',methods=["POST"])
def DeletePunch():
    delete_id = request.json.get('delete_id')
    delete_day = request.json.get('delete_day')
    delete_punch = PunchModel.query.filter_by(id=delete_id,day=delete_day).first()
    db.session.delete(delete_punch)
    db.session.commit()
    return json.dumps({"code":20000}, ensure_ascii=False)

# 删除上班打卡时间
@bp.route('/DeleteGoTime',methods=["POST"])
def DeleteGoTime():
    delete_id = request.json.get('delete_id')
    delete_day = request.json.get('delete_day')
    delete_punch = PunchModel.query.filter_by(id=delete_id,day=delete_day).first()
    delete_punch.go_time = None
    db.session.commit()
    return json.dumps({"code":20000}, ensure_ascii=False)

# 删除下班打卡时间
@bp.route('/DeleteLeaveTime',methods=["POST"])
def DeleteLeaveTime():
    delete_id = request.json.get('delete_id')
    delete_day = request.json.get('delete_day')
    delete_punch = PunchModel.query.filter_by(id=delete_id,day=delete_day).first()
    delete_punch.leave_time = None
    db.session.commit()
    return json.dumps({"code":20000}, ensure_ascii=False)

# 修改小组长批准驳回状态
@bp.route('/UpdateGrpAgree',methods=["POST"])
def UpdateGrpAgree():
    id = request.json.get('id')
    grp_agree = request.json.get('grp_agree')
    day = request.json.get('day')
    update_punch = PunchModel.query.filter_by(id=id,day=day).first()
    update_punch.grp_agree = grp_agree
    db.session.commit()
    return json.dumps({"code":20000}, ensure_ascii=False)

# 修改主管批准驳回状态
@bp.route('/UpdateHtpAgree',methods=["POST"])
def UpdateHtpAgree():
    id = request.json.get('id')
    htp_agree = request.json.get('htp_agree')
    day = request.json.get('day')
    update_punch = PunchModel.query.filter_by(id=id,day=day).first()
    update_punch.htp_agree = htp_agree
    db.session.commit()
    return json.dumps({"code":20000}, ensure_ascii=False)


# 查询当前登录用户的一周打卡审批情况
@bp.route('/SelectApproval',methods=["POST"])
def SelectApproval():
    request_token = request.json.get('token')
    token_id = request_token.split('_')[0]
    punchs = PunchModel.query.order_by(db.desc(PunchModel.day)).filter_by(id=token_id).all()
    items = [{'day':punch.day,
            'go_time':punch.go_time,
            'leave_time':punch.leave_time,   
            'intervals':punch.intervals,
            'grp_agree': punch.grp_agree,
            'htp_agree': punch.htp_agree,
            } for punch in punchs]
    return json.dumps({"code":20000,"items":items[:7]}, ensure_ascii=False)