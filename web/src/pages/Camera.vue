<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-1 q-pt-md q-pl-md">
        <q-btn class="bg-blue text-white" label="添加摄像头" @click="if_add_camera">
          <q-icon name="add"></q-icon>
        </q-btn>
        <q-dialog v-model="add_camera_dialog" persistent>
          <q-card style="width: 600px">
            <q-card-section class="text-h5 text-center">
              添加摄像头
            </q-card-section>
            <q-card-section>
              <q-item>
                <q-item-section side>摄像头命名:</q-item-section>
                <q-item-section><q-input dense v-model="camera_name" autofocus></q-input></q-item-section>
              </q-item>
            </q-card-section>
            <q-card-section>
              <q-item>
                <q-item-section side>摄像头地址:</q-item-section>
                <q-item-section><q-input placeholder="rtmp分发地址" dense v-model="camera_address"></q-input></q-item-section>
              </q-item>
            </q-card-section>
            <q-card-section>
              <q-item>
                <q-item-section side>摄像头描述:</q-item-section>
                <q-item-section><q-input dense v-model="camera_description"></q-input></q-item-section>
              </q-item>
            </q-card-section>
            <q-card-section>
              <q-item>
                <q-item-section side>摄像头类型:</q-item-section>
                <q-item-section side class="q-gutter-sm">
                  <q-radio v-model="type" val="1" label="车辆车牌检测摄像头" />
                  <q-radio v-model="type" val="2" label="未知人脸检测摄像头" />
                  <q-radio v-model="type" val="3" label="敏感区域检测摄像头" />
                </q-item-section>
              </q-item>
            </q-card-section>
            <q-card-actions align="right" class="text-primary">
              <q-btn flat label="取消" v-close-popup />
              <q-btn flat label="确定" v-close-popup @click="add_camera"/>
            </q-card-actions>
          </q-card>
        </q-dialog>
        <q-dialog v-model="cant_add_camera_dialog">
          <q-card style="width: 400px">
            <q-card-section class="text-h4">
              警告
            </q-card-section>
            <q-card-section>
              最多添加四个摄像头
            </q-card-section>
            <q-card-actions align="right">
              <q-btn flat label="确认" color="primary" v-close-popup />
            </q-card-actions>
          </q-card>
        </q-dialog>

        <q-table
          class="my-sticky-header-table q-mt-xl"
          title="摄像头"
          :rows=cameras
          :columns=columns
          row-key="id"
          flat
          bordered
          @row-click="go_camera_detail"
        >
        </q-table>
      </div>
      <div class="col q-pa-md">

      </div>
    </div>
  </q-page>
</template>

<script>

import {Dialog, Notify} from 'quasar'
import { useQuasar } from 'quasar'
import { ref } from 'vue'
import axios from "axios";

export default {
  setup () {
    return {
      type: ref('line')
    }
  },
  created(){
    if(sessionStorage.getItem('user_id') === null){
      this.$router.push('/')
      return
    }
    this.user_id = sessionStorage.getItem('user_id')
    this.get_cameras()
  },
  name: "Camera",
  data(){
    return{
      user_id: "",
      add_camera_dialog: false,
      camera_name: "",
      camera_address: "",
      camera_description: "",
      cant_add_camera_dialog: false,
      columns: [
        {
          name: 'id',
          required: true,
          label: '摄像头编号',
          align: 'left',
          field: row => row.id,
          sortable: true
        },
        { name: 'camera_name', align: 'center', label: '摄像头命名', field: 'camera_name'},
        { name: 'camera_url', label: '摄像头url地址', field: 'camera_url', sortable: true },
        { name: 'camera_type', label: '摄像头类型', field: 'camera_type' },
        { name: 'camera_description', label: '摄像头描述', field: 'camera_description' },
      ],
      cameras:[],
    }
  },
  methods:{
    if_add_camera(){
      if(this.cameras.length <= 4) this.add_camera_dialog=true
      else this.cant_add_camera_dialog=true
    },
    add_camera(){

    },
    get_cameras(){
      let _this = this
      let user_id = this.user_id
      console.log(user_id)
      axios.post("http://172.30.68.249:8000/api/camera/query_camera/", {
        id : user_id
      }).then(function(response){
        console.log(response)
        let res = response.data
        if(res.status === "Success"){
          let camera_list = res.camera_list
          for(let i = 0; i < camera_list.length; i++){
            let row = {}
            row.id = camera_list[i].id
            row.camera_name = camera_list[i].name
            row.camera_url = camera_list[i].url
            row.camera_type = camera_list[i].type
            row.camera_description = camera_list[i].description
            _this.cameras.push(row)
          }
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
    go_camera_detail(){

    }
  }
}
</script>


<style scoped>

</style>
