<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-ma-md" style="height: 650px">
      <div class="col-1 q-pt-md q-pl-md">
        <q-btn class="bg-blue text-white" label="添加摄像头" @click="add_camera = true">
          <q-icon name="add"></q-icon>
        </q-btn>
        <q-dialog>

        </q-dialog>
      </div>
      <div class="col q-pa-md">

      </div>
    </div>
  </q-page>
</template>

<script>

import { Dialog } from 'quasar'
import { useQuasar } from 'quasar'

export default {
  name: "Camera",
  data(){
    return{
      add_camera: false
    }
  },
  methods:{

  }
}
</script>


<style scoped>

</style>
