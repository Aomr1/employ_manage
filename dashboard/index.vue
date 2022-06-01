<template>
  <div class="dashboard-editor-container app-container">
    <el-row :gutter="30">
      <el-col :xs="{span: 24}" :sm="{span: 10}" :md="{span: 10}" :lg="{span: 10}" :xl="{span: 6}" style="margin-bottom:30px;">
        <Main />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 14}" :md="{span: 14}" :lg="{span: 14}" :xl="{span: 6}" style="margin-bottom:30px;">
        <Notice />
      </el-col>
    </el-row>
    <el-row :gutter="30">
      <el-col :xs="{span: 24}" :sm="{span: 10}" :md="{span: 10}" :lg="{span: 10}" :xl="{span: 6}" style="margin-bottom:30px;">
        <todo-list />
      </el-col>
      <el-col :xs="{span: 24}" :sm="{span: 14}" :md="{span: 14}" :lg="{span: 14}" :xl="{span: 6}" style="margin-bottom:30px;">
        <Calendar />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Main from './components/Main'
import TodoList from './components/TodoList'
import Notice from './components/Notice'
import Calendar from './components/Calendar'

export default {
  name: 'Dashboard',
  components: {
    Main,
    TodoList,
    Notice,
    Calendar
  }
}
</script>

<style lang="scss" scoped>
.dashboard-editor-container {
  padding: 30px;
  background-color: rgb(240, 242, 245);
  position: relative;
}

@media (max-width:1024px) {
  .chart-wrapper {
    padding: 16px;
  }
}
</style>
