<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-white" v-if="this.$route.path !== '/' && this.$route.path !== '/register'">
      <q-toolbar>
        <q-btn
          class="bg-grey"
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
          v-if="this.$route.path !== '/' && this.$route.path !== '/register'"
        />
        <q-toolbar-title class="text-black">欢迎回来</q-toolbar-title>
      </q-toolbar>

    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      style="background: #001529"
      v-if="this.$route.path !== '/' && this.$route.path !== '/register'">
    >
      <q-item class="text-white text-h5" style="font-weight: bold">
        监控摄像管理平台
      </q-item>
      <br/>
      <q-list>
        <q-expansion-item
          style="background: #001529"
          class="text-white"
          dense
          dense-toggle
          expand-separator
          icon="subject"
          label="功能"
        >
          <q-item class="text-grey-1" style="background: #000c17" to="/home">
            <q-item-section side>
              <q-icon name="home"></q-icon>
            </q-item-section>
            <q-item-section>主页</q-item-section>
          </q-item>
          <q-item class="text-grey-1" style="background: #000c17" to="/camera">
            <q-item-section side>
              <q-icon name="videocam"></q-icon>
            </q-item-section>
            <q-item-section>摄像头</q-item-section>
          </q-item >
          <q-item class="text-grey-1" style="background: #000c17" to="/case">
            <q-item-section side>
              <q-icon name="highlight_off"></q-icon>
            </q-item-section>
            <q-item-section>检测到异常</q-item-section>
          </q-item>
          <q-item class="text-grey-1" style="background: #000c17" to="/analytics">
            <q-item-section side>
              <q-icon name="analytics"></q-icon>
            </q-item-section>
            <q-item-section>统计信息</q-item-section>
          </q-item>
        </q-expansion-item>
        <q-expansion-item
          style="background: #001529"
          class="text-white"
          dense
          dense-toggle
          expand-separator
          icon="settings"
          label="设置"
        >
          <q-item class="text-grey-1" style="background: #000c17" to="/profile">
            <q-item-section side>
              <q-icon name="account_circle"></q-icon>
            </q-item-section>
            <q-item-section>修改个人信息</q-item-section>
          </q-item>
          <q-item class="text-grey-1" style="background: #000c17" to="/">
            <q-item-section side>
              <q-icon name="logout"></q-icon>
            </q-item-section>
            <q-item-section>退出登录</q-item-section>
          </q-item>
        </q-expansion-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>

export default {
  name: 'MainLayout',
  data(){
    return{
      leftDrawerOpen: false
    }
  },
  methods:{
    toggleLeftDrawer () {
      this.leftDrawerOpen = !this.leftDrawerOpen
    }
  }

}
</script>
