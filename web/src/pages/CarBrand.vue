<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-2 text-h4 q-ma-md">添加可通行车牌</div>
      <q-form class="col-6 column q-ml-md" style="width: 30%"
              @submit="add_brand">
        <q-input
          class="col-3"
          filled
          v-model="brand"
          label="车牌"/>
        <div class="col-1"></div>
        <q-btn class="full-width col-2" label="确定添加" type="submit" color="blue"></q-btn>
      </q-form>
    </div>
  </q-page>
</template>

<script>
import {Notify} from "quasar";
import {api} from "boot/axios";

export default {
  name: "CarBrand",
  data(){
    return{
      brand: "",
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
    add_brand(){
      let _this = this
      api.post("http://172.30.68.249:8000/api/add_car/", {
        car_brand: this.brand
      }).then(function(response){
        console.log(response)
        let res = response.data
        if(res.status === "Success"){
          Notify.create(
            {
              type: 'positive',
              message: '添加'
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
