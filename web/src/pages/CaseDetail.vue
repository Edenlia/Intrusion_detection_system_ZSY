<template>
  <q-page className="flex" style="background: #f0f2f5">
    <div class=" full-width row q-ma-md" style="height: 650px; background: #112347">
      <div class="col-6 column text-white">
        <div class="col-1">
          <q-btn
            class="q-ml-xs q-mt-md"
            color="blue"
            style="width: 80px; height: 40px"
            label="返回"
            @click="back"></q-btn>
        </div>
        <div class="col-2 text-h3 q-pa-md ">异常详情</div>
        <div class="col q-pa-md text-h5 q-ml-xl">异常编号：{{ id }}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">异常类型：{{ case_type }}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">异常等级：{{ level }}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">是否被查阅：{{ checked ? '已查阅' : '未查阅' }}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">出现时间：{{ date_time }}</div>
        <div class="col q-pa-md text-h5 q-ml-xl">详情：{{ description }}</div>
        <div class="col-2 row">
          <q-btn class=" q-ma-md q-ml-xl bg-green text-black text-h6"  glossy
                 style="height: 60px; width: 150px; font-weight: bold"
                 label="确认查阅" :disable="checked" @click="check_case"></q-btn>
          <q-btn class=" q-ma-md q-ml-xl bg-red text-black text-h6"  glossy
                 style="height: 60px; width: 150px; font-weight: bold" label="删除" @click="delete_dialog=true"></q-btn>
          <q-dialog v-model="delete_dialog" persistent>
            <q-card style="width: 400px;">
              <q-card-section class="row items-center">
                <span class="q-ml-sm">请问您确定要删除这条异常记录吗</span>
              </q-card-section>

              <q-card-actions align="right">
                <q-btn flat label="取消" color="primary" v-close-popup />
                <q-btn flat label="确认" color="primary" v-close-popup @click="delete_case"/>
              </q-card-actions>
            </q-card>
          </q-dialog>
        </div>

      </div>
      <div class="col-6 column q-pa-xl">
        <img class="q-pr-xl" style="width: 560px; height: 400px" :src="img"/>
      </div>
    </div>
  </q-page>
</template>

<script>
import {Notify} from "quasar";
import {api} from "boot/axios";

export default {
  name: "CaseDetail",
  props: ['id'],
  created() {
    this.get_case_detail()
  },
  data() {
    return {
      case_type: "",
      level: -1,
      checked: false,
      date_time: "",
      img: "",
      description: "",
      delete_dialog: false
    }
  },
  methods: {
    // test(){
    //   console.log(this.id)
    // }
    back(){
      this.$router.go(-1)
    },
    get_case_detail() {
      let _this = this
      let the_id = this.id
      api.post("http://172.30.68.249:8000/api/case/query_case/", {
        id: the_id
      }).then(function (response){
        let res = response.data
        if(res.status === "Success"){
          if(res.case_type === 1) _this.case_type = "未知车辆闯入"
          else if(res.case_type === 2) _this.case_type = "未知人员闯入"
          else _this.case_type = "敏感区域人员闯入"
          _this.level = res.level
          _this.date_time = res.date_time
          _this.checked = res.checked
          _this.img = res.img
          _this.description = res.description
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

    },
    check_case(){
      let _this = this
      let the_id = this.id
      api.post("http://172.30.68.249:8000/api/case/change_checked/", {
        id: the_id
      }).then(function (response){
        let res = response.data
        if(res.status === "Success"){
          _this.checked = true
          Notify.create(
            {
              type: 'positive',
              message: '成功'
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
    },
    delete_case(){
      let _this = this
      let the_id = this.id
      api.post("http://172.30.68.249:8000/api/case/delete_case/", {
        id: the_id
      }).then(function (response){
        let res = response.data
        if(res.status === "Success"){
          Notify.create(
            {
              type: 'positive',
              message: '删除成功'
            }
          )
          _this.back()
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
