<template>
  <div class="app-container">
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column label="用户ID" align="center">
        <template slot-scope="row">
          {{ row.id }}
        </template>
      </el-table-column>
      <el-table-column label="用户名" align="center">
        <template slot-scope="row">
          {{ row.username }}
        </template>
      </el-table-column>
      <el-table-column label="邮箱" align="center">
        <template slot-scope="row">
          <span>{{ row.mail }}</span>
        </template>
      </el-table-column>
      <el-table-column label="所在部门" align="center">
        <template slot-scope="row">
          {{ row.department }}
        </template>
      </el-table-column>
      <el-table-column label="身份" align="center">
        <template slot-scope="row">
          <el-tag :type="scope.row.identity | identityFilter">{{ row.identity }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  filters: {
    identityFilter(identity) {
      const identityMap = {
        员工: 'primary',
        组长: 'success',
        高管: 'warning',
        老板: 'danger'
      }
      return identityMap[identity]
    }
  },
  data() {
    return {
      list: null,
      listLoading: false
    }
  }
}
</script>
