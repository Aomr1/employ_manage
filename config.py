# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'employ_manage'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS=True

SQLALCHEMY_TRACK_MOOIFICATIONS = True

SECRET_KEY = "sdfsadfskrwerfj1233453345"

JSON_AS_ASCII = False


# 邮箱配置
# 我们项目中用的是QQ邮箱
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
#MAIL_DEBUG = True
MAIL_USERNAME = "" #在此处配置你的邮箱
MAIL_PASSWORD = "skavsbndfksibgcf"
MAIL_DEFAULT_SENDER = "" #在此处配置你的邮箱