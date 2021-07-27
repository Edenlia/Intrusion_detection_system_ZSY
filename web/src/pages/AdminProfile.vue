<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-2 text-h4 q-ma-md">修改密码</div>
      <q-form class="col-6 column q-ml-md" style="width: 30%"
              @submit="change_password">
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
        <q-btn class="full-width col-2" label="确认修改" type="submit" color="blue"></q-btn>
      </q-form>
    </div>
  </q-page>
</template>

<script>
import {Notify} from "quasar";
import {api} from "boot/axios";

export default {
  name: "Profile",
  data(){
    return{
      username: "",
      password: "",
      confirm: "",
      user_id: ""
    }
  },
  created(){
    if(sessionStorage.getItem('user_id') === null){
      this.$router.push('/')
      return
    }
    this.user_id = sessionStorage.getItem('user_id')
  },
  methods:{
    change_password(){
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
      api.post("http://127.0.0.1:8000.28:8000/api/log/change_password/", {
        id: this.user_id,
        username: this.username,
        password: this.password
      }).then(function(response){
        console.log(response)
        let res = response.data
        if(res.status === "Success"){
          Notify.create(
            {
              type: 'positive',
              message: '修改成功'
            }
          )
        }else{
          if(res.message === "Wrong Username"){
            Notify.create(
              {
                type: 'negative',
                message: '用户名错误'
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
