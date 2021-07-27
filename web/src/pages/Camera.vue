<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-1 q-pt-md q-pl-md">
        <q-btn class="bg-blue text-white" label="添加摄像头" @click="add_camera_dialog = true">
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

import { Dialog } from 'quasar'
import { useQuasar } from 'quasar'
import { ref } from 'vue'

export default {
  setup () {
    return {
      type: ref('line')
    }
  },

  name: "Camera",
  data(){
    return{
      add_camera_dialog: false,
      camera_name: "",
      camera_address: "",
      camera_description: "",
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
        { name: 'camera_url', label: '摄像头url地址', field: 'case_type', sortable: true },
        { name: 'camera_type', label: '摄像头类型', field: 'level' },
        { name: 'camera_description', label: '摄像头描述', field: 'date_time' },
      ],
      cameras:[],
    }
  },
  methods:{
    add_camera(){

    },
    go_camera_detail(){

    }
  }
}
</script>


<style scoped>

</style>
