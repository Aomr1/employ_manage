<template>
  <div class="register-container">
    <el-form
      ref="ruleForm"
      :model="ruleForm"
      status-icon
      :rules="rules"
      label-width="100px"
      class="bg-reg"
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="ruleForm.username"
          placeholder="请输入用户名"
        />
      </el-form-item>
      <el-form-item label="密码" prop="pass">
        <el-input
          v-model="ruleForm.pass"
          type="password"
          autocomplete="off"
          show-password
          placeholder="请输入密码"
        />
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input
          v-model="ruleForm.checkPass"
          type="password"
          autocomplete="off"
          show-password
          placeholder="请再次输入密码"
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

      <el-row :gutter="0">
        <el-col :span="14">
          <el-form-item label="部门/职位" prop="department">
            <el-select v-model="ruleForm.department" placeholder="请选择所在部门">
              <el-option label="财务部" value="财务部" />
              <el-option label="技术部" value="技术部" />
              <el-option label="后勤部" value="后勤部" />
              <el-option label="营销部" value="营销部" />
              <el-option label="人力资源部" value="人力资源部" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item prop="identity" label-width="30px">
            <el-select v-model="ruleForm.identity" placeholder="请选择当前职位">
              <el-option label="员工" value="员工" />
              <el-option label="小组长" value="小组长" />
              <el-option label="主管" value="主管" />
              <el-option label="老板" value="老板" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item>
        <el-col :span="8">
          <el-button type="primary" @click="submitForm('ruleForm')">注册</el-button>
        </el-col>
        <el-col :span="8">
          <el-button type="primary" @click="ReturnLogin()">返回</el-button>
        </el-col>
        <el-col :span="8">
          <el-button type="primary" @click="resetForm('ruleForm')">重置</el-button>
        </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Register',
  data() {
    var checkAge = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('年龄不能为空'))
      }
      setTimeout(() => {
        if (!Number.isInteger(value)) {
          callback(new Error('请输入数字值'))
        } else {
          if (value < 18) {
            callback(new Error('必须年满18岁'))
          } else {
            callback()
          }
        }
      }, 1000)
    }
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
      content: '发送验证码',
      totalTime: 10,
      canClick: false,
      ruleForm: {
        username: '',
        pass: '',
        checkPass: '',
        email: '',
        code: '',
        department: '',
        identity: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名称', trigger: 'blur' },
          { min: 3, max: 15, message: '长度在 3 到 15 个字符', trigger: 'blur' }
        ],
        pass: [{ validator: validatePass, trigger: 'blur' }],
        checkPass: [{ validator: validatePass2, trigger: 'blur' }],
        age: [{ validator: checkAge, trigger: 'blur' }],
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
        department: [
          { required: true, message: '请选择部门', trigger: 'blur' }
        ],
        identity: [
          { required: true, message: '请选择职位', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm(formName) {
      const path = 'http://127.0.0.1:5000/User/Register'

      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post(path, this.ruleForm).then((response) => {
            if (response.data === 'codeError') {
              this.$message({
                message: '验证码错误!',
                center: true,
                type: 'error'
              })
            } else if (response.data.msg === '注册成功') {
              this.$message({
                message: '恭喜你,注册成功!',
                center: true,
                type: 'success'
              })
              this.$router.push({
                path: '/'
              })
            } else {
              this.$message({
                message: '改账号已经存在!',
                center: true,
                type: 'warning'
              })
            }
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },

    /* 发送验证码 */
    getCode() {
      if (this.ruleForm.email) {
        if (this.canClick) return
        this.$message({
          message: '验证码发送成功!',
          center: true,
          type: 'success'
        })
        const path = 'http://127.0.0.1:5000/User/SendMail'
        axios.post(path, { mail: this.ruleForm.email })
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
    },
    ReturnLogin() {
      this.$router.push(
        { name: 'Login' }
      )
    }
  }
}
</script>

<style>
.register-container{
    min-height: 100%;
    width: 100%;
    background: url("../../assets/bg.jpg");
    background-size: 100% 100%;

}

.register-container .el-form{
    position: fixed;
    left: 0px;
    right: 0px;
    margin-left: auto;
    margin-right: auto;
    top: 80px;
    width: 500px;
    height: 540px;
}

.bg-reg {
  /* background-color: rgba(245, 243, 247, 1); */
  border: 1px solid #dcdfe6;
  padding-right: 80px;
  padding-top: 40px;
  padding-bottom: 10px;
  color: aliceblue;
}

/*  #改变label字体 */
.el-form-item__label,
.el-radio__label {
  color: rgb(9, 9, 9);
}

.el-input__inner {
  height: 47px;
  background-color: rgba(255, 255, 255, 0.93);
}

</style>
