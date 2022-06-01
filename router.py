
#普通员工
employee_data =  {
        "list":[
                {
                    "path": "/",
                    "component": "Layout",
                    "redirect": "/dashboard",
                    "name": "Home",
                    "children": [
                        {
                            "path": "/dashboard",
                            "name": "Dashboard",
                            "component": "views/dashboard/index",
                            "meta": {
                                "title": "首页",
                                "icon": "dashboard"
                                }   
                        }
                    ]
                },
                {
                    "path": "/profile",
                    "component": "Layout",
                    "children": [
                        {
                            "path": "/profile",
                            "name": "Profile",
                            "component": "views/profile/index",
                            "meta": {
                                "title": "个人中心",
                                "icon": "user"
                            }
                        }
                    ]
                },
            ]
        }


#小组长
groupleader_data =  {
        "list":[
                {
                    "path": "/",
                    "component": "Layout",
                    "redirect": "/dashboard",
                    "name": "Home",
                    "children": [
                        {
                            "path": "/dashboard",
                            "name": "Dashboard",
                            "component": "views/dashboard/index",
                            "meta": {
                                "title": "首页",
                                "icon": "dashboard"
                                }   
                        }
                    ]
                },
                {
                    "path": "/profile",
                    "component": "Layout",
                    "children": [
                        {
                            "path": "/profile",
                            "name": "Profile",
                            "component": "views/profile/index",
                            "meta": {
                                "title": "个人中心",
                                "icon": "user"
                            }
                        }
                    ]
                },
                {
                    "path": "/punch",
                    "component": "Layout",
                    "children": [
                        {
                            "path": "/punch",
                            "name": "Punch",
                            "component": "views/punch/index",
                            "meta": {
                                "title": "打卡管理",
                                "icon": "punch"
                            }
                        }
                    ]
                },
            ]
        }

#高管
highleader_data =  {
        "list":[
                {
                    "path": "/",
                    "component": "Layout",
                    "redirect": "/dashboard",
                    "name": "Home",
                    "children": [
                        {
                            "path": "/dashboard",
                            "name": "Dashboard",
                            "component": "views/dashboard/index",
                            "meta": {
                                "title": "首页",
                                "icon": "dashboard"
                                }   
                        }
                    ]
                },
                {
                    "path": "/profile",
                    "component": "Layout",
                    "children": [
                        {
                            "path": "/profile",
                            "name": "Profile",
                            "component": "views/profile/index",
                            "meta": {
                                "title": "个人中心",
                                "icon": "user"
                            }
                        }
                    ]
                },
                {
                    "path": "/punch",
                    "component": "Layout",
                    "children": [
                        {
                            "path": "/punch",
                            "name": "Punch",
                            "component": "views/punch/index",
                            "meta": {
                                "title": "打卡管理",
                                "icon": "punch"
                            }
                        }
                    ]
                },
            ]
        }

#最高领导层（老板）
boss_data =  {
        "list":[
                {
                    "path": "/",
                    "component": "Layout",
                    "redirect": "/dashboard",
                    "name": "Home",
                    "children": [
                        {
                            "path": "/dashboard",
                            "name": "Dashboard",
                            "component": "views/dashboard/index",
                            "meta": {
                                "title": "首页",
                                "icon": "dashboard"
                                }   
                        }
                    ]
                },
                {
                    "path": "/form",
                    "component": "Layout",
                    "children": [
                        {
                            "path": "/form",
                            "name": "Form",
                            "component": "views/form/index",
                            "meta": {
                                "title": "表单提交",
                                "icon": "form"
                            }
                        }
                    ]
                },
                {
                    "path": "/setting",
                    "component": "Layout",
                    "name": "Setting",
                    "redirect": '/setting/table',
                    "meta": {
                        "title": "系统管理",
                        "icon": "el-icon-s-help"
                    },
                    "children": [
                        {
                            "path": "/setting/table",
                            "name": "Table",
                            "component": "views/table/index",
                            "meta": {
                                "title": "人员管理"
                            }
                        },
                        {
                            "path": "/setting/user",
                            "name": "User",
                            "component": "views/user/index",
                            "meta": {
                                "title": "用户管理"
                            }
                        },
                    ]
                },
                {
                    "path": "/chart",
                    "component": "Layout",
                    "name": "Chart",
                    "redirect": '/chart/keyboard',
                    "meta": {
                        "title": "数据统计",
                        "icon": "chart"
                    },
                    "children": [
                        {
                            "path": "/chart/keyboard",
                            "name": "KeyboardChart",
                            "component": "views/charts/keyboard",
                            "meta": {
                                "title": "键盘图表"
                            }
                        },
                        {
                            "path": "/chart/line",
                            "name": "LineChart",
                            "component": "views/charts/line",
                            "meta": {
                                "title": "折线图"
                            }
                        },
                        {
                            "path": "/chart/mix-chart",
                            "name": "MixChart",
                            "component": "views/charts/mix-chart",
                            "meta": {
                                "title": "混合图表"
                            }
                        },
                    ]
                },
                 {
                    "path": "/punch",
                    "component": "Layout",
                    "children": [
                        {
                            "path": "/punch",
                            "name": "Punch",
                            "component": "views/punch/index",
                            "meta": {
                                "title": "打卡管理",
                                "icon": "punch"
                            }
                        }
                    ]
                },
                {
                    "path": "/excel",
                    "component": "Layout",
                    "name": "Excel",
                    "redirect": '/excel/export-excel',
                    "meta": {
                        "title": "Excel",
                        "icon": "excel"
                    },
                    "children": [
                        {
                            "path": "/excel/export-excel",
                            "name": "ExportExcel",
                            "component": "views/excel/export-excel",
                            "meta": {
                                "title": "导出文件"
                            }
                        },
                        {
                            "path": "/excel/export-selected-excel",
                            "name": "SelectExcel",
                            "component": "views/excel/select-excel",
                            "meta": {
                                "title": "导出已选项"
                            }
                        },
                        {
                            "path": "/excel/upload-excell",
                            "name": "UploadExcel",
                            "component": "views/excel/upload-excel",
                            "meta": {
                                "title": "上传Excel"
                            }
                        },
                    ]
                },
                {
                    "path": "/profile",
                    "component": "Layout",
                    "children": [
                        {
                            "path": "/profile",
                            "name": "Profile",
                            "component": "views/profile/index",
                            "meta": {
                                "title": "个人中心",
                                "icon": "user"
                            }
                        }
                    ]
                }
            ]
        }

