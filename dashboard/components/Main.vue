<template>
  <el-card shadow="hover">
    <div slot="header" class="clearfix">
      <mallki class-name="mallki-text" text="用户简介" />
    </div>
    <el-row :gutter="32">
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 12}" :xl="{span: 6}">
        <div class="user-profile">
          <div class="box-center">
            <el-image style="width: 140px; height: 140px; border-radius:70px" :src="avatar" />
          </div>
        </div>
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 12}" :md="{span: 12}" :lg="{span: 12}" :xl="{span: 6}" style="margin-top: 15px;">
        <div class="user-profile">
          <div class="user-bio-first">
            <div class="user-education user-bio-section">
              <div class="user-bio-section-header"><svg-icon icon-class="user" /><span>用户信息</span></div>
            </div>
          </div>
          <div class="box-center">
            <div class="user-name text-center">{{ name }}</div>
          </div>
          <div class="user-bio-first">
            <div class="user-education user-bio-section">
              <div class="user-bio-section-header"><svg-icon icon-class="department" /><span>身份</span></div>
            </div>
          </div>
          <div class="box-center">
            <div class="user-department">{{ roles[0] }}</div>
          </div>
          <div class="user-bio-first">
            <div class="user-education user-bio-section">
              <div class="user-bio-section-header"><svg-icon icon-class="example" /><span>所在部门</span></div>
            </div>
          </div>
          <div class="box-center">
            <div class="user-department">{{ department }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="user-bio">
      <div class="user-skills user-bio-section">
        <div class="user-bio-section-header"><svg-icon icon-class="education" />
          <span>职业技能</span>
        </div>
        <div class="user-bio-section-body">
          <div class="progress-item">
            <span>Vue-Admin</span>
            <el-progress :percentage="90" />
          </div>
          <div class="progress-item">
            <span>Vue</span>
            <el-progress :percentage="80" />
          </div>
          <div class="progress-item">
            <span>Python</span>
            <el-progress :percentage="70" />
          </div>
          <div class="progress-item">
            <span>Flask</span>
            <el-progress :percentage="60" />
          </div>
          <div class="progress-item">
            <span>JavaScript</span>
            <el-progress :percentage="50" />
          </div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import { mapGetters } from 'vuex'
import Mallki from '@/components/TextHoverEffect/Mallki'

export default {
  components: { Mallki },
  computed: {
    ...mapGetters([
      'avatar', 'name', 'roles', 'department'
    ])
  }
}
</script>

<style lang="scss" scoped>
.box-center {
  margin: 0 auto;
  display: table;
}

.user-profile {
  .user-name {
    font: inherit;
    font-weight: 500;
    color: #303133;
    font-size: 18px;
    text-align: center;
    padding-bottom: 10px;
  }

  .box-center {
    margin-top: 8px;
  }

  .user-department {
    font: inherit;
    font-weight: 500;
    color: #303133;
    font-size: 18px;
    text-align: center;
    padding-bottom: 10px;
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
.user-bio-first {
  color: #606266;

  span {
    padding-left: 4px;
  }

  .user-bio-section {
    font-size: 14px;
    .user-bio-section-header {
      border-bottom: 1px solid #dfe6ec;
      padding-bottom: 10px;
      margin-bottom: 10px;
      font-weight: bold;
    }
  }
}
</style>
