<template>
  <q-page class="flex flex-center" style="background: #112347">
    <q-card class="q-mb-xl" style="width:950px; height: 400px">
      <q-img src="../assets/img/bg.png"/>
      <div class="absolute-top-right column q-mr-xs" style="width: 400px; height: 500px">
        <div class="col-1"></div>
        <div class="text-h4 col-3">用户登录</div>
        <q-form class="col-6 column"
        @submit="Login">
          <q-input
            class="col-4"
            filled
            v-model="username"
            label="用户名"/>

          <q-input
            class="col-4"
            filled
            v-model="password"
            label="密码"/>
          <div class="col-1"></div>
          <q-btn class="full-width col-2" label="登录" type="submit" color="blue"></q-btn>
        </q-form>
        <q-btn class="absolute-bottom-right q-mb-md" flat label="没有账号" to="/register"></q-btn>
      </div>
    </q-card>
  </q-page>
</template>

<script>
import {api} from "boot/axios";
import {Notify} from "quasar";

export default {
  name: "Login",

  data(){
    return{
      username: "",
      password: ""
    }
  },
  methods:{
    Login(){
      let _this = this
      api.post("http://127.0.0.1:8000/api/log/login/", {
        username: this.username,
        password: this.password
      }).then(function(response){
        console.log(response)
        let res = response.data
        if(res.status === "Success"){
          sessionStorage.setItem('user_id', res.id)
          sessionStorage.setItem('user_permission', res.permission)
          if(res.permission === 0) _this.$router.push("/home")
          else _this.$router.push("/admin_home")
        }else{
          Notify.create(
            {
              type: 'negative',
              message: '用户名或密码错误'
            }
          )
        }
      }).catch(function (error){
        console.log(error)
        Notify.create(
          {
            type: 'negative',
            message: '内部错误'
          })
      })
    }
  }
}
</script>

<style scoped>

</style>
