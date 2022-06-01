from flask import Flask,render_template #引入模板插件
import config
from exts import db,mail
from blueprints import user_bp,employ_bp,punch_bp
from flask_cors import CORS  #Flask的跨域问题
from flask_migrate import Migrate

# 应用配置信息
app = Flask(__name__,
            static_folder='./dist',  #设置静态文件夹目录
            template_folder = "./dist",
            static_url_path="")
app.config.from_object(config)
db.init_app(app)

mail.init_app(app)

CORS(app, supports_credentials=True) 

migrate = Migrate(app, db)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(employ_bp)
app.register_blueprint(punch_bp)

@app.route('/')
def index():
    return render_template('index.html',name='index') #使用模板插件，引入index.html。此处会自动Flask模板文件目录寻找index.html文件。

if __name__ == '__main__':
    app.run()