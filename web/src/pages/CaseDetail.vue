<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width row q-ma-md" style="height: 650px; background: #112347">
      <div class="col-6 column text-white">
        <div class="col-3 text-h3 q-pa-md ">异常详情</div>
        <div class="col q-pa-md text-h5 q-ml-xl">异常编号：{{id}}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">异常类型：{{case_type}}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">异常等级：{{level}}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">是否被查阅：{{checked?'已查阅':'未查阅'}}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">出现时间：{{data_time}}</div>
        <div class="col-2 row">
          <q-btn class=" q-ma-md q-ml-xl bg-green text-black text-h6" style="height: 60px; width: 150px; font-weight: bold" label="确认查阅"></q-btn>
          <q-btn class=" q-ma-md q-ml-xl bg-red text-black text-h6" style="height: 60px; width: 150px; font-weight: bold" label="删除"></q-btn>
        </div>

      </div>
      <div class="col-6 column q-pa-xl">
                <img class="q-pr-xl" style="width: 560px; height: 400px" src="">
      </div>
    </div>
  </q-page>
</template>

<script>
import {Notify} from "quasar";
import {api} from "boot/axios";

export default {
  name: "CaseDetail",
  props:['id'],
  created(){

  },
  data(){
    return{
      case_type: "未知车辆闯入",
      level: 5,
      checked: true,
      data_time: "1999/1/1",
    }
  },
  methods:{
    get_case_detail(){

    }
    // look(){
    //   let _this = this
    //   api.post("http://192.168.43.28:8000/api/test/",{}).then(function(response){
    //     console.log(response)
    //     let res = response.data
    //     if(res.status === "Success"){
    //       _this.img = res.img
    //     }else{
    //       Notify.create(
    //         {
    //           type: 'negative',
    //           message: '未知错误'
    //         }
    //       )
    //     }
    //   }).catch(function (error){
    //     console.log(error)
    //     Notify.create(
    //       {
    //         type: 'negative',
    //         message: '内部错误'
    //       })
    //   })
    // }
  }
}
</script>

<style scoped>

</style>

