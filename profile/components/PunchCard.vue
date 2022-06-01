<template>
  <el-card style="margin-bottom:20px;">
    <div class="user-bio">
      <div class="user-skills user-bio-section">
        <div class="user-bio-section-header"><svg-icon icon-class="skill" /><span style="font-size:large">每日打卡</span></div>
        <div class="user-bio-section-body">
          <el-row>
            <el-col>
              <span class="username text-muted">签到人：</span>
              <el-tag type="info">
                {{ name }}
              </el-tag>
            </el-col>
          </el-row>
          <el-row style="margin-top:20px;">
            <div class="block">
              <span class="username text-muted">上班打卡时间：</span>
              <el-time-picker
                v-model="go_time"
                :picker-options="{selectableRange: '00:00:00 - 23:59:59'}"
                style="margin-top:10px;"
              />
            </div>
          </el-row>
          <el-row style="margin-top:20px;">
            <div class="block">
              <span class="username text-muted">下班打卡时间：</span>
              <el-time-picker
                v-model="leave_time"
                :picker-options="{selectableRange: '00:00:00 - 23:59:59'}"
                style="margin-top:10px;"
              />
            </div>
          </el-row>
          <el-row style="margin-top:20px;">
            <el-col>
              <el-button type="primary" icon="el-icon-s-flag" round @click="handlePunch">{{ content }}</el-button>
              <el-alert
                v-if="is_go_punch==='true' && is_leave_punch==='true'"
                title="打卡成功"
                type="success"
                :closable="false"
                :description="go_desc+leave_desc"
                show-icon
                style="margin-top:20px"
              />
            </el-col>
          </el-row>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import { mapGetters } from 'vuex'
import { parseTime } from '@/utils/index'

export default {
  data() {
    return {
      content: '点击打卡',
      go_time: null,
      leave_time: null,
      is_go_punch: '',
      is_leave_punch: '',
      desc_go_time: '',
      desc_leave_time: '',
      pickerOptions: {
        shortcuts: [
          {
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date())
            }
          },
          {
            text: '昨天',
            onClick(picker) {
              const date = new Date()
              date.setTime(date.getTime() - 3600 * 1000 * 24)
              picker.$emit('pick', date)
            }
          },
          {
            text: '一周前',
            onClick(picker) {
              const date = new Date()
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
              picker.$emit('pick', date)
            }
          }
        ]
      }
    }
  },
  computed: {
    go_desc() {
      return `上班打卡时间为：${this.desc_go_time}`
    },
    leave_desc() {
      return `下班打卡时间为：${this.desc_leave_time}`
    },
    ...mapGetters([
      'name',
      'avatar',
      'roles',
      'token',
      'department'
    ])
  },
  mounted() {
    this.GetIsPunch()
  },
  methods: {
    handlePunch() {
      if (this.go_time !== '1900-01-01 00:00:00' && this.leave_time !== '1900-01-01 00:00:00') {
        this.go_time = parseTime(this.go_time)
        this.leave_time = parseTime(this.leave_time)
        const day_today = parseTime(new Date())
        this.$confirm(`您选择的上班打卡时间为：${this.go_time.split(' ')[1]}，下班打卡时间为：${this.leave_time.split(' ')[1]}，请确认！`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            this.$axios.post('http://127.0.0.1:5000/Punch/GetPunch', {
              token: this.token,
              name: this.name,
              date: day_today,
              go_time: this.go_time,
              leave_time: this.leave_time,
              identity: this.roles[0],
              department: this.department
            })
              .then((response) => {
                this.desc_go_time = response.data.desc_go_time
                this.desc_leave_time = response.data.desc_leave_time
              })
            this.is_go_punch = 'true'
            this.is_leave_punch = 'true'
            this.go_content = '重新打卡'
            this.$message({
              type: 'success',
              center: true,
              message: `打卡成功！`
            })
          })
          .catch(() => {
            this.$message({
              type: 'info',
              center: true,
              message: '已取消打卡'
            })
          })
      } else {
        this.$message({
          type: 'info',
          center: true,
          message: '打卡时间未选择！'
        })
      }
    },
    GetIsPunch() {
      const day_today = parseTime(new Date())
      this.$axios.post('http://127.0.0.1:5000/Punch/GetIsPunch', {
        token: this.token,
        date: day_today
      })
        .then((response) => {
          this.is_go_punch = response.data.is_go_punch
          this.is_leave_punch = response.data.is_leave_punch
          this.go_time = parseTime(new Date(response.data.go_time))
          this.leave_time = parseTime(new Date(response.data.leave_time))
          this.desc_go_time = response.data.desc_go_time
          this.desc_leave_time = response.data.desc_leave_time
          if (this.is_go_punch === 'true' && this.is_leave_punch === 'true') {
            this.content = '重新打卡'
          }
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.box-center {
  margin: 0 auto;
  display: table;
}

.text-muted {
  color: #777;
}

.user-profile {
  .user-name {
    font-weight: bold;
  }

  .box-center {
    padding-top: 10px;
  }

  .user-role {
    padding-top: 10px;
    font-weight: 400;
    font-size: 14px;
  }

  .box-social {
    padding-top: 30px;

    .el-table {
      border-top: 1px solid #dfe6ec;
    }
  }

  .user-follow {
    padding-top: 20px;
  }
}

.user-bio {
  color: #606266;

  span {
    padding-left: 4px;
  }

  .user-bio-section {
    font-size: 14px;
    padding: 15px 0;

    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      font-weight: bold;
    }
  }
}
.username{
  font-size: 16px;
  color: #000;
}
.el-date-editor.el-input, .el-date-editor.el-input__inner {
  width: 200px;
}
.el-tag.el-tag--info {
  color: #606266;
  text-align: center;
}
.el-tag {
  font-size: 14px;
  text-align: center;
}
.el-alert {
  width: 230px;
}
</style>
