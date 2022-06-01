<template>
  <el-card shadow="hover">
    <div slot="header" class="clearfix">
      <mallki class-name="mallki-text" text="待办事项" />
    </div>
    <section class="todoapp">
      <!-- header -->
      <header class="header">
        <input class="new-todo" autocomplete="off" placeholder="请输入待办事项" @keyup.enter="addTodo">
      </header>
      <!-- main section -->
      <section v-show="todos.length" class="main">
        <input id="toggle-all" :checked="allChecked" class="toggle-all" type="checkbox" @change="toggleAll({ done: !allChecked })">
        <label for="toggle-all" />
        <ul class="todo-list">
          <todo
            v-for="(todo, index) in filteredTodos"
            :key="index"
            :todo="todo"
            @toggleTodo="toggleTodo"
            @editTodo="editTodo"
            @deleteTodo="deleteTodo"
          />
        </ul>
      </section>
      <!-- footer -->
      <footer v-show="todos.length" class="footer">
        <span class="todo-count">
          剩余
          <strong>{{ remaining }}</strong>
          {{ remaining | pluralize('项') }}
        </span>
        <ul class="filters">
          <li v-for="(val, key) in filters" :key="key">
            <a :class="{ selected: visibility === key }" @click.prevent="visibility = key">{{ key | capitalize }}</a>
          </li>
        </ul>
        <!-- <button class="clear-completed" v-show="todos.length > remaining" @click="clearCompleted">
          Clear completed
        </button> -->
      </footer>
    </section>
  </el-card>
</template>

<script>
import Todo from './Todo.vue'
import Mallki from '@/components/TextHoverEffect/Mallki'

const STORAGE_KEY = 'todos'
const filters = {
  全部: todos => todos,
  未完成: todos => todos.filter(todo => !todo.done),
  已完成: todos => todos.filter(todo => todo.done)
}
const defalutList = [
  { text: '吃饭', done: false },
  { text: '睡觉', done: false },
  { text: '打游戏', done: false },
  { text: '刷b站', done: false },
  { text: '打球', done: false },
  { text: '考试', done: false },
  { text: '上课', done: true },
  { text: '喝水', done: true },
  { text: '呼吸', done: true },
  { text: '起床', done: true },
  { text: '走路', done: true }
]
export default {
  components: { Todo, Mallki },
  filters: {
    pluralize: (n, w) => n === 1 ? w : w,
    capitalize: s => s.charAt(0) + s.slice(1)
  },
  data() {
    return {
      visibility: '全部',
      filters,
      // todos: JSON.parse(window.localStorage.getItem(STORAGE_KEY)) || defalutList
      todos: defalutList
    }
  },
  computed: {
    allChecked() {
      return this.todos.every(todo => todo.done)
    },
    filteredTodos() {
      return filters[this.visibility](this.todos)
    },
    remaining() {
      return this.todos.filter(todo => !todo.done).length
    }
  },
  methods: {
    setLocalStorage() {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(this.todos))
    },
    addTodo(e) {
      const text = e.target.value
      if (text.trim()) {
        this.todos.push({
          text,
          done: false
        })
        this.setLocalStorage()
      }
      e.target.value = ''
    },
    toggleTodo(val) {
      val.done = !val.done
      this.setLocalStorage()
    },
    deleteTodo(todo) {
      this.todos.splice(this.todos.indexOf(todo), 1)
      this.setLocalStorage()
    },
    editTodo({ todo, value }) {
      todo.text = value
      this.setLocalStorage()
    },
    clearCompleted() {
      this.todos = this.todos.filter(todo => !todo.done)
      this.setLocalStorage()
    },
    toggleAll({ done }) {
      this.todos.forEach(todo => {
        todo.done = done
        this.setLocalStorage()
      })
    }
  }
}
</script>

<style lang="scss">
  @import './index.scss';
</style>
