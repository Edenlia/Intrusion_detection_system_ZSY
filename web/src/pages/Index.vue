<template>
  <q-page class="flex flex-center">
    <img
      src="http://127.0.0.1:8000/video/"
    >
    <q-btn @click="request_video" label="hhh"></q-btn>
  </q-page>
</template>

<script>

import {api} from "boot/axios";

export default{
  name: 'PageIndex',
  data(){
    return{
      img: ""
    }
  },
  methods:{
    // request_video(){
    //   let _this = this
    //   let url = "http://127.0.0.1:8000/video/"
    //   api.post(url, {}).then(function (response){
    //
    //     console.log(response)
    //   })
    // }
  }
}
</script>
