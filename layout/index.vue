<template>
  <div :class="classObj" class="app-wrapper">
    <div class="top-menu-container" style="height: 50px;">
      <div class="top-logo">
        <logo v-if="showLogo" :collapse="isCollapse" />
      </div>
      <div class="top-toolbar">
        <hamburger :is-active="sidebar.opened" class="hamburger-container toolbar" @toggleClick="toggleSideBar" />
      </div>
      <div class="top-menu">
        <top-menu />
      </div>
      <div class="right-menu">
        <template v-if="device!=='mobile'">
          <go class="right-menu-item hover-effect" />
          <back class="right-menu-item hover-effect" />
          <home class="right-menu-item hover-effect" />
          <screenfull id="screenfull" class="right-menu-item hover-effect" />
        </template>

        <el-dropdown class="avatar-container right-menu-item" trigger="click">
          <div class="avatar-wrapper">
            <!-- <img :src="avatar+'?imageView2/1/w/80/h/80'" class="user-avatar"> -->
            <img :src="avatar" class="user-avatar">
            <i class="el-icon-caret-bottom" />
          </div>
          <el-dropdown-menu slot="dropdown">
            <router-link to="/profile">
              <el-dropdown-item>个人中心</el-dropdown-item>
            </router-link>
            <router-link to="/">
              <el-dropdown-item>返回主页</el-dropdown-item>
            </router-link>
            <el-dropdown-item divided @click.native="logout">
              <span style="display:block;">退出登录</span>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>

    </div>
    <div v-if="device==='mobile'&&sidebar.opened && second_routes.length>0" class="drawer-bg" @click="handleClickOutside" />
    <sidebar />
    <div class="main-container" :class="classSidebar">
      <div :class="{'fixed-header':fixedHeader}">
        <navbar />
      </div>
      <app-main />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { Navbar, Sidebar, AppMain } from './components'
import Logo from './components/Sidebar/Logo'
import TopMenu from './components/Sidebar/TopMenu'
import Hamburger from '@/components/Hamburger'
import ResizeMixin from './mixin/ResizeHandler'
import Screenfull from '@/components/Screenfull'
import Home from '@/components/HomeSvg'
import Go from '@/components/GoSvg'
import Back from '@/components/BackSvg'

export default {
  name: 'Layout',
  components: {
    Navbar,
    Sidebar,
    AppMain,
    Logo,
    TopMenu,
    Hamburger,
    Screenfull,
    Home,
    Go,
    Back
  },
  mixins: [ResizeMixin],
  computed: {
    ...mapGetters([
      'second_routes',
      'third_routes',
      'sidebar',
      'avatar'
    ]),
    sidebar() {
      return this.$store.state.app.sidebar
    },
    device() {
      return this.$store.state.app.device
    },
    fixedHeader() {
      return this.$store.state.settings.fixedHeader
    },
    classObj() {
      return {
        hideSidebar: !this.sidebar.opened,
        openSidebar: this.sidebar.opened,
        withoutAnimation: this.sidebar.withoutAnimation,
        mobile: this.device === 'mobile'
      }
    },
    showLogo() {
      return this.$store.state.settings.sidebarLogo
    },
    isCollapse() {
      return !this.sidebar.opened
    },
    classSidebar() {
      return {
        sidebarLeft: this.second_routes.length > 0,
        subSidebarLeft: this.second_routes.length > 0 && this.third_routes.length > 0
      }
    }
  },
  methods: {
    handleClickOutside() {
      this.$store.dispatch('app/closeSideBar', { withoutAnimation: false })
    },
    toggleSideBar() {
      if (this.device === 'mobile' && this.second_routes.length < 1) {
        return
      }
      this.$store.dispatch('app/toggleSideBar')
    },
    async logout() {
      await this.$store.dispatch('user/logout')
      this.$router.push(`/login?redirect=${this.$route.fullPath}`)
    }
  }
}
</script>

<style lang="scss" scoped>
  @import "~@/styles/mixin.scss";
  @import "~@/styles/variables.scss";

  .app-wrapper {
    @include clearfix;
    position: relative;
    height: 100%;
    width: 100%;
    &.mobile.openSidebar{
      position: fixed;
      top: 0;
    }
  }
  .drawer-bg {
    background: #000;
    opacity: 0.3;
    width: 100%;
    top: 0;
    height: 100%;
    position: absolute;
    z-index: 999;
  }

    .fixed-header {
      position: fixed;
      top: 50px;
      right: 0;
      z-index: 9;
      width: 100%;
      // transition: width 0.28s;
    }

  .sidebarLeft {
    .fixed-header {
      width: calc(100% - #{$sideBarWidth});
    }
  }
  .subSidebarLeft {
    .fixed-header {
      width: calc(100% - #{$sideBarWidth} - #{$subBarWidth});
    }
  }

  .hideSidebar {
    .fixed-header {
      width: 100%;
    }
    .sidebarLeft .fixed-header {
      width: calc(100% - 54px);
    }
  }

  .mobile {
    .fixed-header {
      width: 100%;
    }

    .sidebarLeft .fixed-header {
      width: 100%;
    }
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #BFCBD9;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background .3s;

        &:hover {
          background: #263445
        }
      }
    }

    .avatar-container {
      margin-left: 15px;
      margin-right: 30px;
      height: 50px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;

        .user-avatar {
          cursor: pointer;
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }

        .el-icon-caret-bottom {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
</style>
