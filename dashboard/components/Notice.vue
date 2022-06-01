<template>
  <el-card shadow="hover" class="notice">
    <div slot="header" class="clearfix">
      <mallki class-name="mallki-text" text="通知公告" />
    </div>
    <el-table :data="tableData" :show-header="false" highlight-current-row style="width: 100%">
      <el-table-column label="标题" min-width="576">
        <template slot-scope="scope"><el-link :href="scope.row.href" target="_blank" :underline="false">{{ scope.row.name }}</el-link></template>
      </el-table-column>
      <el-table-column label="时间" width="95">
        <template slot-scope="scope">
          {{ scope.row.date }}
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script>
import Mallki from '@/components/TextHoverEffect/Mallki'

export default {
  components: { Mallki },
  data() {
    return {
      tableData: [
        {
          date: '2022-05-04',
          name: '关于组织申报第五届教学成果奖暨福建省2022年高等教育教学成果奖推荐申报工作的通知',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7307.htm'
        },
        {
          date: '2022-05-03',
          name: '集美大学诚毅学院“信仰永恒”诗文朗诵会',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7300.htm'
        },
        {
          date: '2022-05-03',
          name: '集美大学诚毅学院2022年普通高考招生章程',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7292.htm'
        },
        {
          date: '2022-05-03',
          name: '关于开展2021年度福建省优秀科普作品评选活动的通知',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7289.htm'
        },
        {
          date: '2022-04-28',
          name: '2022年“五一”国际劳动节图书馆开放通知',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7273.htm'
        },
        {
          date: '2022-04-27',
          name: '景祺楼消防联动测试公告',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7261.htm'
        },
        {
          date: '2022-04-22',
          name: '关于2022年“五一”国际劳动节放假的通知',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7248.htm'
        },
        {
          date: '2022-04-21',
          name: '项目申报：关于组织申报2022年技术创新重点攻关及产业化项目的通知',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7241.htm'
        },
        {
          date: '2022-04-19',
          name: '关于开展诚毅学院“声润书香”校园朗读大赛的通知',
          href: 'http://chengyi.jmu.edu.cn/info/1055/7230.htm'
        }
      ]
    }
  }
}
</script>

<style scoped>
  .notice a {
    text-decoration:none;
    -webkit-transition: padding .4s;
    -moz-transition: padding .4s;
    -o-transition: padding .4s;
    transition: padding .4s;
  }
  .notice a:hover{
    color:#006DC8;
    padding-left: 6px;
  }
</style>
