<template>
  <q-page class="flex flex-center" style="background: #112347">
    <q-card class="q-mb-xl" style="width:950px; height: 400px">
      <q-img src="../assets/img/bg.png"/>
      <div class="absolute-top-right column q-mr-xs" style="width: 400px; height: 500px">
        <div class="col-1"></div>
        <div class="text-h4 col-2">用户注册</div>
        <q-form class="col-6 column justify-center"
                @submit="Register">
          <q-input
            class="col-3"
            filled
            v-model="username"
            label="用户名"/>
          <q-input
            class="col-3"
            filled
            v-model="password"
            label="密码"/>
          <q-input
            class="col-3"
            filled
            v-model="confirm"
            label="确认密码"/>
          <div class="col-1"></div>
          <q-btn class="full-width col-2" label="登录" type="submit" color="blue"></q-btn>
        </q-form>
        <q-btn class="absolute-bottom-right q-mb-md" flat label="返回" to="/"></q-btn>
      </div>
    </q-card>
  </q-page>
</template>

<script>
export default {
  name: "Register",
  data(){
    return{
      username: "",
      password: "",
      confirm: ""
    }
  },
  methods:{
    Register(){

    }
  }
}
</script>

<style scoped>

</style>
