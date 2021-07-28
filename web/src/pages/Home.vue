<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-6 row q-py-md">
        <div class="col-6 q-px-md column">
          <div class="text-center col-1">摄像头1</div>
          <div class="col">
            <img style="width: 577px; height: 268px"
                 src="http://172.30.68.249:8000/video/test1">
          </div>
          </div>
        </div>
        <div class="col-6 q-px-md column">
          <div class="text-center col-1">摄像头2</div>
          <div class="col">

        </div>
      </div>
      <div class="col-6 row q-py-md">
        <div class="col-6 q-px-md column">
          <div class="text-center col-1">摄像头3</div>
          <div class="col">
            <img style="width: 577px; height: 268px"
                 :src="camera_urls[2] === ''?'http://ids.edenlia.icu/img_error.jpg':camera_urls[2]">
          </div>
        </div>
        <div class="col-6 q-px-md column">
          <div class="text-center col-1">摄像头4</div>
          <div class="col">
            <img style="width: 577px; height: 268px"
                 :src="camera_urls[3] === ''?'http://ids.edenlia.icu/img_error.jpg':camera_urls[3]">
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import axios from "axios";
import {Notify} from "quasar";
import 'video.js/dist/video-js.css'
import { videoPlayer } from 'vue-video-player'
import 'videojs-flash'

export default {
  name: "Home",
  created(){
    if(sessionStorage.getItem('user_id') === null){
      this.$router.push('/')
      return
    }
    this.user_id = sessionStorage.getItem('user_id')
    this.get_cameras()
  },
  data(){
    return{
      user_id: "",
      img_error_url: 'img_error.jpg',
      camera_urls: ['', '', '', ''],
      playerOptions: {//测试视频流数据
        width: "210",
        height: "134",
        language: 'zh-CN',
        techOrder: ['flash'],
        muted: true,
        autoplay: true,
        controls: true,
        loop: true,
        sources: [{
          type: 'rtmp/mp4',
          src: 'rtmp://localhost:1935/live/home' //rtmp流地址
        }],
        poster: 'static/fire/bgpp.png',
        flash:{
          swf:'static/video-js.swf' //视频屏幕小于400x300时设置
        }

      }
    }
  },
  methods:{
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
            _this.camera_urls[i] = 'http://172.30.68.249:8000/api/live/' + camera_list[i].name
          }
          console.log(_this.camera_urls[0])
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
