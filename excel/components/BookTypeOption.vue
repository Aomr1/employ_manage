<template>
  <div style="display:inline-block;">
    <label class="radio-label">导出类型: </label>
    <el-select v-model="bookType" style="width:120px;">
      <el-option
        v-for="item in options"
        :key="item"
        :label="item"
        :value="item"
      />
    </el-select>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: String,
      default: 'xlsx'
    }
  },
  data() {
    return {
      options: ['xlsx', 'csv', 'txt']
    }
  },
  computed: {
    bookType: {
      get() {
        return this.value
      },
      set(val) {
        this.$emit('input', val)
      }
    }
  }
}
</script>
