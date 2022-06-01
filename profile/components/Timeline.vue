<template>
  <div class="block">
    <el-timeline>
      <el-timeline-item v-for="(item,index) of timeline" :key="index" :timestamp="item.day" placement="top">
        <el-card class="box-card">
          <h3>打卡情况</h3>
          <p>上班打卡时间：{{ item.go_time }} <el-divider direction="vertical" /> 下班打卡时间：{{ item.leave_time }} <el-divider direction="vertical" /> 工作时长：{{ item.intervals }}</p>
          <p v-if="roles[0] === '员工'">部门组长审批情况：{{ item.grp_agree | agreeFilter }}</p>
          <p v-if="roles[0] === '员工'">部门主管审批情况：{{ item.htp_agree | agreeFilter }}</p>

          <p v-if="roles[0] === '小组长'">部门主管审批情况：{{ item.htp_agree | agreeFilter }}</p>

          <p v-if="roles[0] === '主管'">老板审批情况：{{ item.htp_agree | agreeFilter }}</p>
        </el-card>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  filters: {
    agreeFilter(agree) {
      const agreeMap = {
        false: '驳回',
        true: '批准',
        agency: '代办'
      }
      return agreeMap[agree]
    }
  },
  data() {
    return {
      timeline: []
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles',
      'token',
      'department'
    ])
  },
  mounted() {
    this.getList()
  },
  methods: {
    getList() {
      this.$axios
        .post('http://127.0.0.1:5000/Punch/SelectApproval', {
          token: this.token
        })
        .then((response) => {
          this.timeline = response.data.items
        })
    }
  }
}
</script>

<style scoped>
  .box-card {
    width: 600px;
  }
  .el-timeline-item__timestamp {
    color: #909399;
    line-height: 1;
    font-size: 30px;
  }
</style>
