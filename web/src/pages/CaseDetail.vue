<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width row bg-white q-ma-md" style="height: 650px">
      <div class="col-6 column">
        <div class="col-3 text-h3 q-pa-md">异常详情</div>
        <div class="col q-pa-md">异常编号：{{id}}</div>
        <div class="col q-pa-md">异常类型：{{case_type}}</div>
        <div class="col q-pa-md">异常等级：{{level}}</div>
        <div class="col q-pa-md">是否被查阅：{{checked?'是':'否'}}</div>
        <div class="col q-pa-md">出现时间：{{data_time}}</div>
        <q-btn class="col-2 q-ma-md" style="height: 60px; width: 150px" label="查阅"></q-btn>
      </div>
      <div class="col-6 column">
        <!--        <img src="">-->
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
  data(){
    return{
      detected_camera: "hh",
      case_type: "未知车辆闯入",
      level: 5,
      checked: true,
      data_time: "1999/1/1",
    }
  },
  methods:{

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

