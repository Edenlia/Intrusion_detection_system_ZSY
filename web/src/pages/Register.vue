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
import {api} from "boot/axios";
import {Notify} from "quasar";

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
      if(this.password !== this.confirm){
        Notify.create(
          {
            type: 'negative',
            message: '密码与确认密码不同'
          }
        )
        return
      }
      let _this = this
      api.post("http://192.168.43.28:8000/api/log/register/", {
        username: this.username,
        password: this.password
      }).then(function(response){
        console.log(response)
        let res = response.data
        if(res.status === "Success"){
          Notify.create(
            {
              type: 'positive',
              message: '注册成功'
            }
          )
          _this.$router.push("/")
        }else{
          if(res.message === "User exist"){
            Notify.create(
              {
                type: 'negative',
                message: '用户名已存在'
              }
            )
          }else{
            Notify.create(
              {
                type: 'negative',
                message: '未知错误'
              }
            )
          }
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
