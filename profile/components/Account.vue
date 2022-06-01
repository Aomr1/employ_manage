<template>
  <div class="app-container">
    <div class="form_box">
      <el-form
        ref="ruleForm"
        :model="ruleForm"
        :rules="rules"
        label-width="100px"
        class="demo-ruleForm"
        status-icon
        label-position="left"
      >
        <el-row :gutter="20" style="margin-top: 40px">
          <el-col :span="9" :offset="3">
            <el-form-item label="员工姓名" prop="name">
              <el-input v-model="ruleForm.name" />
            </el-form-item>
            <el-form-item label="入职时间" required prop="entrytime">
              <el-date-picker
                v-model="ruleForm.entrytime"
                type="date"
                value-format="yyyy-MM-dd"
                placeholder="选择入职时间"
                style="width: 100%"
              />
            </el-form-item>

            <el-form-item label="出生日期" required prop="birthday">
              <el-date-picker
                v-model="ruleForm.birthday"
                type="date"
                value-format="yyyy-MM-dd"
                placeholder="选择出生日期"
                style="width: 100%"
              />
            </el-form-item>

            <el-form-item label="电子邮箱" prop="mail">
              <el-input v-model="ruleForm.mail" />
            </el-form-item>

            <el-form-item label="毕业学校" prop="school">
              <el-input v-model="ruleForm.school" />
            </el-form-item>

            <el-form-item label="员工备注" prop="remark">
              <el-input
                v-model="ruleForm.remark"
                type="textarea"
                :rows="7"
                clearable
              />
            </el-form-item>
          </el-col>
          <el-col :span="9" :offset="3">
            <el-form-item label="性别" prop="sex">
              <el-radio-group v-model="ruleForm.sex">
                <el-radio label="男" />
                <el-radio label="女" />
              </el-radio-group>
            </el-form-item>

            <el-form-item label="婚姻状态" prop="marriage">
              <el-radio-group v-model="ruleForm.marriage">
                <el-radio label="已婚" />
                <el-radio label="未婚" />
              </el-radio-group>
            </el-form-item>

            <el-form-item label="员工星级" prop="imp">
              <el-rate
                v-model="ruleForm.imp"
                :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                :max="5"
                style="margin-top: 11px"
              />
            </el-form-item>
            <el-form-item label="学历" prop="education">
              <el-select
                v-model="ruleForm.education"
                placeholder="请选择员工学历"
              >
                <el-option label="博士" value="博士" />
                <el-option label="硕士" value="硕士" />
                <el-option label="本科" value="本科" />
                <el-option label="专科" value="专科" />
              </el-select>
            </el-form-item>

            <el-form-item label="部门" prop="department">
              <el-select
                v-model="ruleForm.department"
                placeholder="请选择员工部门"
              >
                <el-option label="财务部" value="财务部" />
                <el-option label="技术部" value="技术部" />
                <el-option label="后勤部" value="后勤部" />
                <el-option label="营销部" value="营销部" />
                <el-option label="人力资源部" value="人力资源部" />
              </el-select>
            </el-form-item>

            <el-form-item label="员工状态" prop="state">
              <el-select v-model="ruleForm.state" placeholder="请选择员工状态">
                <el-option label="执勤" value="执勤" />
                <el-option label="休假" value="休假" />
              </el-select>
            </el-form-item>

            <el-form-item label="来源地" prop="home">
              <el-cascader
                v-model="selectedAddressOptions"
                placeholder="请选择来源地"
                size="large"
                :options="options"
                @change="handleChange"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 20px">
          <el-form-item>
            <el-col :span="8" :offset="4">
              <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
            </el-col>
            <el-col :span="12">
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-col>
          </el-form-item>
        </el-row>
      </el-form>
    </div>
  </div>
</template>

<script>
import {
  provinceAndCityData,
  CodeToText
} from 'element-china-area-data'
export default {
  name: 'Account',
  data() {
    return {
      ruleForm: {
        name: this.$store.state.user.name,
        sex: this.$store.state.user.sex,
        marriage: this.$store.state.user.marriage,
        education: this.$store.state.user.education,
        mail: this.$store.state.user.mail,
        imp: this.$store.state.user.imp,
        department: this.$store.state.user.department,
        state: this.$store.state.user.zt_state,
        entrytime: this.$store.state.user.entrytime,
        birthday: this.$store.state.user.birthday,
        school: this.$store.state.user.school,
        home: '',
        remark: this.$store.state.user.remark
      },
      rules: {
        name: [{ required: true, message: '请输入员工姓名', trigger: 'blur' }],
        sex: [{ required: true, message: '请选择性别', trigger: 'change' }],
        marriage: [
          { required: true, message: '请选择婚姻状态', trigger: 'change' }
        ],
        education: [
          { required: true, message: '请选择员工学历', trigger: 'change' }
        ],
        imp: [{ required: true, message: '请选择员工星级', trigger: 'blur' }],
        department: [
          { required: true, message: '请选择员工部门', trigger: 'change' }
        ],
        state: [
          { required: true, message: '请选择员工状态', trigger: 'change' }
        ],
        entrytime: [
          {
            required: true,
            message: '请选择入职时间',
            trigger: 'blur'
          }
        ],
        birthday: [
          {
            required: true,
            message: '请选择出生日期',
            trigger: 'blur'
          }
        ],
        mail: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' }
        ],
        school: [
          { required: true, message: '请输入员工毕业学校', trigger: 'blur' }
        ],
        home: [
          { required: true, message: '请选择员工来源地', trigger: 'blur' }
        ],
        remark: [
          { required: true, message: '请输入员工备注', trigger: 'blur' }
        ]
      },
      options: provinceAndCityData,
      selectedAddressOptions: []
    }
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  destroyed() {
    clearInterval(this.timer)
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios
            .post('http://127.0.0.1:5000/Employ/FormSubmit', {
              ruleForm: this.ruleForm,
              token: this.$store.state.user.token
            })
            .then((response) => {
              if (response.data.code === 200) {
                this.$message({
                  message: '提交成功',
                  center: true,
                  type: 'success'
                })
              }
              /* this.$refs[formName].resetFields() */
              location.reload()
            })
        } else {
          this.$message({
            message: '存在字段未输入，请重新尝试！',
            center: true,
            type: 'error'
          })
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    handleChange() {
      var name = ''
      this.selectedAddressOptions.map(
        (item) => (name += CodeToText[item] + ' ')
      )
      this.ruleForm.home = name
      // var addressStr= new Array(); //定义一数组
      // addressStr=(this.form.address).split("/"); //字符分割
      // this.selectedAddressOptions=TextToCode[addressStr[0]][addressStr[1]].code;
    }
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
</style>

