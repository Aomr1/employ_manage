<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.name" placeholder="员工姓名" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.imp" placeholder="员工星级" clearable style="width: 130px" class="filter-item">
        <el-option v-for="item in ImportanceOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.department" placeholder="部门" clearable style="width: 130px" class="filter-item">
        <el-option v-for="item in DepartmentOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.education" placeholder="学历" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in EducationOptions" :key="item.key" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.state" placeholder="状态" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in StateOptions" :key="item.key" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves style="margin-left: 7px;" class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 7px;" type="primary" icon="el-icon-refresh" @click="handleClear">
        清空
      </el-button>
      <el-button class="filter-item" style="margin-left: 7px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        增加
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" style="margin-left: 7px;" type="primary" icon="el-icon-download" @click="handleDownload">
        导出
      </el-button>
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;margin-top: 10px;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="100px" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="姓名" width="120px" align="center">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="性别" width="100px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.sex }}</span>
        </template>
      </el-table-column>
      <el-table-column label="学历" width="100px" align="center">
        <template slot-scope="{row}">
          <el-tag>
            {{ row.education }}
          </el-tag>
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
      <el-table-column label="入职时间" width="160px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.entrytime }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" class-name="status-col" width="100px" align="center">
        <template slot-scope="{row}">
          <el-tag :type="row.state | statusFilter">
            {{ row.state }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" min-width="300px" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button size="mini" @click="handleMore(row)">
            详细信息
          </el-button>
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button v-if="row.state!='执勤'" size="mini" type="success" @click="handleModifyStatus(row,'执勤')">
            执勤
          </el-button>
          <el-button v-if="row.state!='休假'" size="mini" type="info" @click="handleModifyStatus(row,'休假')">
            休假
          </el-button>
          <el-button size="mini" type="danger" @click="handleDelete(row,$index)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="员工详细信息" :visible.sync="dialogTableVisible">
      <el-table :data="ExpandList" border fit highlight-current-row :default-expand-all="true">
        <el-table-column type="expand">
          <template slot-scope="{row}">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="出生日期">
                <span>{{ row.birthday }}</span>
              </el-form-item>
              <el-form-item label="毕业学校">
                <span>{{ row.school }}</span>
              </el-form-item>
              <el-form-item label="生源地址">
                <span>{{ row.home }}</span>
              </el-form-item>
              <el-form-item label="婚姻状态">
                <span>{{ row.marriage }}</span>
              </el-form-item>
              <el-form-item label="创建信息时间">
                <span>{{ row.creatime | parseTime('{y}-{m}-{d} {h}:{i}:{s}') }}</span>
              </el-form-item>
              <el-form-item label="备注">
                <span>{{ row.remark }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column property="id" label="员工ID" />
        <el-table-column property="name" label="员工姓名" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogTableVisible = false">取消</el-button>
      </span>
    </el-dialog>
    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog title="修改员工信息" :visible.sync="dialogFormVisible" center>
      <el-form ref="dataForm" :rules="rules" :model="temp" label-width="200px" style="width: 500px; margin-left:50px;">
        <el-form-item label="员工姓名" prop="name">
          <el-input v-model="temp.name" :disabled="true" />
        </el-form-item>

        <el-form-item label="学历" prop="education">
          <el-select
            v-model="temp.education"
            placeholder="请选择员工学历"
            style="width: 100%;"
          >
            <el-option label="博士" value="博士" />
            <el-option label="硕士" value="硕士" />
            <el-option label="本科" value="本科" />
            <el-option label="专科" value="专科" />
          </el-select>
        </el-form-item>

        <el-form-item label="员工星级" prop="imp">
          <el-rate
            v-model="temp.imp"
            :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
            :max="5"
            style="margin-top: 11px"
          />
        </el-form-item>

        <el-form-item label="部门" prop="department">
          <el-select
            v-model="temp.department"
            placeholder="请选择员工部门"
            style="width: 100%;"
          >
            <el-option label="财务部" value="财务部" />
            <el-option label="技术部" value="技术部" />
            <el-option label="后勤部" value="后勤部" />
            <el-option label="营销部" value="营销部" />
            <el-option label="人力资源部" value="人力资源部" />
          </el-select>
        </el-form-item>

        <el-form-item label="入职时间" required prop="entrytime">
          <el-date-picker
            v-model="temp.entrytime"
            type="date"
            value-format="yyyy-MM-dd"
            placeholder="选择入职时间"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="婚姻状态" prop="marriage">
          <el-radio-group v-model="temp.marriage">
            <el-radio label="已婚" />
            <el-radio label="未婚" />
          </el-radio-group>
        </el-form-item>

        <el-form-item label="员工备注" prop="remark">
          <el-input
            v-model="temp.remark"
            type="textarea"
            :rows="7"
            clearable
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="updateData()">
          提交
        </el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils/index'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        执勤: 'success',
        休假: 'info',
        删除: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 10,
        sort: '+id',
        name: undefined,
        imp: undefined,
        department: undefined,
        education: undefined,
        state: undefined
      },
      ImportanceOptions: [1, 2, 3, 4, 5],
      DepartmentOptions: ['财务部', '技术部', '后勤部', '营销部', '人力资源部'],
      EducationOptions: ['博士', '硕士', '本科', '专科'],
      StateOptions: ['执勤', '休假'],
      sortOptions: [{ label: 'ID 升序', key: '+id' }, { label: 'ID 降序', key: '-id' }],
      temp: {
        id: undefined,
        name: '',
        education: '',
        imp: undefined,
        department: '',
        entrytime: '',
        marriage: '',
        remark: ''
      },
      dialogFormVisible: false,
      dialogTableVisible: false,
      rules: {
        marriage: [
          { required: true, message: '请选择婚姻状态', trigger: 'change' }
        ],
        education: [
          { required: true, message: '请选择员工学历', trigger: 'change' }
        ],
        imp: [{ required: true, message: '请选择员工星级', trigger: 'blur' }],
        department: [
          { required: true, message: '请选择员工部门', trigger: 'change' }
        ],
        state: [
          { required: true, message: '请选择员工状态', trigger: 'change' }
        ],
        entrytime: [
          {
            required: true,
            message: '请选择入职时间',
            trigger: 'change'
          }
        ]
      },
      downloadLoading: false,
      ExpandList: null
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      this.$axios
        .post('http://127.0.0.1:5000/Employ/SelectEmployee', {
          listQuery: this.listQuery
        })
        .then((response) => {
          if (response.data.code === 20000) {
            // console.log(response.data)
            this.list = response.data.items
            this.total = response.data.total
            console.log(response.data)
            setTimeout(() => {
              this.listLoading = false
            }, 1)
          }
        })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, state) {
      this.$message({
        message: '修改成功',
        type: 'success',
        center: true
      })
      this.$axios
        .post('http://127.0.0.1:5000/Employ/UpdateEmployeeState', {
          change_state_id: row.id,
          change_state: state
        })
      row.state = state
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        name: '',
        education: '',
        imp: undefined,
        department: '',
        entrytime: '',
        marriage: '',
        remark: ''
      }
    },
    handleCreate() {
      this.$router.push({
        name: 'Form'
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.entrytime = new Date(this.temp.entrytime)
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          this.$axios
            .post('http://127.0.0.1:5000/Employ/UpdateEmployee', {
              tempData: tempData
            })
            .then((response) => {
              if (response.data.code === 20000) {
                const index = this.list.findIndex(v => v.id === this.temp.id)
                this.temp.entrytime = parseTime(this.temp.entrytime).split(' ')[0]
                this.list.splice(index, 1, this.temp)
                this.dialogFormVisible = false
                this.$message({
                  message: '修改成功',
                  type: 'success',
                  center: true
                })
              }
            })
        }
      })
    },
    handleDelete(row, index) {
      this.$confirm('此操作将永久删除该员工信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.list.splice(index, 1)
          this.$axios.post('http://127.0.0.1:5000/Employ/DeleteEmployee', {
            delete_id: row.id
          })
          this.$message({
            type: 'success',
            center: true,
            message: '删除成功!'
          })
          setTimeout(() => {
            this.getList()
          }, 100)
        })
        .catch(() => {
          this.$message({
            type: 'info',
            center: true,
            message: '已取消删除'
          })
        })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['id', 'name', 'sex', 'education', 'imp', 'department', 'entrytime', 'state']
        const filterVal = ['id', 'name', 'sex', 'education', 'imp', 'department', 'entrytime', 'state']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'employees'
        })
        this.downloadLoading = false
      })
    },
    handleClear() {
      this.listQuery = {
        page: 1,
        limit: 20,
        sort: '+id',
        name: undefined,
        imp: undefined,
        department: undefined,
        education: undefined,
        state: undefined
      }
      this.getList()
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
    handleMore(row) {
      this.$axios
        .post('http://127.0.0.1:5000/Employ/SeleteEmployeeMore', {
          more_id: row.id
        })
        .then((response) => {
          this.ExpandList = response.data.more_employee
          this.dialogTableVisible = true
        })
    }
  }
}
</script>
<style scoped>
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>
