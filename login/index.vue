<template>
  <div class="login-container">
    <!--ref="loginForm"：表示为表单起个别名-->
    <el-form
      ref="loginForm"
      :rules="loginRules"
      :model="loginForm"
      label-width="80px"
      class="login-box"
    >
      <el-tooltip placement="top">
        <div slot="content">
          老板:aomr<br>
          主管(人力资源部):htp<br>
          小组长(人力资源部):grp<br>
          员工(人力资源部):emp<br>
          <br>
          测试员工(财务部):emp1,密码1<br>
          测试小组长(财务部):grp1,密码1<br>
          测试主管(财务部):htp1,密码1
        </div>
        <h2 class="login-title">欢迎登录</h2>
      </el-tooltip>
      <el-form-item label="账号:" prop="username">
        <el-input
          v-model="loginForm.username"
          type="text"
          placeholder="请输入账号"
        />
      </el-form-item>

      <el-form-item label="密码:" prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          autocomplete="off"
          show-password
          placeholder="请输入密码"
          @keyup.enter.native="handleLogin()"
        />
      </el-form-item>

      <el-form-item>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-button type="primary" @click="handleLogin()">登录</el-button>
          </el-col>
          <el-col :span="8" :offset="1">
            <el-button type="primary" @click="handleChangePwd()">修改密码</el-button>
          </el-col>
          <el-col :span="6" :offset="1">
            <el-button type="primary" @click="handleRegister()">注册</el-button>
          </el-col>
        </el-row>
      </el-form-item>
    </el-form>
  </div>

</template>

<script>

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 5, message: '长度在 2 到 5 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 1, max: 12, message: '长度在 1 到 12 个字符', trigger: 'blur' }
        ]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(() => {
            this.loading = false
          })
        } else {
          return false
        }
      })
    },
    handleRegister() {
      this.$router.push({ name: 'Register' })
    },
    handleChangePwd() {
      this.$router.push({ name: 'Changepwd' })
    }
  }
}
</script>

<style>

  .login-container {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: url("../../assets/bg.jpg");
    background-size: 100% 100%;
  }
  .login-box {
    border: 1px solid #dcdfe6;
    width: 430px;
    margin: 170px auto;
    padding: 35px 55px 15px 15px;
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
</style>
