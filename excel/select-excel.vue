<template>
  <div class="app-container">
    <label class="radio-label" style="padding-left:0;">文件名: </label>
    <el-input v-model="filename" placeholder="请输入文件名（默认employees-list）" style="width:350px;" prefix-icon="el-icon-document" />
    <el-button :loading="downloadLoading" style="margin-bottom:20px" type="primary" icon="el-icon-document" @click="handleDownload">
      导出选定项
    </el-button>
    <el-table
      ref="multipleTable"
      v-loading="listLoading"
      :data="list"
      element-loading-text="拼命加载中"
      border
      fit
      highlight-current-row
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" align="center" />
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="100px">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="姓名" width="120px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="性别" width="100px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.sex }}</span>
        </template>
      </el-table-column>
      <el-table-column label="学历" width="100px" align="center">
        <template slot-scope="{row}">
          <span>
            {{ row.education }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="员工星级" width="110px" align="center">
        <template slot-scope="{row}">
          <!-- <el-rate v-model="row.imp" disabled show-score text-color="#ff9900" /> -->
          <svg-icon v-for="n in row.imp" :key="n" icon-class="star" class="meta-item__icon" />
        </template>
      </el-table-column>
      <el-table-column label="部门" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.department }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" class-name="status-col" width="100px" align="center">
        <template slot-scope="{row}">
          <span>
            {{ row.state }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="入职时间" width="160px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.entrytime }}</span>
        </template>
      </el-table-column>
      <el-table-column label="出生日期" width="160px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.birthday }}</span>
        </template>
      </el-table-column>
      <el-table-column label="毕业学校" min-width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.school }}</span>
        </template>
      </el-table-column>
      <el-table-column label="生源地址" min-width="300px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.home }}</span>
        </template>
      </el-table-column>
      <el-table-column label="婚姻状态" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.marriage }}</span>
        </template>
      </el-table-column>
      <el-table-column label="备注" min-width="600px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.remark }}</span>
        </template>
      </el-table-column>
      <el-table-column label="创建信息时间" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.creatime | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>

export default {
  name: 'SelectExcel',
  data() {
    return {
      list: null,
      listLoading: true,
      multipleSelection: [],
      downloadLoading: false,
      filename: '',
      listQuery: {
        page: 1,
        sort: '+id'
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      this.$axios
        .post('http://127.0.0.1:5000/Employ/SelectEmployee', {
          listQuery: this.listQuery
        })
        .then((response) => {
          if (response.data.code === 20000) {
            // console.log(response.data)
            this.list = response.data.items
            this.listLoading = false
          }
        })
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    handleDownload() {
      if (this.multipleSelection.length) {
        this.downloadLoading = true
        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = ['id', 'name', 'sex', 'education', 'imp', 'department', 'state', 'entrytime', 'birthday', 'school', 'home', 'marriage', 'remark', 'creatime']
          const filterVal = ['id', 'name', 'sex', 'education', 'imp', 'department', 'state', 'entrytime', 'birthday', 'school', 'home', 'marriage', 'remark', 'creatime']
          const list = this.multipleSelection
          const data = this.formatJson(filterVal, list)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: this.filename
          })
          this.$refs.multipleTable.clearSelection()
          this.downloadLoading = false
        })
      } else {
        this.$message({
          message: '请选择您要导出的内容',
          type: 'warning',
          center: true
        })
      }
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => v[j]))
    }
  }
}
</script>
