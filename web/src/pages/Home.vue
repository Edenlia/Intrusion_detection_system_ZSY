<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-6 row q-py-md">
        <div class="col-6 q-px-md column">
          <div class="text-center col-1">摄像头1</div>
          <div class="col">
            <img style="width: 577px; height: 268px" src="http://127.0.0.1:8000/video/test1">
          </div>
        </div>
        <div class="col-6 q-px-md column">
          <div class="text-center col-1">摄像头2</div>
          <div class="col">
            <img style="width: 577px; height: 268px" src="http://127.0.0.1:8000/video/test1">
          </div>
        </div>
      </div>
      <div class="col-6 row q-py-md">
        <div class="col-6 q-px-md column">
          <div class="text-center col-1">摄像头3</div>
          <div class="col">
            <img style="width: 577px; height: 268px" :src="img_exist(camera_urls[2])">
          </div>
        </div>
        <div class="col-6 q-px-md column">
          <div class="text-center col-1">摄像头4</div>
          <div class="col">
            <img style="width: 577px; height: 268px" :src="img_exist(camera_urls[3])">
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: "Home",

  data(){
    return{
      img_error_url: 'img_error.jpg',
      camera_urls: ['', '', '', '']
    }
  },
  methods:{
    img_exist(url){
      if(url === ''){
        return require('assets/img/img_error.jpg')
      }else{
        return require(url)
      }
    }
  }
}
</script>

<style scoped>

</style>
