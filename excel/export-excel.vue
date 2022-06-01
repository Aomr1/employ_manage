<template>
  <div class="app-container">

    <div>
      <FilenameOption v-model="filename" />
      <AutoWidthOption v-model="autoWidth" />
      <BookTypeOption v-model="bookType" />
      <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="el-icon-document" @click="handleDownload">
        导出文件
      </el-button>
    </div>

    <el-table v-loading="listLoading" :data="list" element-loading-text="Loading..." border fit highlight-current-row>
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
import { parseTime } from '@/utils'
// options components
import FilenameOption from './components/FilenameOption'
import AutoWidthOption from './components/AutoWidthOption'
import BookTypeOption from './components/BookTypeOption'

export default {
  name: 'ExportExcel',
  components: { FilenameOption, AutoWidthOption, BookTypeOption },
  data() {
    return {
      list: null,
      listLoading: true,
      downloadLoading: false,
      filename: '',
      autoWidth: true,
      bookType: 'xlsx',
      listQuery: {
        page: 1,
        sort: '+id'
      }
    }
  },
  mounted() {
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
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['id', 'name', 'sex', 'education', 'imp', 'department', 'state', 'entrytime', 'birthday', 'school', 'home', 'marriage', 'remark', 'creatime']
        const filterVal = ['id', 'name', 'sex', 'education', 'imp', 'department', 'state', 'entrytime', 'birthday', 'school', 'home', 'marriage', 'remark', 'creatime']
        const list = this.list
        const data = this.formatJson(filterVal, list)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.filename,
          autoWidth: this.autoWidth,
          bookType: this.bookType
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>

<style>
.radio-label {
  font-size: 14px;
  color: #606266;
  line-height: 40px;
  padding: 0 12px 0 30px;
}
</style>
