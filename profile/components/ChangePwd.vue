<template>
  <div class="chpwd">
    <el-form ref="ruleForm" :model="ruleForm" status-icon :rules="rules" label-width="100px" class="demo-ruleForm">

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
      <el-button type="primary" @click="changepwd">点击修改</el-button>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios'
export default {
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
      ruleForm: {
        username: this.$store.state.user.name,
        email: this.$store.state.user.mail,
        pass: '',
        checkPass: ''
      },
      rules: {
        pass: [{ required: true, validator: validatePass, trigger: 'blur' }],
        checkPass: [{ required: true, validator: validatePass2, trigger: 'blur' }]
      }
    }
  },
  methods: {
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login?redirect=${this.$route.fullPath}`)
    },
    changepwd() {
      const path = 'http://127.0.0.1:5000/User/ChangePwd'
      axios.post(path, this.ruleForm).then(
        (response) => {
          if (response.data['code'] === 20000) {
            this.$message({
              message: '密码修改成功！\n 请重新登录',
              center: true,
              type: 'success'
            })
          }
          this.logout()
        }
      )
    },
    handle() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.changepwd()
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style>
/* .chpwd{
    display: flex;
    justify-content:center;
    flex-direction:row
} */
.chpwd .el-input{
    width: 80%;
}
</style>
