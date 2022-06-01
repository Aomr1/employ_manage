<template>
  <el-card shadow="hover">
    <div slot="header" class="clearfix">
      <mallki class-name="mallki-text" text="日历" />
    </div>
    <el-calendar>
      <template slot="dateCell" slot-scope="{data}">
        {{ data.day.split('-').slice(1).join('-') }}
        <div v-for="(item,index) in scheduleData" :key="index">
          <el-tag v-if="(item.workingDay).indexOf(data.day.split('-').slice(2).join('-'))!=-1" type="primary">
            {{ item.content }}
          </el-tag>
        </div>
      </template>
    </el-calendar>
  </el-card>
</template>

<script>
import Mallki from '@/components/TextHoverEffect/Mallki'

export default {
  components: { Mallki },
  data() {
    return {
      value: new Date(),
      scheduleData: [
        {
          workingDay: '11',
          content: '汇报日期'
        }
      ]
    }
  }
}
</script>

<style scoped>
  /deep/ .el-calendar-day {
    text-align: center;
    box-sizing: border-box;
    padding: 9px;
    height: 70px;
  }
</style>
