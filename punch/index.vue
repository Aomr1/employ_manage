<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="PunchQuery.name" placeholder="员工姓名" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="PunchQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-select v-model="PunchQuery.identity" placeholder="身份" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in rolesOptions" :key="item.key" :label="item" :value="item" />
      </el-select>
      <el-date-picker
        v-model="PunchQuery.day"
        type="date"
        value-format="yyyy-MM-dd"
        placeholder="选择日期"
        :picker-options="pickerOptions"
      />
      <el-time-select
        v-model="PunchQuery.intervals"
        :picker-options="{
          start: '01:00',
          step: '01:00',
          end: '12:00'
        }"
        placeholder="选择工作时长"
      />
      <el-select v-if="roles[0] != '老板'" v-model="PunchQuery.state" placeholder="状态" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in StateOptions" :key="item.key" :label="item" :value="item" />
      </el-select>
      <el-button v-waves style="margin-left: 7px;" class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 7px;" type="primary" icon="el-icon-refresh" @click="handleClear">
        清空
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
      <el-table-column align="center" prop="id" sortable="custom" label="ID" :class-name="getSortClass('id')" width="60px">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" label="姓名" width="60px">
        <template slot-scope="{row}">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" label="部门" width="95px">
        <template slot-scope="{row}">
          <span>{{ row.department }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" label="身份" width="65px">
        <template slot-scope="{row}">
          <span>{{ row.identity }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" label="打卡日期" width="95px">
        <template slot-scope="{row}">
          <span>{{ row.day }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" label="上班打卡时间" width="355px">
        <template slot-scope="{row}">
          <template v-if="roles[0]==='老板'">
            <el-tag v-show="row.go_time!=null" class="link-type" :disable-transitions="true" effect="plain" style="margin-right:10px">{{ row.go_time }}</el-tag>
          </template>
          <template v-else>
            <template v-if="row.go_edit">
              <el-time-picker
                v-model="gotime"
                :picker-options="{selectableRange: '00:00:00 - 23:59:59'}"
                size="small"
              />
              <el-button-group slot="prepend">
                <el-button
                  type="success"
                  size="small"
                  icon="el-icon-edit-outline"
                  @click="confirmGoEdit(row)"
                >
                  提交
                </el-button>
                <el-button
                  size="small"
                  icon="el-icon-refresh"
                  type="warning"
                  @click="cancelGoEdit(row)"
                >
                  取消
                </el-button>
              </el-button-group>
            </template>
            <template v-else>
              <template>
                <el-tag v-show="row.go_time!=null" class="link-type" :disable-transitions="true" effect="plain" style="margin-right:10px" @click="row.go_edit=!row.go_edit">{{ row.go_time }}</el-tag>
                <el-button v-show="row.go_time!=null" plain size="small" type="danger" icon="el-icon-delete" @click="DeleteGoTime(row)" />
              </template>
              <el-tag v-show="row.go_time==null" type="warning" :disable-transitions="true" effect="plain" @click="row.go_edit=!row.go_edit"><el-link :underline="false" icon="el-icon-edit">添加打卡时间</el-link></el-tag>
            </template>
          </template>
        </template>
      </el-table-column>

      <el-table-column align="center" label="下班打卡时间" width="355px">
        <template slot-scope="{row}">
          <template v-if="roles[0]==='老板'">
            <el-tag v-show="row.leave_time!=null" class="link-type" :disable-transitions="true" effect="plain" style="margin-right:10px">{{ row.leave_time }}</el-tag>
          </template>
          <template v-else>
            <template v-if="row.leave_edit ">
              <el-time-picker
                v-model="leavetime"
                :picker-options="{selectableRange: '00:00:00 - 23:59:59'}"
                size="small"
              />
              <el-button-group slot="prepend">
                <el-button
                  type="success"
                  size="small"
                  icon="el-icon-edit-outline"
                  @click="confirmLeaveEdit(row)"
                >
                  提交
                </el-button>
                <el-button
                  size="small"
                  icon="el-icon-refresh"
                  type="warning"
                  @click="cancelLeaveEdit(row)"
                >
                  取消
                </el-button>
              </el-button-group>
            </template>
            <template v-else>
              <template>
                <el-tag v-show="row.leave_time!=null" class="link-type" :disable-transitions="true" effect="plain" style="margin-right:10px" @click="row.leave_edit=!row.leave_edit">{{ row.leave_time }}</el-tag>
                <el-button v-show="row.leave_time!=null" plain size="small" type="danger" icon="el-icon-delete" @click="DeleteLeaveTime(row)" />
              </template>
              <el-tag v-show="row.leave_time==null" type="warning" :disable-transitions="true" effect="plain" @click="row.leave_edit=!row.leave_edit"><el-link :underline="false" icon="el-icon-edit">添加打卡时间</el-link></el-tag>
            </template>
          </template>
        </template>
      </el-table-column>

      <el-table-column align="center" label="工作时长" width="95px">
        <template slot-scope="{row}">
          <span>{{ row.intervals }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center" label="状态" width="75px">
        <template slot-scope="{row}">
          <template v-if="roles[0] === '小组长'">
            <el-tag v-if="row.grp_agree==='false'" size="medium" type="info">
              驳回
            </el-tag>
            <el-tag v-if="row.grp_agree==='agency'" size="medium" type="warning">
              代办
            </el-tag>
          </template>
          <template v-if="roles[0] === '主管'">
            <el-tag v-if="row.htp_agree==='false'" size="medium" type="info">
              驳回
            </el-tag>
            <el-tag v-if="row.htp_agree==='agency'" size="medium" type="warning">
              代办
            </el-tag>
          </template>
          <template v-if="roles[0] === '老板'">
            <el-tag v-if="row.htp_agree ==='true'" size="medium" type="success">
              批准
            </el-tag>
          </template>
        </template>
      </el-table-column>

      <el-table-column align="center" label="操作" min-width="220px">
        <template slot-scope="{row}">
          <template v-if="row.identity==='员工'">
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >删除</el-button>
            <template v-if="roles[0] === '小组长'">
              <el-button v-if="row.grp_agree!='true'" size="small" type="success" @click="handleModifyGrpAgree(row,index,'true')">
                批准
              </el-button>
              <el-button v-if="row.grp_agree!='true'" size="small" type="info" @click="handleModifyGrpAgree(row,index,'false')">
                驳回
              </el-button>
            </template>
            <template v-if="roles[0] === '主管'">
              <el-button v-if="row.htp_agree!='true'" size="small" type="success" @click="handleModifyHtpAgree(row,index,'true')">
                批准
              </el-button>
              <el-button v-if="row.grp_agree==='true'" size="small" type="info" @click="handleModifyGrpAgree(row,index,'false')">
                驳回
              </el-button>
            </template>
            <template v-if="roles[0] === '老板'">
              <el-button v-if="row.htp_agree!='false'" size="small" type="info" @click="handleModifyHtpAgree(row,index,'false')">
                驳回
              </el-button>
            </template>
          </template>
          <template v-if="row.identity==='小组长'">
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >删除</el-button>
            <template v-if="roles[0] === '主管'">
              <el-button v-if="row.htp_agree!='true'" size="small" type="success" @click="handleModifyHtpAgree(row,index,'true')">
                批准
              </el-button>
              <el-button v-if="row.htp_agree!='true'" size="small" type="info" @click="handleModifyHtpAgree(row,index,'false')">
                驳回
              </el-button>
            </template>
            <template v-if="roles[0] === '老板'">
              <el-button v-if="row.htp_agree!='false'" size="small" type="info" @click="handleModifyHtpAgree(row,index,'false')">
                驳回
              </el-button>
            </template>
          </template>
          <template v-if="row.identity==='主管'">
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >删除</el-button>
            <template v-if="roles[0] === '老板'">
              <el-button v-if="row.htp_agree!='false'" size="small" type="info" @click="handleModifyHtpAgree(row,index,'false')">
                驳回
              </el-button>
            </template>
          </template>
        </template>
      </el-table-column>
    </el-table>
    <pagination v-show="total>0" :total="total" :page.sync="PunchQuery.page" :limit.sync="PunchQuery.limit" @pagination="getList" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils/index'

export default {
  name: 'Punch',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      leavetime: new Date(),
      gotime: new Date(),
      tableKey: 0,
      total: 0,
      list: null,
      listLoading: true,
      PunchQuery: {
        page: 1,
        limit: 10,
        sort: '+id',
        intervals: undefined,
        state: undefined,
        name: undefined,
        identity: undefined,
        day: undefined
      },
      StateOptions: ['代办', '驳回'],
      sortOptions: [{ label: 'ID 升序', key: '+id' }, { label: 'ID 降序', key: '-id' }],
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now()
        },
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', new Date())
          }
        },
        {
          text: '昨天',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', date)
          }
        },
        {
          text: '一周前',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', date)
          }
        }]
      }
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles',
      'token',
      'department'
    ]),
    rolesOptions() {
      if (this.roles[0] === '小组长') {
        return false
      } else if (this.roles[0] === '主管') {
        return ['员工', '小组长']
      } else {
        return ['员工', '小组长', '主管']
      }
    }
  },
  mounted() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      this.$axios
        .post('http://127.0.0.1:5000/Punch/SelectPunch', {
          token: this.token,
          department: this.department,
          PunchQuery: this.PunchQuery
        })
        .then((response) => {
          if (response.data.code === 20000) {
            const items = response.data.items
            this.list = items.map(v => {
              this.$set(v, 'go_edit', false) // https://vuejs.org/v2/guide/reactivity.html
              v.go_time_originalTitle = v.go_time //  will be used when user click the cancel botton
              return v
            })
            this.list = items.map(v => {
              this.$set(v, 'leave_edit', false) // https://vuejs.org/v2/guide/reactivity.html
              v.leave_time_originalTitle = v.leave_time //  will be used when user click the cancel botton
              return v
            })
            console.log(this.list)
            this.total = response.data.total
            setTimeout(() => {
              this.listLoading = false
            }, 1)
          }
        })
      this.listLoading = false
    },
    handleFilter() {
      this.PunchQuery.page = 1
      this.getList()
    },
    handleClear() {
      this.PunchQuery = {
        page: 1,
        limit: 10,
        sort: '+id',
        intervals: undefined,
        state: undefined,
        name: undefined,
        identity: undefined,
        day: undefined
      }
      this.getList()
    },
    cancelGoEdit(row) {
      row.go_time = row.go_time_originalTitle
      row.go_edit = false
      this.$message({
        message: '取消修改',
        center: true,
        type: 'warning'
      })
    },
    confirmGoEdit(row) {
      row.go_edit = false
      row.go_time = parseTime(this.gotime).split(' ')[1]
      row.go_time_originalTitle = row.go_time
      this.$axios
        .post('http://127.0.0.1:5000/Punch/UpDateGoTime', {
          // login_role: this.roles[0],
          // identity: row.identity,
          id: row.id,
          new_go_time: row.go_time,
          leave_time: row.leave_time,
          day: row.day
        })
        .then((response) => {
          row.intervals = response.data.intervals
        })
      this.$message({
        message: '成功修改上班打卡时间',
        center: true,
        type: 'success'
      })
    },
    cancelLeaveEdit(row) {
      row.leave_time = row.leave_time_originalTitle
      row.leave_edit = false
      this.$message({
        message: '取消修改',
        center: true,
        type: 'warning'
      })
    },
    confirmLeaveEdit(row) {
      row.leave_edit = false
      row.leave_time = parseTime(this.leavetime).split(' ')[1]
      row.leave_time_originalTitle = row.leave_time
      this.$axios
        .post('http://127.0.0.1:5000/Punch/UpDateLeaveTime', {
          // login_role: this.roles[0],
          // identity: row.role,
          id: row.id,
          new_leave_time: row.leave_time,
          go_time: row.go_time,
          day: row.day
        })
        .then((response) => {
          row.intervals = response.data.intervals
        })
      this.$message({
        message: '成功修改下班打卡时间',
        center: true,
        type: 'success'
      })
    },
    getSortClass: function(key) {
      const sort = this.PunchQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.PunchQuery.sort = '+id'
      } else {
        this.PunchQuery.sort = '-id'
      }
      this.handleFilter()
    },
    handleDelete(row, index) {
      this.$confirm('此操作将永久删除该员工该天的所有打卡记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.list.splice(index, 1)
          this.$axios.post('http://127.0.0.1:5000/Punch/DeletePunch', {
            delete_id: row.id,
            delete_day: row.day
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
    DeleteGoTime(row, index) {
      this.$confirm('此操作将永久删除该员工该天的上班打卡记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          row.go_time = null
          this.$axios.post('http://127.0.0.1:5000/Punch/DeleteGoTime', {
            delete_id: row.id,
            delete_day: row.day
          })
          this.$message({
            type: 'success',
            center: true,
            message: '删除成功!'
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            center: true,
            message: '已取消删除'
          })
        })
    },
    DeleteLeaveTime(row, index) {
      this.$confirm('此操作将永久删除该员工该天的下班打卡记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          row.leave_time = null
          this.$axios.post('http://127.0.0.1:5000/Punch/DeleteLeaveTime', {
            delete_id: row.id,
            delete_day: row.day
          })
          this.$message({
            type: 'success',
            center: true,
            message: '删除成功!'
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            center: true,
            message: '已取消删除'
          })
        })
    },
    handleModifyGrpAgree(row, index, grp_agree) {
      var grpmessage = ''
      if (grp_agree === 'true') {
        grpmessage = '批准'
      } else {
        grpmessage = '驳回'
      }
      this.$message({
        message: `${grpmessage}成功`,
        type: 'success',
        center: true
      })
      this.$axios
        .post('http://127.0.0.1:5000/Punch/UpdateGrpAgree', {
          id: row.id,
          grp_agree: grp_agree,
          day: row.day
        })
      setTimeout(() => {
        this.getList()
      }, 100)
    },
    handleModifyHtpAgree(row, index, htp_agree) {
      var htpmessage = ''
      if (htp_agree === 'true') {
        htpmessage = '批准'
      } else {
        htpmessage = '驳回'
      }
      this.$message({
        message: `${htpmessage}成功`,
        type: 'success',
        center: true
      })
      this.$axios
        .post('http://127.0.0.1:5000/Punch/UpdateHtpAgree', {
          id: row.id,
          htp_agree: htp_agree,
          day: row.day
        })
      setTimeout(() => {
        this.getList()
      }, 100)
    }
  }
}
</script>

<style scoped>
.el-date-editor.el-input, .el-date-editor.el-input__inner {
    margin-top: 1px;
    width: 180px;
}
.el-tag{
  font-size: 14px;
}
</style>
