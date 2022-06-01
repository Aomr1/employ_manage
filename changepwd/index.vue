<template>
  <div class="changepwd-container">
    <div class="changepwd-box">
      <el-steps :active="active" finish-status="success" process-status="process">
        <el-step title="验证身份" />
        <el-step title="找回密码" />
        <el-step title="完成" />
      </el-steps>

      <el-form ref="ruleForm" :model="ruleForm" status-icon :rules="rules" label-width="100px" class="demo-ruleForm">
        <div v-if="active==0">
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="ruleForm.username"
              placeholder="请输入用户名"
            />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="ruleForm.email" placeholder="请输入邮箱地址" />
          </el-form-item>
          <el-form-item label="验证码" prop="code">
            <el-input v-model="ruleForm.code" clearable placeholder="请输入验证码">
              <el-button
                slot="append"
                type="info"
                :disabled="canClick"
                @click="getCode"
              >
                {{ content }}
              </el-button>
            </el-input>
          </el-form-item>
          <el-row>
            <el-col :span="8" offset="6">
              <el-button type="primary" onclick="javascript:history.go(-1);">返回</el-button>
            </el-col>
            <el-col :span="8" offset="1">
              <el-button type="primary" @click="next">下一步</el-button>
            </el-col>
          </el-row>
        </div>

        <div v-if="active==1">

          <el-form-item label="新密码" prop="pass">
            <el-input
              v-model="ruleForm.pass"
              type="password"
              autocomplete="off"
              show-password
              placeholder="请输入密码"
            />
          </el-form-item>
          <el-form-item label="确认新密码" prop="checkPass">
            <el-input
              v-model="ruleForm.checkPass"
              type="password"
              autocomplete="off"
              show-password
              placeholder="请再次输入密码"
            />
          </el-form-item>
          <el-row>
            <el-col :span="8" offset="6">
              <el-button type="primary" onclick="javascript:history.go(-1);">返回</el-button>
            </el-col>
            <el-col :span="8" offset="1">
              <el-button type="primary" @click="next">下一步</el-button>
            </el-col>
          </el-row>
        </div>
      </el-form>

      <div v-show="active==2" class="flex-contain">
        <div>        <el-progress type="dashboard" :percentage="percentage" />
          <div>正在返回登陆页面</div></div>

      </div>

    </div>
  </div>

</template>

<script>
import axios from 'axios'
export default {
  name: 'Changepwd',
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      clock: '',
      percentage: 0,
      active: 0,
      canClick: false,
      content: '发送验证码',
      totalTime: 10,
      VerificationCode: '',
      ruleForm: {
        username: '',
        email: '',
        code: '',
        pass: '',
        checkPass: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名称', trigger: 'blur' },
          { min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          {
            type: 'email',
            message: '请输入正确的邮箱地址',
            trigger: ['blur', 'change']
          }
        ],
        code: [
          { required: true, message: '请输入邮箱验证码', trigger: 'blur' },
          { min: 6, max: 6, message: '验证码长度为6', trigger: 'blur' }
        ],
        pass: [{ required: true, validator: validatePass, trigger: 'blur' }],
        checkPass: [{ required: true, validator: validatePass2, trigger: 'blur' }]
      }
    }
  },
  watch: {
    percentage(newvalue, oldvalue) {
      if (newvalue === 100) {
        window.clearInterval(this.clock)
        this.$router.push({ path: '/login' })
      }
    }
  },
  methods: {
    changepwd() {
      const path = 'http://127.0.0.1:5000/User/ChangePwd'
      axios.post(path, this.ruleForm).then(
        (response) => {
          if (response.data['code'] === 20000) {
            this.$message({
              message: '密码修改成功！',
              center: true,
              type: 'success'
            })
          }
        }
      )
    },
    next() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          if (this.active === 0) {
            if (this.ruleForm.code === this.VerificationCode.toString()) {
              this.active = this.active + 1
              this.$message({
                message: '验证成功！',
                center: true,
                type: 'success'
              })
            } else {
              this.$message({
                message: '验证码错误！',
                center: true,
                type: 'error'
              })
            }
          } else if (this.active === 1) {
            this.changepwd()
            this.active = this.active + 1
            this.clock = window.setInterval(() => { this.percentage++ }, 50)
          } else {
            console.log('结束')
          }
        } else {
          return false
        }
      })
    },
    getCode() {
      if (this.ruleForm.email) {
        if (this.canClick) return
        this.$message({
          message: '验证码发送成功!',
          center: true,
          type: 'success'
        })
        const path = 'http://127.0.0.1:5000/User/SendMail'
        axios.post(path, { mail: this.ruleForm.email }).then(
          (response) => {
            this.VerificationCode = response.data['VerificationCode']
          }
        )
        this.canClick = true
        this.content = this.totalTime + 's后重新发送'
        const clock = window.setInterval(() => {
          this.totalTime--
          this.content = this.totalTime + 's后重新发送'
          if (this.totalTime < 0) {
            window.clearInterval(clock)
            this.content = '重新发送验证码'
            this.totalTime = 10
            this.canClick = false
          }
        }, 1000)
      } else {
        this.$message({
          message: '邮箱未输入，请输入邮箱！',
          center: true,
          type: 'error'
        })
      }
    }
  }
}
</script>

<style>

  .changepwd-container {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: url("../../assets/bg.jpg");
    background-size: 100% 100%;
  }
  .changepwd-box {
    border: 1px solid #dcdfe6;
    width: 480px;
    margin: 170px auto;
    padding: 35px 15px 15px 15px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }
  .login-title {
    text-align: center;
    margin: 0 auto 40px 60px;
    color: #303133;
  }
/*  #改变label字体 */
.el-form-item__label,
.el-radio__label {
  color: rgb(2, 2, 2);
}

.el-input__inner {
  height: 47px;
  background-color: rgba(255, 255, 255, 0.93);
}

.changepwd-container .el-input{
    width: 80%;
}

.changepwd-container .flex-contain{
    display: flex;
    justify-content:center;
    flex-direction:row
}
</style>
