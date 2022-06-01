<template>
  <div class="app-container">
    <div v-if="user">
      <el-row :gutter="20">
        <el-col :span="15" :offset="2" :xs="24">
          <el-card>
            <div class="user-bio">
              <div class="user-skills user-bio-section">
                <div class="user-bio-section-header">
                  <svg-icon icon-class="profile" /><span style="font-size:large">个人信息</span>
                </div>
                <div class="user-bio-section-body">
                  <el-tabs v-model="activeTab">
                    <el-tab-pane label="个人资料" name="mycard">
                      <my-card />
                    </el-tab-pane>
                    <el-tab-pane label="修改资料" name="account">
                      <account />
                    </el-tab-pane>
                    <el-tab-pane label="修改密码" name="changepwd">
                      <change-pwd />
                    </el-tab-pane>
                    <el-tab-pane label="社区消息" name="activity">
                      <activity />
                    </el-tab-pane>
                    <el-tab-pane label="审批情况" name="timeline">
                      <timeline />
                    </el-tab-pane>
                  </el-tabs>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="5" :xs="24">
          <punch-card v-if="roles[0]!='老板'" />
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import MyCard from './components/MyCard'
import Activity from './components/Activity'
import Timeline from './components/Timeline'
import PunchCard from './components/PunchCard.vue'
import Account from './components/Account.vue'
import ChangePwd from './components/ChangePwd.vue'

export default {
  name: 'Profile',
  components: { Activity, Timeline, PunchCard, Account, MyCard, ChangePwd },
  data() {
    return {
      user: {},
      activeTab: 'mycard'
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles',
      'id',
      'department'
    ])
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
</style>
