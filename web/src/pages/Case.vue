<template>
  <q-page class="flex" style="background: #f0f2f5">
    <div class=" full-width column bg-white q-mx-md q-py-xs" style="height: 320px">
      <q-table
        class="my-sticky-header-table"
        title="未查看异常"
        :rows=checked_cases
        :columns=columns
        row-key="id"
        flat
        bordered
        @row-click="go_case_detail"
      >
      </q-table>
    </div>
    <div class=" full-width column bg-white q-mx-md q-py-xs" style="height: 320px">
      <q-table
        class="my-sticky-header-table"
        title="已查看异常"
        :rows=unchecked_cases
        :columns=columns
        row-key="id"
        flat
        bordered
        @row-click="go_case_detail"
      ></q-table>
    </div>
  </q-page>
</template>

<script>
import axios from "axios";
import {Notify} from "quasar";

export default {
  name: "Case",
  created(){
    if(sessionStorage.getItem('user_id') === null){
      this.$router.push('/')
      return
    }
    this.user_id = sessionStorage.getItem('user_id')
    this.get_all_query()
  },
  data(){
    return{
      columns: [
        {
          name: 'id',
          required: true,
          label: '异常编号',
          align: 'left',
          field: row => row.id,
          sortable: true
        },
        { name: 'detected_camera', align: 'center', label: '检测到异常的摄像头', field: 'camera_name'},
        { name: 'case_type', label: '异常类型', field: 'case_type', sortable: true },
        { name: 'level', label: '异常等级', field: 'level' },
        { name: 'data_time', label: '发生时间', field: 'date_time' },
      ],
      unchecked_cases:[],
      checked_cases:[]
    }
  },
  methods:{
    go_case_detail(evt, row){
      this.$router.push('/case_detail/' + row.id)
    },
    get_all_query(){
      let _this = this
      axios.post("http://127.0.0.1:8000/api/case/query_all_case/", {
        id : this.user_id
      }).then(function(response){
        console.log(response)
        let res = response.data
        if(res.status === "Success"){
          let case_list = res.case_list
          for(let i = 0; i < case_list.length; i++){
            let row = {}
            row.id = case_list[i].id
            row.camera_name = case_list[i].detect_camera
            row.checked = case_list[i].checked
            row.case_type = case_list[i].case_type
            row.case_description = case_list[i].case_description
            row.level = case_list[i].level
            row.date_time = case_list[i].date_time
            if(row.checked) _this.checked_cases.push(row)
            else _this.unchecked_cases.push(row)
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
    }

  }
}
</script>

<style lang="sass" scoped>
.my-sticky-header-table
  /* height or max-height is important */
  height: 310px

  .q-table__top,
  .q-table__bottom,
  thead tr:first-child th
    /* bg color is important for th; just specify one */
    background-color: #c1f4cd

  thead tr th
    position: sticky
    z-index: 1
  thead tr:first-child th
    top: 0

  /* this is when the loading indicator appears */
  &.q-table--loading thead tr:last-child th
    /* height of all previous header rows */
    top: 48px
</style>

